#!/usr/bin/env python3
"""
麦当劳点餐辅助脚本
用法:
  python3 order_helper.py check-config
  python3 order_helper.py format-order-summary --items '<json>' --price '<json>' --address '<json>'
  python3 order_helper.py load-default-meal --time-slot breakfast|lunch|dinner
  python3 order_helper.py calorie-pairing --menu '<data_json>' --nutrition-text '<markdown>' --time-slot breakfast|lunch|dinner
  python3 order_helper.py gen-pay-qr --pay-url '<scanToPay_url>'
"""

import sys
import os
import json
import argparse
import re


def cmd_check_config(args):
    """检查 MCD_MCP_TOKEN 是否已配置"""
    token = os.environ.get("MCD_MCP_TOKEN", "").strip()
    if token:
        print(json.dumps({"ok": True}))
        return

    steps = [
        "1. 访问 https://open.mcd.cn 并登录您的麦当劳账户",
        "2. 进入「开发者控制台」→「我的应用」",
        "3. 创建或选择已有应用，进入「API 密钥」页面",
        "4. 点击「激活」或「生成 Token」，复制生成的 Token",
        "5. 在终端或 OpenClaw 配置中设置环境变量：",
        "   export MCD_MCP_TOKEN='your_token_here'",
        "   或在 openclaw.json 的 skills.entries.mcd_order_skill.env 中配置 MCD_MCP_TOKEN",
    ]
    print(json.dumps({"ok": False, "steps": steps}, ensure_ascii=False))


def _parse_json_arg(value, name):
    """解析 JSON 参数，出错时输出到 stderr"""
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        print(f"错误：{name} 不是有效的 JSON：{e}", file=sys.stderr)
        sys.exit(1)


def cmd_format_order_summary(args):
    """将订单信息格式化为人类可读的确认摘要"""
    items = _parse_json_arg(args.items, "--items")
    price_info = _parse_json_arg(args.price, "--price")
    address = _parse_json_arg(args.address, "--address")

    lines = []
    lines.append("=" * 40)
    lines.append("📋  订单确认单")
    lines.append("=" * 40)

    # 配送地址
    lines.append("")
    lines.append("📍 配送地址")
    if isinstance(address, dict):
        full = address.get("fullAddress", "").strip()
        if full:
            addr_line = full
        else:
            addr_parts = []
            for key in ("province", "city", "district", "street", "detail", "address"):
                val = address.get(key, "").strip()
                if val:
                    addr_parts.append(val)
            addr_line = " ".join(addr_parts)
        if addr_line:
            lines.append("   " + addr_line)
        name = address.get("contactName") or address.get("name") or address.get("contact_name", "")
        phone = address.get("phone") or address.get("contact_phone", "")
        if name or phone:
            lines.append(f"   收件人：{name}  {phone}".strip())
    else:
        lines.append(f"   {address}")

    # 购物车明细
    lines.append("")
    lines.append("🛒 购物清单")
    if isinstance(items, list):
        subtotal = 0.0
        for item in items:
            name = item.get("name", item.get("meal_name", "未知商品"))
            qty = int(item.get("quantity", 1))
            price = float(item.get("price", 0))
            item_total = price * qty
            subtotal += item_total
            lines.append(f"   {name} × {qty}  ¥{item_total:.2f}")
        lines.append(f"   {'─' * 28}")
        lines.append(f"   小计：¥{subtotal:.2f}")
    else:
        lines.append(f"   {items}")

    # 价格明细
    lines.append("")
    lines.append("💰 价格明细")
    if isinstance(price_info, dict):
        subtotal = price_info.get("subtotal") or price_info.get("items_total", "")
        delivery_fee = price_info.get("delivery_fee", "")
        discount = price_info.get("discount") or price_info.get("coupon_discount", "")
        total = price_info.get("total") or price_info.get("final_price", "")

        if subtotal != "":
            lines.append(f"   商品金额：¥{float(subtotal):.2f}")
        if delivery_fee != "":
            lines.append(f"   配送费：  ¥{float(delivery_fee):.2f}")
        if discount not in ("", None, 0, 0.0):
            lines.append(f"   优惠减免：-¥{float(discount):.2f}")
        if total != "":
            lines.append(f"   {'─' * 28}")
            lines.append(f"   实付金额：¥{float(total):.2f}")

        coupon_name = price_info.get("coupon_name") or price_info.get("applied_coupon", "")
        if coupon_name:
            lines.append(f"   （已使用优惠券：{coupon_name}）")
    else:
        lines.append(f"   {price_info}")

    lines.append("")
    lines.append("=" * 40)

    print("\n".join(lines))


def _get_time_slot(hour: int) -> str:
    """根据小时数返回时段名称"""
    if 6 <= hour <= 10:
        return "breakfast"
    if 11 <= hour <= 14:
        return "lunch"
    if hour in (15, 16):
        return "lunch"
    if 17 <= hour <= 21:
        return "dinner"
    return "dinner"  # 22+ 或 0-5


def _load_config() -> dict:
    """加载 config.json（相对 order_helper.py 的父目录）"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_nutrition_markdown(text: str) -> dict:
    """
    从 list-nutrition-foods 返回的 Markdown 文本中提取 {菜品名: kcal} 字典。
    扫描 ## 标题行，然后找含「热量」的行中的第一个数字。
    """
    result = {}
    current_food = None
    for line in text.splitlines():
        # 匹配 ## 菜品名
        m = re.match(r"^#{1,3}\s+(.+)", line)
        if m:
            current_food = m.group(1).strip()
            continue
        # 匹配含「热量」的行，提取第一个整数
        if current_food and "热量" in line:
            nums = re.findall(r"\d+", line)
            if nums:
                result[current_food] = int(nums[0])
                current_food = None  # 已找到该菜品热量，重置
    return result


def _find_meal_by_name(name: str, meals_map: dict) -> dict | None:
    """在菜单中按名称查找菜品：先精确匹配，再模糊匹配（互相包含）"""
    # 精确匹配
    for code, info in meals_map.items():
        if info.get("name", "") == name:
            return {"code": code, **info}
    # 模糊匹配
    for code, info in meals_map.items():
        meal_name = info.get("name", "")
        if name in meal_name or meal_name in name:
            return {"code": code, **info}
    return None


def cmd_load_default_meal(args):
    """读取 config.json 中对应时段的默认套餐，通过菜品名在菜单中匹配 productCode"""
    slot = args.time_slot
    config = _load_config()
    default_meals = config.get("default_meals", {})
    if slot not in default_meals:
        print(json.dumps({"ok": False, "error": f"未知时段: {slot}"}, ensure_ascii=False))
        sys.exit(1)

    entry = default_meals[slot]

    # 无菜单数据时，只返回名称（价格/code 待后续补全）
    if not args.menu:
        cart = [{"name": item["name"], "quantity": item["quantity"], "price": 0}
                for item in entry["items"]]
        print(json.dumps({"ok": True, "slot": slot, "label": entry["label"],
                          "cart": cart, "resolved": False}, ensure_ascii=False))
        return

    menu_data = _parse_json_arg(args.menu, "--menu")
    meals_map = menu_data.get("meals", {}) if isinstance(menu_data, dict) else {}

    cart = []
    not_found = []
    for item in entry["items"]:
        matched = _find_meal_by_name(item["name"], meals_map)
        if matched:
            cart.append({
                "productCode": matched["code"],
                "code": matched["code"],
                "name": matched.get("name", item["name"]),
                "quantity": item["quantity"],
                "price": matched.get("currentPrice", 0),
            })
        else:
            not_found.append(item["name"])

    if not_found:
        print(json.dumps({
            "ok": False,
            "not_found": not_found,
            "error": f"以下菜品在当前门店未找到：{'、'.join(not_found)}，请在 config.json 中更新菜品名称",
        }, ensure_ascii=False))
        return

    print(json.dumps({
        "ok": True,
        "slot": slot,
        "label": entry["label"],
        "cart": cart,
        "resolved": True,
    }, ensure_ascii=False))


def cmd_calorie_pairing(args):
    """根据菜单和营养数据，按热量目标自动搭配购物车"""
    menu_data = _parse_json_arg(args.menu, "--menu")
    nutrition_text = args.nutrition_text
    slot = args.time_slot

    config = _load_config()
    calorie_fallback = config.get("calorie_fallback", {})
    calorie_targets = config.get("calorie_targets", {})

    target = calorie_targets.get(slot, {"min": 600, "max": 900})
    target_mid = (target["min"] + target["max"]) / 2

    # 解析营养热量数据
    nutrition = _parse_nutrition_markdown(nutrition_text)

    def get_kcal(name: str) -> int:
        """查热量：先用精确匹配，再按关键字模糊匹配 fallback"""
        if name in nutrition:
            return nutrition[name]
        for key, val in nutrition.items():
            if key in name or name in key:
                return val
        # 兜底 fallback
        for key, val in calorie_fallback.items():
            if key in name or name in key:
                return val
        return 0

    # 从菜单提取菜品列表
    categories = menu_data.get("categories", []) if isinstance(menu_data, dict) else []
    meals_map = menu_data.get("meals", {}) if isinstance(menu_data, dict) else {}

    skip_words = {"圣代", "甜筒", "麦旋风", "派", "薯条", "薯饼", "冰淇淋", "蛋挞", "苹果片"}
    burger_kws = {"堡", "鸡排", "鸡腿汉堡", "麦香鸡", "酥酥多笋卷"}

    burgers = []
    optionals = []
    drink_code = "903071"

    seen_codes = set()
    for cat in categories:
        for m in cat.get("meals", []):
            code = m["code"]
            if code in seen_codes:
                continue
            seen_codes.add(code)
            info = meals_map.get(code, {})
            name = info.get("name", code)

            # 跳过不适合的品类
            if any(sw in name for sw in skip_words):
                continue

            kcal = get_kcal(name)
            entry = {"productCode": code, "name": name,
                     "price": info.get("currentPrice", 0), "quantity": 1, "kcal": kcal}

            if code == drink_code:
                continue  # 饮品单独处理
            if any(kw in name for kw in burger_kws):
                burgers.append(entry)
            elif "麦乐鸡" in name or "鸡翅" in name:
                optionals.append(entry)

    if not burgers:
        print(json.dumps({
            "ok": False,
            "error": "当前门店菜单中未找到汉堡类菜品，建议使用自由选菜模式",
        }, ensure_ascii=False))
        return

    # 选热量最接近 target_mid×0.6 的汉堡（主食占约 60% 热量）
    burger_target = target_mid * 0.6
    burgers.sort(key=lambda x: abs(x["kcal"] - burger_target) if x["kcal"] > 0 else float("inf"))
    chosen_burger = burgers[0]

    cart = [{"productCode": chosen_burger["productCode"], "name": chosen_burger["name"],
             "price": chosen_burger["price"], "quantity": 1}]
    total_kcal = chosen_burger["kcal"]

    # 加无糖可乐（若菜单有）
    coke_info = meals_map.get(drink_code, {})
    coke_kcal = get_kcal(coke_info.get("name", "无糖可口可乐中杯")) if coke_info else calorie_fallback.get("无糖可口可乐中杯", 3)
    if coke_info or True:  # 无论如何都尝试加可乐（默认套餐已验证 code 有效）
        cart.append({"productCode": drink_code, "name": coke_info.get("name", "无糖可口可乐中杯"),
                     "price": coke_info.get("currentPrice", 0), "quantity": 1})
        total_kcal += coke_kcal

    # 尝试加一种可选品（不超热量上限）
    for opt in optionals:
        if opt["kcal"] > 0 and total_kcal + opt["kcal"] <= target["max"]:
            cart.append({"productCode": opt["productCode"], "name": opt["name"],
                         "price": opt["price"], "quantity": 1})
            total_kcal += opt["kcal"]
            break

    in_range = target["min"] <= total_kcal <= target["max"]
    range_note = "" if in_range else "（略超目标，可根据需要调整）"
    items_display = " + ".join(item["name"] for item in cart)
    display = (
        f"{'早餐' if slot=='breakfast' else '午餐' if slot=='lunch' else '晚餐'}热量搭配：{items_display}\n"
        f"预计热量：{total_kcal} kcal（目标 {target['min']}~{target['max']} kcal）{range_note}"
    )

    print(json.dumps({
        "ok": True,
        "cart": cart,
        "total_kcal": total_kcal,
        "in_range": in_range,
        "display": display,
    }, ensure_ascii=False))


def cmd_gen_pay_qr(args):
    """将 scanToPay URL 转换为 jumpToApp URL 并生成支付二维码 PNG"""
    raw_url = args.pay_url.strip()

    # URL 转换：scanToPay?orderId=XXX → jumpToApp/?orderId=XXX
    pay_url = re.sub(r'/scanToPay\?', '/jumpToApp/?', raw_url)

    # 提取订单号用于文件命名
    m = re.search(r'orderId=(\w+)', pay_url)
    order_id = m.group(1) if m else "unknown"

    try:
        import qrcode
    except ImportError:
        print(json.dumps({
            "ok": False,
            "error": "缺少依赖，请运行：pip3 install 'qrcode[pil]'",
        }, ensure_ascii=False))
        sys.exit(1)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(pay_url)
    qr.make(fit=True)

    try:
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"/tmp/mcd_pay_{order_id}.png"
        img.save(qr_path)
        print(json.dumps({
            "ok": True,
            "pay_url": pay_url,
            "qr_path": qr_path,
            "mode": "image",
        }, ensure_ascii=False))
    except Exception:
        # Pillow 不可用时降级为 ASCII 二维码
        import io
        buf = io.StringIO()
        qr.print_ascii(out=buf)
        print(json.dumps({
            "ok": True,
            "pay_url": pay_url,
            "ascii_qr": buf.getvalue(),
            "mode": "ascii",
        }, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="麦当劳点餐辅助脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check-config
    subparsers.add_parser("check-config", help="检查 MCD_MCP_TOKEN 是否已配置")

    # format-order-summary
    fs_parser = subparsers.add_parser("format-order-summary", help="格式化订单确认摘要")
    fs_parser.add_argument("--items", required=True, help="购物车商品列表（JSON array）")
    fs_parser.add_argument("--price", required=True, help="calculate-price 返回值（JSON object）")
    fs_parser.add_argument("--address", required=True, help="选中的配送地址（JSON object）")

    # load-default-meal
    ldm_parser = subparsers.add_parser("load-default-meal", help="按时段读取默认套餐")
    ldm_parser.add_argument("--time-slot", required=True,
                            choices=["breakfast", "lunch", "dinner"],
                            help="时段：breakfast / lunch / dinner")
    ldm_parser.add_argument("--menu", default=None,
                            help="query-meals 返回的 data 部分（JSON），用于按名称匹配 productCode")

    # calorie-pairing
    cp_parser = subparsers.add_parser("calorie-pairing", help="按热量目标从菜单自动搭配套餐")
    cp_parser.add_argument("--menu", required=True, help="query-meals 返回的 data 部分（JSON）")
    cp_parser.add_argument("--nutrition-text", required=True, help="list-nutrition-foods 原始文本（Markdown）")
    cp_parser.add_argument("--time-slot", required=True,
                           choices=["breakfast", "lunch", "dinner"],
                           help="时段：breakfast / lunch / dinner")

    # gen-pay-qr
    gq_parser = subparsers.add_parser("gen-pay-qr", help="将支付 URL 转换并生成二维码")
    gq_parser.add_argument("--pay-url", required=True, help="create-order 返回的 payUrl（scanToPay 格式）")

    args = parser.parse_args()

    if args.command == "check-config":
        cmd_check_config(args)
    elif args.command == "format-order-summary":
        cmd_format_order_summary(args)
    elif args.command == "load-default-meal":
        cmd_load_default_meal(args)
    elif args.command == "calorie-pairing":
        cmd_calorie_pairing(args)
    elif args.command == "gen-pay-qr":
        cmd_gen_pay_qr(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
