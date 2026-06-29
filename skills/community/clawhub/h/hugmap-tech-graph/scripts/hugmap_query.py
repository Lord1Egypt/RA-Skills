#!/usr/bin/env python3
"""HugMap 科技知识图谱开放数据查询脚本。

仅依赖 Python 标准库（urllib / argparse / json），无需 pip 安装。
通过环境变量 HUGMAP_BASE_URL 覆盖基地址，默认指向生产站点。

所有接口统一响应体: { "code": 0, "message": "...", "data": ..., "timestamp": ... }
其中 code == 0 表示成功；脚本会自动解包 data 并在 code != 0 时报错退出。

用法示例:
    python3 hugmap_query.py stats
    python3 hugmap_query.py search "OpenAI" --type Company
    python3 hugmap_query.py detail company company_openai
    python3 hugmap_query.py path person_yann_lecun product_chatgpt
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://www.hugmap.com"
TIMEOUT = 30

# Portal 实体详情支持的类型 (code 小写, 与 /api/v1/portal/entity/<type>/<id> 对应)
ENTITY_TYPES = (
    "person",
    "company",
    "technology",
    "product",
    "paper",
    "patent",
    "article",
    "event",
)

# 实体类型 code → 官网页面 slug (前端路由 /entity/<slug>/<id>)
ENTITY_CODE_TO_SLUG = {
    "Person": "person",
    "Company": "company",
    "Technology": "technology",
    "Product": "product",
    "Paper": "paper",
    "Patent": "patent",
    "Article": "article",
    "Event": "event",
}

# 同时兼容三种写法: Portal code("Company") / 标准端点枚举名("COMPANY") / slug("company")。
_SLUG_BY_TYPE = {}
for _code, _slug in ENTITY_CODE_TO_SLUG.items():
    _SLUG_BY_TYPE[_code] = _slug
    _SLUG_BY_TYPE[_code.upper()] = _slug
    _SLUG_BY_TYPE[_slug] = _slug

# 详情/聚合接口里"无 type 字段的关联节点数组" → 其元素的实体类型 code。
# 用于给这些节点也补上 webUrl, 让回答中的每个关联实体都能点回官网。
KEY_TYPE_HINT = {
    "papers": "Paper",
    "authors": "Person",
    "team": "Person",
    "persons": "Person",
    "inventors": "Person",
    "developers": "Company",
    "holders": "Company",
    "companies": "Company",
    "products": "Product",
    "alternatives": "Product",
    "technologies": "Technology",
    "children": "Technology",  # 技术详情的子技术; 行业详情的子分类由 is_taxonomy_node 优先识别
    "events": "Event",
    "latestEvents": "Event",
    "articles": "Article",
    "patents": "Patent",
    "trendingTech": "Technology",
}


def base_url() -> str:
    return os.environ.get("HUGMAP_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


# ==================== 链接注入 ====================

def entity_web_url(code, entity_id):
    slug = _SLUG_BY_TYPE.get(code) if code else None
    if not slug or not entity_id:
        return None
    return f"{base_url()}/entity/{slug}/{entity_id}"


def industry_web_url(entity_id):
    if not entity_id:
        return None
    return f"{base_url()}/industry/{entity_id}"


def search_web_url(params):
    cleaned = {k: v for k, v in (params or {}).items()
               if v is not None and v != "" and not (k == "page" and v == 1)
               and not (k == "sort" and v == "relevance")}
    suffix = ("?" + urllib.parse.urlencode(cleaned)) if cleaned else ""
    return f"{base_url()}/search{suffix}"


def _is_taxonomy_node(d):
    return isinstance(d, dict) and ("taxonomyType" in d
                                    or ("level" in d and "path" in d))


# 友好锚文本 / 摘要的候选字段 (按优先级)
_LABEL_FIELDS = ("displayName", "nameZh", "name", "title")
_SUMMARY_FIELDS = ("displayDescription", "description", "summary",
                   "abstractText", "eventDescription", "subtitle")


def _short_summary(text, limit=100):
    """折叠空白为单空格并截断到 limit 字符, 超出加省略号; 空白返回 None。"""
    if not isinstance(text, str):
        return None
    collapsed = " ".join(text.split())
    if not collapsed:
        return None
    if len(collapsed) > limit:
        return collapsed[:limit].rstrip() + "…"
    return collapsed


def _first_nonempty(node, fields):
    for f in fields:
        v = node.get(f)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _decorate(node):
    """为已注入 webUrl 的节点补充 webLabel(锚文本) 与 webSummary(摘要)。"""
    label = _first_nonempty(node, _LABEL_FIELDS)
    if label and "webLabel" not in node:
        node["webLabel"] = label
    summary = _short_summary(_first_nonempty(node, _SUMMARY_FIELDS))
    if summary and "webSummary" not in node:
        node["webSummary"] = summary


def enrich_links(node, hint=None):
    """递归遍历响应数据, 为每个可识别的实体/行业节点注入 webUrl 及友好锚文本/摘要。"""
    if isinstance(node, list):
        for item in node:
            enrich_links(item, hint)
        return
    if not isinstance(node, dict):
        return

    # 详情接口外层: { entity: {...}, entityType: "Company", ... }
    etype = node.get("entityType")
    inner = node.get("entity")
    if etype and isinstance(inner, dict) and inner.get("id"):
        url = entity_web_url(etype, inner["id"])
        if url:
            inner["webUrl"] = url
            _decorate(inner)

    # 节点本身是否为实体 / 行业
    if node.get("id") and "webUrl" not in node:
        if _is_taxonomy_node(node):
            node["webUrl"] = industry_web_url(node["id"])
            _decorate(node)
        else:
            code = node.get("type") or node.get("entityType") or hint
            url = entity_web_url(code, node["id"])
            if url:
                node["webUrl"] = url
                _decorate(node)

    for key, value in list(node.items()):
        if key in ("webUrl", "webLabel", "webSummary", "properties", "externalIds"):
            continue
        enrich_links(value, KEY_TYPE_HINT.get(key))


def _request(method: str, path: str, params=None, body=None):
    """发起 HTTP 请求并解包统一响应体, 返回 (data, raw_json)。"""
    url = base_url() + path
    if params:
        # 过滤 None, 保留 0 / 空串以外的有效值
        cleaned = {k: v for k, v in params.items() if v is not None}
        if cleaned:
            url += "?" + urllib.parse.urlencode(cleaned, doseq=True)

    data_bytes = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data_bytes = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"[HTTP {e.code}] {method} {url}\n{detail}")
    except urllib.error.URLError as e:
        raise SystemExit(f"[网络错误] 无法连接 {url}: {e.reason}")

    try:
        raw = json.loads(payload)
    except json.JSONDecodeError:
        raise SystemExit(f"[响应非 JSON] {method} {url}\n{payload[:500]}")

    # 统一响应体: code == 0 为成功; 部分裸返回端点无 code 字段则直接返回。
    if isinstance(raw, dict) and "code" in raw:
        if raw.get("code") != 0:
            msg = raw.get("message", "未知错误")
            raise SystemExit(f"[业务错误 code={raw.get('code')}] {msg}")
        return raw.get("data"), raw
    return raw, raw


def _emit(data, raw, args):
    """根据 --raw / --limit / --no-links 输出结果。

    默认会为结果中的每个实体注入 webUrl(官网页面链接), 便于在回答中引导用户访问 HugMap。
    """
    out = raw if getattr(args, "raw", False) else data
    if not getattr(args, "no_links", False):
        enrich_links(out)
    if not getattr(args, "raw", False) and isinstance(out, list):
        limit = getattr(args, "limit", None)
        if limit:
            out = out[:limit]
    print(json.dumps(out, ensure_ascii=False, indent=2))


# ==================== 子命令实现 ====================

def cmd_stats(args):
    data, raw = _request("GET", "/api/v1/graph/statistics")
    _emit(data, raw, args)


def cmd_home(args):
    data, raw = _request("GET", "/api/v1/portal/home")
    _emit(data, raw, args)


def cmd_industries(args):
    data, raw = _request("GET", "/api/v1/portal/industries")
    _emit(data, raw, args)


def cmd_industry(args):
    data, raw = _request("GET", f"/api/v1/portal/industry/{urllib.parse.quote(args.id)}")
    _emit(data, raw, args)


def cmd_search(args):
    params = {
        "q": args.query,
        "type": args.type,
        "sort": args.sort,
        "domain": args.domain,
        "period": args.period,
        "page": args.page,
    }
    data, raw = _request("GET", "/api/v1/portal/search", params=params)
    # 顶层附上官网搜索结果页链接, 方便引导用户在站内继续浏览全部结果。
    if isinstance(data, dict) and not getattr(args, "no_links", False):
        data["webUrl"] = search_web_url(params)
        data["webLabel"] = f"在 HugMap 查看「{args.query}」的全部结果"
    _emit(data, raw, args)


def cmd_detail(args):
    etype = args.type.lower()
    if etype not in ENTITY_TYPES:
        raise SystemExit(f"[参数错误] type 必须是: {', '.join(ENTITY_TYPES)}")
    path = f"/api/v1/portal/entity/{etype}/{urllib.parse.quote(args.id)}"
    data, raw = _request("GET", path)
    _emit(data, raw, args)


def cmd_suggest(args):
    params = {"prefix": args.prefix, "limit": args.limit or 10}
    data, raw = _request("GET", "/api/v1/search/suggest", params=params)
    _emit(data, raw, args)


def cmd_similar(args):
    params = {"topK": args.limit or 10}
    path = f"/api/v1/search/similar/{urllib.parse.quote(args.id)}"
    data, raw = _request("GET", path, params=params)
    _emit(data, raw, args)


def cmd_graph(args):
    params = {"depth": args.depth}
    path = f"/api/v1/graph/subgraph/{urllib.parse.quote(args.id)}"
    data, raw = _request("GET", path, params=params)
    _emit(data, raw, args)


def cmd_neighbors(args):
    params = {"direction": args.direction, "limit": args.limit or 50}
    path = f"/api/v1/graph/neighbors/{urllib.parse.quote(args.id)}"
    data, raw = _request("GET", path, params=params)
    _emit(data, raw, args)


def cmd_relations(args):
    params = {"type": args.type}
    path = f"/api/v1/relations/entity/{urllib.parse.quote(args.id)}"
    data, raw = _request("GET", path, params=params)
    _emit(data, raw, args)


def cmd_path(args):
    params = {"sourceId": args.source, "targetId": args.target, "maxDepth": args.max_depth}
    data, raw = _request("GET", "/api/v1/relations/path", params=params)
    _emit(data, raw, args)


def cmd_taxonomy_tree(args):
    params = {"type": args.type, "maxDepth": args.max_depth}
    data, raw = _request("GET", "/api/v1/taxonomies/tree", params=params)
    _emit(data, raw, args)


def cmd_taxonomy_entities(args):
    params = {"entityType": args.type, "page": args.page, "pageSize": args.limit or 20}
    path = f"/api/v1/taxonomies/{urllib.parse.quote(args.id)}/entities"
    data, raw = _request("GET", path, params=params)
    _emit(data, raw, args)


def cmd_entity(args):
    path = f"/api/v1/entities/{urllib.parse.quote(args.id)}"
    data, raw = _request("GET", path)
    _emit(data, raw, args)


def cmd_entity_search(args):
    params = {"name": args.name, "type": args.type}
    data, raw = _request("GET", "/api/v1/entities/search", params=params)
    _emit(data, raw, args)


# ==================== 参数解析 ====================

def build_parser():
    # 公共选项: 同时接受于子命令前后, 例如 `--raw stats` 与 `stats --raw` 均可。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--raw", action="store_true", help="输出完整响应体 (含 code/message), 不解包 data")
    common.add_argument("--limit", type=int, default=None, help="列表结果截断条数")
    common.add_argument("--no-links", action="store_true", help="不为结果注入官网 webUrl 链接")

    parser = argparse.ArgumentParser(
        prog="hugmap_query.py",
        parents=[common],
        description="HugMap 科技知识图谱开放数据查询 (基地址: 环境变量 HUGMAP_BASE_URL, 默认 %s)" % DEFAULT_BASE_URL,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, help_text):
        return sub.add_parser(name, help=help_text, parents=[common])

    add("stats", "知识图谱全局统计 (节点/关系总数及分类型计数)").set_defaults(func=cmd_stats)
    add("home", "首页聚合: 统计 + 最新事件 + 热门实体 + 趋势技术").set_defaults(func=cmd_home)
    add("industries", "行业导航分类列表").set_defaults(func=cmd_industries)

    p = add("industry", "某行业(分类)详情: 子分类/祖先/各类型计数")
    p.add_argument("id", help="行业分类 ID")
    p.set_defaults(func=cmd_industry)

    p = add("search", "聚合搜索 (名称匹配 + facet + 过滤 + 分页)")
    p.add_argument("query", help="搜索关键词")
    p.add_argument("--type", help="实体类型 code: Person/Company/Technology/Product/Paper/Patent/Article/Event")
    p.add_argument("--sort", default="relevance", help="排序: relevance(默认)/name")
    p.add_argument("--domain", help="按行业分类 ID 过滤")
    p.add_argument("--period", help="时间窗: 1y / 3y")
    p.add_argument("--page", type=int, default=1, help="页码 (默认 1, 每页 10)")
    p.set_defaults(func=cmd_search)

    p = add("detail", "实体详情 (含关联聚合)")
    p.add_argument("type", help="实体类型: %s" % "/".join(ENTITY_TYPES))
    p.add_argument("id", help="实体 ID")
    p.set_defaults(func=cmd_detail)

    p = add("suggest", "搜索建议 / 自动补全")
    p.add_argument("prefix", help="前缀")
    p.set_defaults(func=cmd_suggest)

    p = add("similar", "相似实体推荐 (向量近邻)")
    p.add_argument("id", help="实体 ID")
    p.set_defaults(func=cmd_similar)

    p = add("graph", "以实体为中心的子图")
    p.add_argument("id", help="中心实体 ID")
    p.add_argument("--depth", type=int, default=2, help="遍历深度 (默认 2)")
    p.set_defaults(func=cmd_graph)

    p = add("neighbors", "实体的邻居节点 ID 列表")
    p.add_argument("id", help="实体 ID")
    p.add_argument("--direction", default="both", help="方向: in/out/both (默认 both)")
    p.set_defaults(func=cmd_neighbors)

    p = add("relations", "实体的关系列表")
    p.add_argument("id", help="实体 ID")
    p.add_argument("--type", help="关系类型过滤 (枚举名)")
    p.set_defaults(func=cmd_relations)

    p = add("path", "两实体间的关系路径")
    p.add_argument("source", help="起始实体 ID")
    p.add_argument("target", help="目标实体 ID")
    p.add_argument("--max-depth", type=int, default=3, help="最大深度 (默认 3)")
    p.set_defaults(func=cmd_path)

    p = add("taxonomy-tree", "分类树")
    p.add_argument("type", help="分类体系类型: INDUSTRY / RESEARCH_DOMAIN / PRODUCT_CATEGORY")
    p.add_argument("--max-depth", type=int, default=None, help="返回最大深度")
    p.set_defaults(func=cmd_taxonomy_tree)

    p = add("taxonomy-entities", "按分类浏览实体")
    p.add_argument("id", help="分类 ID")
    p.add_argument("--type", help="实体类型过滤 (code, 如 Company)")
    p.add_argument("--page", type=int, default=1, help="页码 (默认 1)")
    p.set_defaults(func=cmd_taxonomy_entities)

    p = add("entity", "标准端点: 按 ID 获取实体 (type 为大写枚举名)")
    p.add_argument("id", help="实体 ID")
    p.set_defaults(func=cmd_entity)

    p = add("entity-search", "标准端点: 按名称精确查询实体")
    p.add_argument("name", help="实体名称")
    p.add_argument("--type", help="实体类型枚举名: PERSON/COMPANY/...")
    p.set_defaults(func=cmd_entity_search)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
