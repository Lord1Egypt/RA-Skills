#!/usr/bin/env python3
"""拼多多百亿补贴好货推荐 MCP Server v1.0

配合独立SCF函数 pdd-baiyi-proxy 使用。
SCF负责：全量拉取568条百亿补贴商品(5分钟TTL缓存) + 4维好货评分
         + 关键词匹配(类目>细分类>品牌>商品名) + 价格/品牌筛选 + 排序 + 分页
MCP负责：发送参数、接收结果、构建"稀缺精选商场"引导话术

设计理念：稀缺精选商场
- 第一层（无关键词）：进商场大门 → 展示Top30好货 + 总数568 + 品类分布引导
- 第二层（带关键词）：逛店铺 → 返回匹配结果 + 其他品类引导
- 始终传递"百亿补贴仅500+条，很稀缺"的认知

返回格式：JSON {"content": "...", "summary": "..."}
"""

import sys
import json
import urllib.request
import urllib.error

# ===== 配置 =====
PROXY_URL = "https://1439498936-44g9han8pj.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"

TIMEOUT_SHORT = 8    # 短超时：检测冷启动
TIMEOUT_LONG = 90    # 长超时：等待全量拉取完成（14页×0.5s间隔≈7秒+网络）

PAGE_SIZE = 30       # 每页展示30条
TOTAL_BAIYI = 568    # 百亿补贴全量商品数（实测）


def _scf_call(params, timeout=TIMEOUT_SHORT):
    """调用SCF代理"""
    payload = json.dumps({"tool": "list", "params": params}).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=payload,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            return {"_timeout": True}
        return {"_error": str(e)}
    except Exception as e:
        return {"_error": str(e)}


def _format_item(item):
    """格式化单条商品用于MCP返回"""
    return {
        "name": item.get("goods_name", ""),
        "product_url": item.get("product_url", ""),
        "original_price": item.get("normal_price", 0),
        "final_price": item.get("final_price", 0),
        "sales_tip": item.get("sales_tip", ""),
        "quality_desc": item.get("quality_desc", ""),
        "image_url": item.get("goods_image", ""),
    }


def _build_category_guide(category_overview, exclude_kw=None):
    """构建品类引导话术"""
    if not category_overview:
        return ""

    parts = []
    for c in category_overview[:6]:
        cat = c.get("category", "")
        cnt = c.get("count", 0)
        if cat and cnt > 0:
            parts.append(f"{cat}({cnt}件)")

    if not parts:
        return ""

    return "其他品类：" + "、".join(parts) + "。说\"看手机\"或\"看男装\"可按品类筛选。"


def tool_list(params):
    """百亿补贴好货推荐主查询函数"""
    keyword = str(params.get("keyword", "")).strip()
    category = str(params.get("category", "")).strip()
    search_kw = keyword or category

    max_price = params.get("max_price")
    min_price = params.get("min_price")
    brand_only = params.get("brand_only", False)
    sort_by = params.get("sort", "deal_score")
    page = int(params.get("page", 1) or 1)
    if page < 1:
        page = 1

    # ===== 第一步：调用SCF代理 =====
    scf_params = {"page": page, "sort": sort_by}
    if search_kw:
        scf_params["keyword"] = search_kw
    if max_price:
        scf_params["max_price"] = max_price
    if min_price:
        scf_params["min_price"] = min_price
    if brand_only:
        scf_params["brand_only"] = True

    data = _scf_call(scf_params, timeout=TIMEOUT_SHORT)

    # 冷启动检测
    if data.get("_timeout"):
        # SCF正在全量拉取，用长超时重试
        data = _scf_call(scf_params, timeout=TIMEOUT_LONG)
        if data.get("_timeout") or data.get("_error"):
            return json.dumps({
                "content": "",
                "summary": "正在为您精选百亿补贴好货，首次加载需约10秒，请稍候后再次查询。"
            }, ensure_ascii=False)

    if data.get("_error"):
        return json.dumps({
            "content": "",
            "summary": "查询失败，请稍后重试。"
        }, ensure_ascii=False)

    if data.get("error"):
        return json.dumps({
            "content": "",
            "summary": data["error"]
        }, ensure_ascii=False)

    # ===== 第二步：解析返回数据 =====
    items = data.get("results", [])
    total = data.get("total", 0)
    has_more = data.get("has_more", False)
    category_overview = data.get("category_overview", [])
    filter_applied = data.get("filter_applied", {})

    if not items and total == 0:
        # 0结果
        if search_kw:
            cat_guide = _build_category_guide(category_overview, search_kw)
            msg = f'百亿补贴中未找到与「{search_kw}」相关的商品。换个关键词试试'
            if cat_guide:
                msg += f'，或浏览其他品类：{cat_guide}'
            else:
                msg += '。'
        else:
            msg = "百亿补贴商品正在加载中，请稍后重试。"
        return json.dumps({"content": "", "summary": msg}, ensure_ascii=False)

    # ===== 第三步：构建商品列表 =====
    results = [_format_item(item) for item in items]

    # ===== 第四步：构建"稀缺精选商场"引导话术 =====
    page_start = (page - 1) * PAGE_SIZE + 1
    page_end = min(page * PAGE_SIZE, total)

    hints = []
    cat_guide = _build_category_guide(category_overview, search_kw)

    if not search_kw:
        # 第一层：无关键词（进商场）
        if page == 1:
            hints.append(f'百亿补贴仅{TOTAL_BAIYI}件商品入选，以上是好货Top{len(results)}。商品不多，逛得快。')
            if has_more:
                hints.append(f'当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
            if cat_guide:
                hints.append(cat_guide)
        else:
            # 翻页
            if has_more:
                hints.append(f'当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
            else:
                hints.append(f'当前显示第{page_start}-{page_end}条，已全部展示。')
            if cat_guide:
                hints.append(cat_guide)

    else:
        # 第二层：带关键词（逛店铺）
        if total <= PAGE_SIZE:
            # 结果少，全部展示
            hints.append(f'百亿补贴「{search_kw}」共{total}件商品，已全部展示。百亿补贴门槛高，每个品类入选商品都不多。')
            if cat_guide:
                hints.append(cat_guide)
        else:
            # 结果多，分页
            hints.append(f'百亿补贴「{search_kw}」共{total}件商品，展示第{page_start}-{page_end}条。')
            if has_more:
                hints.append(f'还有{total - page_end}条，说"下一页"查看更多。')
            else:
                hints.append('已到最后一页。')
            if cat_guide:
                hints.append(cat_guide)

    hints.append('（渲染提示：每条商品先展示图片![商品名](image_url)，然后图片下方单独放一行文字链接：[点击查看详情](product_url)，product_url是带佣金跟踪的推广短链接，用户通过此链接下单即计佣金）')

    return json.dumps({
        "content": json.dumps(results, ensure_ascii=False, indent=2),
        "summary": " ".join(hints)
    }, ensure_ascii=False)


TOOLS = {
    "list": tool_list,
}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"参数JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if tool not in TOOLS:
        print(json.dumps({"error": f"未知工具: {tool}，可用工具: {', '.join(TOOLS.keys())}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool](args)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
