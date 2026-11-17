#!/usr/bin/env python3
"""
蓝鲸选品 - 通用工具模块
提供 HTTP 请求封装、鉴权检查、结果格式化等通用功能。
所有脚本共享此模块，无需重复实现。

用法: 被其他脚本 import 使用，不直接运行。
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "https://xpskills.lingdongsz.com/api"

# 获取技能包根目录（ljxp-skills/）
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# HTML 模板路径（技能包内 references/search_results_template.html）
_HTML_TEMPLATE = os.path.join(_SKILL_ROOT, "references", "search_results_template.html")

# 站点信息
VALID_SITES = ["MLM", "MLB", "MLC", "MLA", "MCO"]
SITE_NAMES = {
    "MLM": "墨西哥", "MLB": "巴西", "MLC": "智利",
    "MLA": "阿根廷", "MCO": "哥伦比亚"
}
SITE_CURRENCIES = {
    "MLM": "MXN", "MLB": "BRL", "MLC": "CLP",
    "MLA": "ARS", "MCO": "COP"
}


def get_token(args_token=None):
    """获取 Authorization Token，优先级：命令行参数 > 环境变量 LJXP_TOKEN。
    ⚠️  安全提示：通过 --token <值> 传入会暴露在 shell 历史、进程列表、日志。优先使用环境变量。
    """
    use_cli = bool(args_token)
    token = args_token or os.environ.get("LJXP_TOKEN")
    if not token:
        print("错误: 未提供 Authorization Token！", file=sys.stderr)
        print("", file=sys.stderr)
        print("获取方式:", file=sys.stderr)
        print("  1. [推荐] 设置环境变量: export LJXP_TOKEN=<your_token>", file=sys.stderr)
        print("     (Windows: $env:LJXP_TOKEN=\"<your_token>\" 或 set LJXP_TOKEN=<your_token>)", file=sys.stderr)
        print("  2. 使用 --token 参数传入（⚠️ 不安全，会暴露在 shell 历史/进程列表）", file=sys.stderr)
        print("", file=sys.stderr)
        print("👉 Token 可在蓝鲸选品 Skill 服务页获取: https://xp.lingdongsz.com/#/skillServer", file=sys.stderr)
        sys.exit(1)
    if use_cli:
        print("⚠️  [警告] 当前使用 --token CLI 参数传递 Token。此方式会在 shell 历史、ps 进程列表、共享终端日志中暴露。", file=sys.stderr)
        print("    建议改用环境变量 LJXP_TOKEN 传入以避免泄露。", file=sys.stderr)
    return token


def request_get(path, token, params=None, timeout=60):
    """发送 GET 请求"""
    url = BASE_URL + path
    if params:
        query_parts = []
        for k, v in params.items():
            if v is not None:
                query_parts.append(f"{k}={urllib.request.quote(str(v))}")
        if query_parts:
            url += "?" + "&".join(query_parts)

    headers = {"Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP错误 {e.code}: {e.reason}", file=sys.stderr)
        print(f"响应内容: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"请求异常: {e}", file=sys.stderr)
        sys.exit(1)


def request_post(path, token, body, timeout=60):
    """发送 POST 请求"""
    url = BASE_URL + path
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP错误 {e.code}: {e.reason}", file=sys.stderr)
        print(f"响应内容: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"请求异常: {e}", file=sys.stderr)
        sys.exit(1)


def check_response(response):
    """检查API响应是否成功，失败时输出错误并退出"""
    code = response.get("code")
    if code != 0 and code != 200:
        # 【字段兼容】正常 Response 返回 msg；认证过滤器错误返回 message
        msg = response.get("msg") or response.get("message") or "N/A"
        print(f"API返回错误: code={code}, msg={msg}", file=sys.stderr)
        sys.exit(1)
    return True


def output_json(response):
    """以JSON格式输出响应"""
    print(json.dumps(response, ensure_ascii=False, indent=2))


def print_page_info(data, label="查询结果"):
    """打印分页信息"""
    page_no = data.get("pageNo", 0)
    page_size = data.get("pageSize", 0)
    total = data.get("total", 0)
    cost_time = data.get("costTime", 0)
    total_more = data.get("totalMore", "")

    print(f"\n=== {label} ===")
    total_str = f"总数: {total}"
    if total_more:
        total_str += f" ({total_more})"
    print(f"页码: {page_no} | 每页: {page_size} | {total_str} | 耗时: {cost_time}ms")
    print(f"{'=' * 80}")


def print_item_brief(item, index=1):
    """打印商品简要信息"""
    rating = item.get("rating", {}) or {}
    shipping = item.get("shipping", {}) or {}
    print(f"\n--- 商品 {index} ---")
    print(f"  ID:       {item.get('id', 'N/A')}")
    print(f"  标题:     {item.get('title', 'N/A')}")
    if item.get("titleCn"):
        print(f"  中文:     {item.get('titleCn')}")
    print(f"  价格:     {item.get('price', 'N/A')} {item.get('currencyId', '')}")
    if item.get("priceUsd"):
        print(f"  美元价格: {item.get('priceUsd')} USD")
    print(f"  站点:     {item.get('siteId', 'N/A')}")
    print(f"  状态:     {item.get('itemStatus', 'N/A')}")
    print(f"  店铺:     {item.get('sellerName', 'N/A')} (ID: {item.get('sellerId', 'N/A')})")
    print(f"  店铺类型: {item.get('sellerType', 'N/A')}")
    print(f"  库存:     {item.get('availableQuantity', 'N/A')} | 总销量: {item.get('soldQuantity', 'N/A')}")
    print(f"  7天销量:  {item.get('sale7', 'N/A')} | 30天销量: {item.get('sale30', 'N/A')}")
    print(f"  60天销量: {item.get('sale60', 'N/A')} | 90天销量: {item.get('sale90', 'N/A')}")
    if item.get("gmv30"):
        print(f"  7天GMV:   {item.get('gmv7', 'N/A')} | 30天GMV: {item.get('gmv30', 'N/A')}")
    print(f"  BSR:      {item.get('bsr', 'N/A')} | 评分: {rating.get('stars', 'N/A')} ({rating.get('amount', 0)}评)")
    print(f"  链接:     {item.get('permalink', 'N/A')}")
    if shipping.get("mode"):
        print(f"  物流:     {shipping.get('mode')} | 包邮: {shipping.get('freeShipping')}")


def print_seller_brief(seller, index=1):
    """打印店铺简要信息"""
    address = seller.get("address", {}) or {}
    ratings = seller.get("ratings", {}) or {}
    print(f"\n--- 店铺 {index} ---")
    print(f"  ID:       {seller.get('id', 'N/A')}")
    print(f"  名称:     {seller.get('name', 'N/A')}")
    print(f"  站点:     {seller.get('site_id', 'N/A')}")
    print(f"  类型:     {seller.get('seller_type', 'N/A')} | 等级: {seller.get('level_id', 'N/A')}")
    print(f"  状态:     {seller.get('seller_status', 'N/A')} | 优质卖家: {seller.get('power_seller_status', 'N/A')}")
    print(f"  注册日期: {seller.get('registration_date', 'N/A')}")
    print(f"  地址:     {address.get('city', '')} {address.get('state', '')}")
    print(f"  好评: {ratings.get('positive', 0)} | 中评: {ratings.get('neutral', 0)} | 差评: {ratings.get('negative', 0)}")
    print(f"  商品总数: {seller.get('item_total', 'N/A')} | 销售总数: {seller.get('sale_total', 'N/A')}")
    print(f"  取消率:   {seller.get('cancel60_rate', 'N/A')} | 延迟率: {seller.get('delayed60_rate', 'N/A')} | 投诉率: {seller.get('claims60_rate', 'N/A')}")
    print(f"  SA30: {seller.get('sa30', 'N/A')} | SA60: {seller.get('sa60', 'N/A')} | SA90: {seller.get('sa90', 'N/A')}")
    print(f"  链接:     {seller.get('permalink', 'N/A')}")


def print_keyword_brief(kw, index=1):
    """打印热搜词简要信息"""
    print(f"\n--- 关键词 {index} ---")
    print(f"  关键词:   {kw.get('key', 'N/A')}")
    if kw.get("keyCn"):
        print(f"  中文:     {kw.get('keyCn')}")
    print(f"  类型:     {kw.get('dataType', 'N/A')} | 时间: {kw.get('actionKey', 'N/A')}")
    print(f"  日期范围: {kw.get('fromDate', 'N/A')} ~ {kw.get('toDate', 'N/A')}")
    print(f"  30天访问量: {kw.get('visit30', 'N/A')} | 30天销量: {kw.get('sale30', 'N/A')}")
    print(f"  商品数:   {kw.get('itemCount', 'N/A')} | 历史总商品数: {kw.get('itemTotalCount', 'N/A')}")
    print(f"  曝光量:   {kw.get('viewCount', 'N/A')}")
    cats = kw.get("categoryIds", [])
    if cats:
        print(f"  涉及类目: {', '.join(cats[:5])}")


def output_html(response, search_params, template_path=None):
    """
    将搜索结果渲染为 HTML 文件写入当前工作目录（=用户工作区）。
    ⚠️  不再自动打开浏览器：防止在更丰富的浏览器执行环境中意外暴露敏感业务数据或加载活跃内容。
    ⚠️  文件持久化提醒：此文件含 API 返回数据和搜索参数，用户需知悉并自行决定删除时机。

    Args:
        response: API 返回的完整响应 JSON 对象
        search_params: 用户使用的搜索参数字典
        template_path: HTML 模板路径，默认自动查找 references/search_results_template.html
    """
    template = template_path or _HTML_TEMPLATE

    # 读取模板
    if not os.path.exists(template):
        print(f"警告: HTML 模板未找到 ({template})，回退到 JSON 输出", file=sys.stderr)
        output_json(response)
        return

    with open(template, "r", encoding="utf-8") as f:
        html = f.read()

    # 注入数据
    html = html.replace("__SEARCH_DATA_PLACEHOLDER__",
                        json.dumps(response, ensure_ascii=False))
    html = html.replace("__SEARCH_PARAMS_PLACEHOLDER__",
                        json.dumps(search_params, ensure_ascii=False))

    # 写入临时文件
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", prefix="ljxp_search_",
        encoding="utf-8", delete=False
    )
    tmp.write(html)
    tmp_path = tmp.name
    tmp.close()

    # 在浏览器中打开
    print(f"正在浏览器中打开结果页面...", file=sys.stderr)
    print(f"文件: {tmp_path}", file=sys.stderr)
    webbrowser.open("file://" + tmp_path)
