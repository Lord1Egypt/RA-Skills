#!/usr/bin/env python3
"""拼多多热销榜 - list"""

import os
import sys
import json
import urllib.request
import urllib.error

PROXY_URL = os.environ.get("PROXY_URL", "https://1439498936-cv2nww3ykf.ap-guangzhou.tencentscf.com")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "tp_8k2mX9vQ4z")
TIMEOUT = 30


def _call_proxy(tool_name, params):
    """调用SCF代理 - type+params格式"""
    body = json.dumps({"type": tool_name, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=body, method="POST",
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"ok": False, "error": "proxy error {}: {}".format(e.code, err)}
    except Exception as e:
        return {"ok": False, "error": "request error: {}".format(e)}


def _format_list(data):
    """格式化好货列表"""
    if not data.get("ok"):
        return "查询失败：" + data.get("error", "未知错误")
    items = data.get("data", [])
    if not items:
        return "暂无商品，请稍后再试"
    total = data.get("total", len(items))
    lines = ["拼多多热销榜，共 {} 件好货：\n".format(total)]
    for i, item in enumerate(items, 1):
        name = item.get("goods_name", "")
        final_price = item.get("final_price", 0)
        min_group_price = item.get("min_group_price", 0)
        coupon_discount = item.get("coupon_discount", 0)
        has_coupon = item.get("has_coupon", False)
        sales = item.get("sales_tip", "")
        mall = item.get("mall_name", "")
        category = item.get("category_name", "")
        goods_sign = item.get("goods_sign", "")
        image = item.get("goods_image_url", "")

        if coupon_discount > 0 and has_coupon:
            price_str = "到手价¥{}（拼团价¥{} - 券¥{}）".format(final_price, min_group_price, coupon_discount)
        else:
            price_str = "¥{}".format(min_group_price)

        coupon_tag = " | 有券" if has_coupon else ""
        sales_str = " | 销量{}".format(sales) if sales else ""
        mall_str = " | {}".format(mall) if mall else ""
        cat_str = " | {}".format(category) if category else ""

        line = "{}. {}{}{}\n   {}{}{}\n   goods_sign: {}".format(
            i, name, coupon_tag, sales_str, price_str, mall_str, cat_str, goods_sign)
        if image:
            line += "\n   图片: {}".format(image)
        lines.append(line)
    lines.append("\n> 数据来源：拼多多热销榜")
    return "\n\n".join(lines)


def tool_list(params):
    keyword = params.get("keyword", "")
    page = params.get("page", 1)
    sort = params.get("sort", 0)

    p = {"page": page, "sort": sort}
    if keyword:
        p["keyword"] = keyword
    if params.get("max_price") is not None:
        p["max_price"] = params["max_price"]
    if params.get("min_price") is not None:
        p["min_price"] = params["min_price"]
    if params.get("brand_only") is not None:
        p["brand_only"] = params["brand_only"]

    data = _call_proxy("list", p)
    return json.dumps({"content": _format_list(data)}, ensure_ascii=False)


TOOLS = {
    "list": tool_list,
}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "参数JSON解析失败: {}".format(e)}, ensure_ascii=False))
        sys.exit(1)

    if tool not in TOOLS:
        print(json.dumps({"error": "未知工具: {}，可用工具: {}".format(tool, ", ".join(TOOLS.keys()))}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool](args)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
