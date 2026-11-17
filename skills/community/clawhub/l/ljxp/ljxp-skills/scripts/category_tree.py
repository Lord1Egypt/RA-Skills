#!/usr/bin/env python3
"""
蓝鲸选品 - 站点类目树查询脚本（带本地缓存）

【重要！后端接口参数 VS 脚本本地处理参数，切勿混淆】
  - 后端真实接口 `GET /category/tree` **只接受 1 个参数：siteId（站点）**。
    绝对没有 depth/keyword 等参数，任何情况下都不要把这两个值传给后端。
  - 本脚本里的 --search、--depth、--output、--refresh、--cache-ttl
    全部是【脚本拿到完整数据后的本地后处理能力】，不发额外请求、不扣额外积分。

核心策略：
  1. 首次调用时，花费 10 积分请求 /category/tree?siteId=XXX 接口，
     把整站类目树完整保存到本地缓存文件，同时持久化后端返回的 cacheLastModified（后端类目文件修改时间）。
  2. 后续相同站点的查询，直接读取本地缓存，**不再调用后端接口，不消耗积分**。
  3. 缓存过期判定以 **后端 cacheLastModified + TTL（默认 7 天）** 为基准：
     当当前时间超过 cacheLastModified + 7 天，视为过期，下次查询自动重新拉取（花 10 积分）。
     也可以手动加 --refresh 强制刷新。
  4. --search 关键词过滤、--depth 深度截断打印、--output json 导出：
     全部在本地缓存数据上完成，无需再次付费。

用法:
  # 只带 --site 就够了：命中缓存直接免费，没缓存才花积分调接口
  python category_tree.py --site MLM
  python category_tree.py --token <TOKEN> --site MLM --refresh   # 强制刷新缓存，本次消耗 10 积分

  # 以下参数全是本地后处理，不传后端、不额外花积分：
  python category_tree.py --site MLM --depth 3                    # 本地只打印前 3 层
  python category_tree.py --site MLM --search 手机壳               # 本地过滤只显示匹配节点+祖先链
  python category_tree.py --site MLM --search "phone case" --output json  # 本地过滤后导出 JSON

参数说明（再次强调：只有 --site 会传给后端，其余均为本地处理）:
  【传给后端接口的参数】
  --site       站点，可选 MLM/MLB/MLC/MLA/MCO，默认 MLM
               （对应后端接口 siteId 参数，唯一需要透传到 /category/tree 的值）

  【鉴权参数（只有真正请求后端时才需要）】
  --token      Authorization Token（缓存命中时可省略；缓存未命中或 --refresh 时需要，
               或通过环境变量 LJXP_TOKEN 设置）

  【脚本本地处理参数，不会发给后端接口】
  --depth      【本地打印截断】默认 3 层；设为 0 表示不限制。不会传给后端。
  --search     【本地关键词过滤】匹配中文 zhName / 英文 name / 类目 ID，
               只保留命中节点及其完整祖先路径。不会传给后端。
  --output     【本地输出格式】table（默认，缩进打印树）/ json（完整 JSON）
  --refresh    【本地缓存控制】强制刷新：忽略本地缓存，重新从后端拉取并覆盖缓存
               （本次消耗 10 积分）
  --cache-ttl  【本地缓存控制】以「后端 cacheLastModified（后端类目 JSON 文件修改时间）」为基准的有效期（秒），
               默认 7 天（604800 秒）；0 表示永不过期。
               当前时间超过 cacheLastModified + TTL 即视为缓存过期，会重新请求后端（花 10 积分）。
               控制的是本地缓存判断，不会传给后端。
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    get_token, request_get, check_response, output_json,
    SITE_NAMES, VALID_SITES
)


# ============================================================
# 缓存配置
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 缓存放 skills/ljxp-skills/cache/ 目录下，与 scripts/ 同级
CACHE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "cache"))
DEFAULT_CACHE_TTL = 7 * 24 * 3600  # 7 天（秒）


def _cache_file_path(site):
    """按站点分文件，如 category_tree_MLM.json"""
    return os.path.join(CACHE_DIR, f"category_tree_{site}.json")


def _ensure_cache_dir():
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR, exist_ok=True)


def _parse_server_modified_to_ts(s):
    """
    把后端 cacheLastModified 字符串 "yyyy-MM-dd HH:mm:ss" 解析为本地时区的 epoch 秒（int）。
    解析失败或为空时返回 None。
    """
    if not s or not isinstance(s, str):
        return None
    try:
        # time.strptime 默认用本地时区解释该时间字符串（与后端格式化所用 ZoneId.systemDefault() 一致）
        return int(time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S")))
    except (ValueError, TypeError):
        return None


def load_cached_category_tree(site, ttl=DEFAULT_CACHE_TTL):
    """
    尝试从本地缓存读取站点类目树。
    过期判定规则（按优先级）：
      1) 若缓存文件内记录了 server_cache_last_modified（后端返回的 cacheLastModified 字符串），
         则以该时间 + TTL 为过期阈值：now > (server_cache_last_modified_ts + TTL) 即过期。
      2) 否则（旧缓存文件没有该字段），退化使用本地 cached_at + TTL 判定。
      ttl == 0 时永不过期。
    返回：(data_list, info_dict) 或 (None, None) 表示缓存未命中/过期。
    info_dict 包含 cached_at / source / server_cache_last_modified 等元信息。
    """
    path = _cache_file_path(site)
    if not os.path.isfile(path):
        return None, None

    try:
        with open(path, "r", encoding="utf-8") as f:
            blob = json.load(f)
    except (OSError, json.JSONDecodeError):
        # 缓存文件损坏，直接删掉下次重建
        try:
            os.remove(path)
        except OSError:
            pass
        return None, None

    cached_at = blob.get("cached_at", 0)
    data = blob.get("data")
    if not isinstance(data, list):
        return None, None

    server_modified_str = blob.get("server_cache_last_modified")
    server_modified_ts = _parse_server_modified_to_ts(server_modified_str)

    # ttl == 0 表示永不过期
    if ttl > 0:
        now = time.time()
        if server_modified_ts is not None:
            # 规则：以 cacheLastModified + TTL 为准
            if now > (server_modified_ts + ttl):
                return None, None
        else:
            # 兼容老缓存：退化按 cached_at + TTL
            if (now - cached_at) > ttl:
                return None, None

    info = {"cached_at": cached_at, "source": path}
    if server_modified_str:
        info["server_cache_last_modified"] = server_modified_str
    return data, info


def save_cached_category_tree(site, data, server_cache_last_modified=None):
    """把接口返回的类目树保存到本地缓存。"""
    _ensure_cache_dir()
    path = _cache_file_path(site)
    blob = {
        "site": site,
        "cached_at": int(time.time()),
        "data": data,
    }
    if server_cache_last_modified is not None:
        blob["server_cache_last_modified"] = server_cache_last_modified
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(blob, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
    return path


# ============================================================
# 搜索过滤：只保留匹配节点及其完整祖先路径
# ============================================================
def _node_id(node):
    """兼容读取节点 ID：后端返回 id / 原始文件 i"""
    return node.get("id") or node.get("i") or ""

def _node_name(node):
    """兼容读取节点英文名：后端返回 name / 原始文件 n"""
    return node.get("name") or node.get("n") or ""

def _node_zhname(node):
    """兼容读取节点中文名：后端返回 zhName / 下划线 zh_name / 原始文件 z"""
    return node.get("zhName") or node.get("zh_name") or node.get("z") or ""

def _node_children(node):
    """兼容读取子节点：后端返回 children / 原始文件 c"""
    c = node.get("children")
    if c is None:
        c = node.get("c")
    return c or []


def _keyword_match(node, keyword):
    """检查某个节点是否命中关键词（不区分大小写，匹配中文名或英文名）"""
    if not keyword:
        return True
    kw = keyword.lower()
    name = _node_name(node).lower()
    zh_name = _node_zhname(node).lower()
    cid = _node_id(node).lower()
    return kw in name or kw in zh_name or kw in cid


def filter_tree(nodes, keyword):
    """
    递归过滤树，只保留命中关键词的节点及其完整祖先链。
    keyword 为空时原样返回。
    返回：(过滤后的列表, 是否有任意节点命中)
    """
    if not keyword:
        return nodes, True

    result = []
    has_match = False
    for node in nodes or []:
        children = _node_children(node)
        filtered_children, child_has_match = filter_tree(children, keyword)
        self_match = _keyword_match(node, keyword)

        if self_match or child_has_match:
            new_node = {
                "id": _node_id(node),
                "name": _node_name(node),
                "zhName": _node_zhname(node),
                "children": filtered_children if child_has_match else [],
            }
            result.append(new_node)
            has_match = True

    return result, has_match


# ============================================================
# 打印树（缩进 + 前缀）
# ============================================================
def _print_node(node, level, depth_limit, is_last, parent_prefix):
    if level == 0:
        connector = ""
    else:
        connector = "└─ " if is_last else "├─ "

    cid = _node_id(node) or "N/A"
    name = _node_name(node)
    zh_name = _node_zhname(node)
    zh_part = f"  ({zh_name})" if zh_name else ""
    print(f"{parent_prefix}{connector}[{cid}] {name}{zh_part}")

    if depth_limit and level + 1 >= depth_limit:
        return

    children = _node_children(node)
    if not children:
        return

    if level == 0:
        child_base_prefix = ""
    else:
        child_base_prefix = parent_prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(children):
        child_last = (i == len(children) - 1)
        _print_node(child, level + 1, depth_limit, child_last, child_base_prefix)


def print_category_tree(nodes, depth_limit=3, source_label=None, site=None):
    """打印类目树的入口函数。source_label 会在标题里显示，比如「本地缓存」。"""
    if not nodes:
        print("\n（空结果：没有找到任何类目节点）")
        return

    site_label = SITE_NAMES.get(site, site) if site else ""
    title_parts = [f"{site_label} 站点类目树"]
    if source_label:
        title_parts.append(f"（{source_label}）")
    title_parts.append(f"深度限制：{'不限' if depth_limit == 0 else str(depth_limit) + ' 层'}")

    print(f"\n{'=' * 80}")
    print(" · ".join(title_parts))
    print(f"{'=' * 80}")

    for i, root in enumerate(nodes):
        is_last_root = (i == len(nodes) - 1)
        _print_node(root, 0, depth_limit, is_last_root, "")

    print(f"\n共显示 {len(nodes)} 个一级类目。")
    if depth_limit:
        print(f"💡 提示：当前只打印前 {depth_limit} 层，想查看更深层请加大 --depth，或用 --search 关键词过滤。")


# ============================================================
# 主函数
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="蓝鲸选品 - 站点类目树查询工具（带本地缓存，同站点首次花 10 积分，后续免费）\n"
                    "【关键提醒】后端 /category/tree 接口仅接受 siteId；"
                    "--search/--depth/--output/--refresh/--cache-ttl 全为本地后处理，不会发给后端。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 命中缓存直接免费返回，未命中才请求后端（10 积分）
  %(prog)s --site MLM
  %(prog)s --token <TOKEN> --site MLM --refresh   # 强制重拉，覆盖缓存（10 积分）

  # 下面的参数都在本地处理，不会发给后端、不额外扣积分：
  %(prog)s --site MLM --depth 2
  %(prog)s --site MLM --search 手机
  %(prog)s --site MLB --search "phone" --output json
        """
    )
    parser.add_argument("--token", default=None,
                        help="【鉴权，仅真正请求后端时用】Authorization Token（缓存命中时可省略）。⚠️ [不推荐] 会暴露在 shell 历史/进程列表；优先用环境变量 LJXP_TOKEN")
    parser.add_argument("--site", default="MLM", choices=VALID_SITES,
                        help="【传给后端 siteId】站点，默认 MLM。"
                             "这是唯一会透传到 /category/tree 接口的参数。")
    parser.add_argument("--depth", type=int, default=3,
                        help="【本地打印截断】默认 3 层；0=不限。不会发给后端。")
    parser.add_argument("--search", default=None,
                        help="【本地过滤】匹配中/英文名/ID，保留节点+祖先链。不会发给后端。")
    parser.add_argument("--output", default="table", choices=["table", "json"],
                        help="【本地输出】table 或 json。不会发给后端。")
    parser.add_argument("--refresh", action="store_true",
                        help="【本地缓存控制】忽略缓存、重拉后端并覆盖（本次 10 积分）。不会发给后端。")
    parser.add_argument("--cache-ttl", type=int, default=DEFAULT_CACHE_TTL,
                        help="【本地缓存控制】有效期（秒），以 cacheLastModified（后端类目 JSON 修改时间）为基准，"
                             "默认 604800=7 天；0=永不过期。不会发给后端。")

    args = parser.parse_args()

    site_name = SITE_NAMES.get(args.site, args.site)
    cache_ttl = 0 if args.cache_ttl < 0 else args.cache_ttl

    # -----------------------------------------------------------
    # Step 1: 尝试命中本地缓存（非 --refresh 模式下）
    # -----------------------------------------------------------
    raw_data = None
    source_hint = ""  # 展示给用户：本次数据从哪里来

    if not args.refresh:
        cached_data, cache_info = load_cached_category_tree(args.site, ttl=cache_ttl)
        if cached_data is not None:
            raw_data = cached_data
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cache_info["cached_at"]))
            parts = [f"来源：本地缓存（写入于 {dt}，文件 {cache_info['source']}），本次不消耗积分 ✅"]
            if cache_info.get("server_cache_last_modified"):
                svr = cache_info["server_cache_last_modified"]
                ttl_days = "永不过期" if cache_ttl == 0 else f"{cache_ttl / 86400:.1f} 天"
                parts.append(f"后端缓存更新于：{svr}（过期判定：{svr} + {ttl_days}）")
            source_hint = " | ".join(parts)
            print(f"✅ {source_hint}", file=sys.stderr)

    # -----------------------------------------------------------
    # Step 2: 缓存未命中 或 --refresh → 调用后端接口（消耗 10 积分）
    # -----------------------------------------------------------
    if raw_data is None:
        token = get_token(args.token)  # 只有真正要调接口时才要求 Token
        action = "重新拉取" if args.refresh else "本地无缓存，首次查询"
        print(f"正在 {action} {site_name} 站点类目树（请求 /category/tree，本次消耗 10 积分）...",
              file=sys.stderr)

        params = {"siteId": args.site}
        response = request_get("/category/tree", token, params)
        check_response(response)
        # 【后端返回结构，严格对齐 Java Response<CategoryTreeResponse>】
        # {
        #   "code": 0,
        #   "msg": "success",
        #   "timestamp": 1234567890,
        #   "data": {
        #       "list": [ { "id": "...", "name": "...", "zhName": "...", "children": [...] } ],
        #       "cacheLastModified": "yyyy-MM-dd HH:mm:ss"
        #   }
        # }
        data_payload = response.get("data") or {}
        if not isinstance(data_payload, dict):
            print(f"⚠️  后端返回 data 字段不是对象，实际结构: {type(data_payload)}", file=sys.stderr)
            print(f"   原始返回 keys: {list(response.keys())}", file=sys.stderr)
            if isinstance(data_payload, list):
                # 兼容 data 直接就是 list 的情况（极少，兜底）
                raw_data = data_payload or []
                server_cache_last_modified = None
            else:
                print("错误：无法解析后端返回结构，请确认 /category/tree 接口是否正常", file=sys.stderr)
                sys.exit(1)
        else:
            raw_data = data_payload.get("list", []) or []
            server_cache_last_modified = data_payload.get("cacheLastModified")

        # 写入缓存（失败不影响结果，打个 warning 即可）
        try:
            saved_path = save_cached_category_tree(args.site, raw_data,
                                                    server_cache_last_modified=server_cache_last_modified)
            if server_cache_last_modified:
                cache_part = f"（后端缓存更新于：{server_cache_last_modified}）"
            else:
                cache_part = ""
            source_hint = (f"来源：后端接口（已写入缓存 {saved_path}，同站点下次起可免积分复用）{cache_part}"
                           f"，本次消耗 10 积分")
            print(f"💾 已缓存到 {saved_path}，下次相同站点查询直接免费复用。", file=sys.stderr)
        except OSError as e:
            source_hint = "来源：后端接口，本次消耗 10 积分（缓存写入失败：%s）" % e
            print(f"⚠️  缓存写入失败：{e}（不影响本次结果，但下次仍需重新付费）", file=sys.stderr)

    # -----------------------------------------------------------
    # Step 3: JSON 输出模式（完整原数据，不过滤不截断）
    # -----------------------------------------------------------
    if args.output == "json":
        # 【对齐后端 Response 字段命名】key 统一用 msg 而不是 message
        wrapper = {"code": 0, "msg": "success", "data": raw_data}
        output_json(wrapper)
        return

    # -----------------------------------------------------------
    # Step 4: Table 输出模式 → （可选）关键词过滤 + 打印树
    # -----------------------------------------------------------
    data_to_print = raw_data
    if args.search:
        filtered, matched = filter_tree(raw_data, args.search)
        if not matched:
            print(f"\n⚠️  未找到包含 \"{args.search}\" 的类目。请尝试其他关键词，或用 --output json 查看完整树。")
            print(f"   （当前结果{source_hint and ('：' + source_hint)}）")
            return
        data_to_print = filtered

    print_category_tree(data_to_print, depth_limit=args.depth, source_label=source_hint, site=args.site)

    if args.search:
        print(f"\n🔍 匹配关键词：\"{args.search}\"（上面只显示了匹配节点及其祖先类目）")

    # -----------------------------------------------------------
    # Step 5: 关联操作提示（取第一个二级类目 ID 做示例）
    # -----------------------------------------------------------
    sample_id = None
    if raw_data:
        first_root = raw_data[0]
        first_children = first_root.get("children") or []
        if first_children:
            sample_id = first_children[0].get("id")
        if not sample_id:
            sample_id = first_root.get("id")

    if sample_id:
        print(f"\n💡 提示: 拿到类目 ID 后，可进一步分析：")
        print(f"   ① 查询该类目趋势:")
        print(f"      python trends.py --site {args.site} --type statistical --category-id {sample_id}")
        print(f"   ② 在该类目下搜索商品（按 30 天销量排序）:")
        print(f"      python search_items.py --site {args.site} --category-id {sample_id} --sort-key sale30 --sort-order desc")


if __name__ == "__main__":
    main()
