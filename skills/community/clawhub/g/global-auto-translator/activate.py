#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
激活脚本 - 付费解锁 Premium 功能
支持支付宝/微信支付
"""

import os
import sys
import json
import time
import hashlib

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.expanduser("~/.openclaw/global-auto-translator")
LICENSE_PATH = os.path.join(CONFIG_DIR, "license.json")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

# ==================== 支付配置（卖家修改这里）====================
PAYMENT_CONFIG = {
    # 价格设置（人民币）
    "price_cny": 29.9,
    "price_description": "终身使用，无订阅费",

    # 收款方式（选一种或多种）
    "methods": [
        {
            "name": "支付宝",
            "enabled": True,
            "qr_image": os.path.join(SKILL_DIR, "alipay_qr.jpg"),
            "guide": "扫码支付 ¥29.90，付款后备注 'AutoTranslator'",
        },
        {
            "name": "微信",
            "enabled": True,
            "qr_image": os.path.join(SKILL_DIR, "wechat_qr.jpg"),
            "guide": "扫码支付 ¥29.90，付款后备注 'AutoTranslator'",
        },
    ],

    # 联系方式（付款后发送激活码）
    "contact": "微信号: NewWave_CN",

    # 备注说明
    "note": "付款后发送截图联系卖家，5分钟内收到激活码",
}

# ==================== 激活码库 ====================
# 格式: "哈希前16位": {"owner": "用户标识", "used": False}
VALID_KEYS = {
    "5100e4c455773f0b": {"owner": "测试用户001", "used": False},
}


def show_payment_guide():
    """显示支付引导"""
    config = PAYMENT_CONFIG
    price = config["price_cny"]
    desc = config["price_description"]

    print("=" * 50)
    print("  Global Auto Translator - Premium 激活")
    print("=" * 50)
    print()
    print("价格: ¥%.2f CNY (%s)" % (price, desc))
    print()
    print("Premium 功能:")
    print("  ✅ DeepL Pro 高精度翻译")
    print("  ✅ 批量文档翻译无限制")
    print("  ✅ 无速率限制")
    print("  ✅ 优先技术支持")
    print()

    for method in config["methods"]:
        if not method["enabled"]:
            continue
        name = method["name"]
        if name == "支付宝":
            print("💳 %s支付" % name)
        else:
            print("💳 %s支付" % name)

        if method.get("qr_image"):
            print("  扫码支付: %s" % method["qr_image"])
        elif method.get("account"):
            print("  转账到: %s" % method["account"])
        else:
            print("  联系 %s 获取收款码" % config.get("contact", "卖家"))

        if method.get("guide"):
            print("  %s" % method["guide"])
        print()

    print("📩 联系方式")
    print("  %s" % config.get("contact", ""))
    print()
    print(config.get("note", ""))
    print()
    print("-" * 50)
    print("收到激活码后，运行:")
    print("  python3 activate.py --key YOUR_KEY")
    print("-" * 50)


def generate_key(owner=""):
    """生成新的激活码（供发行方使用）"""
    import secrets
    key = secrets.token_urlsafe(12)
    key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
    VALID_KEYS[key_hash] = {"owner": owner, "used": False}
    print("=" * 50)
    print("  新激活码已生成")
    print("=" * 50)
    print()
    print("激活码: %s" % key)
    print("哈希: %s" % key_hash)
    print("拥有者: %s" % (owner or "未指定"))
    print()
    print("请将以下条目添加到 activate.py 的 VALID_KEYS 中:")
    print('"%s": {"owner": "%s", "used": False},' % (key_hash, owner))


def verify_key(key):
    """验证激活码"""
    key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
    if key_hash in VALID_KEYS:
        key_info = VALID_KEYS[key_hash]
        return key_info, key_hash
    return None, None


def activate(key, force=False):
    """激活 Premium 功能"""
    key_info, key_hash = verify_key(key)
    if key_info is None:
        print("❌ 激活码无效，请检查后重试")
        print()
        print("如需购买:")
        show_payment_guide()
        return False

    if not force:
        if os.path.exists(LICENSE_PATH):
            with open(LICENSE_PATH) as f:
                existing = json.load(f)
            if existing.get("activated"):
                print("⚠️ 已经激活过了（用户: %s）" % existing.get("owner", ""))
                print("如需重新激活，请删除 %s 后重试" % LICENSE_PATH)
                return False

    license_data = {
        "activated": True,
        "owner": key_info.get("owner", ""),
        "key_hash": key_hash,
        "activated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tier": "premium",
        "features": [
            "deepL_pro",
            "batch_translate",
            "no_rate_limit",
            "priority_support"
        ]
    }
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(LICENSE_PATH, "w") as f:
        json.dump(license_data, f, indent=2, ensure_ascii=False)

    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                config = json.load(f)
        except Exception:
            config = {}
    else:
        config = {}

    config["premium_enabled"] = True
    config["translation_service"] = "deepl"
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("✅ 激活成功!")
    print("  用户: %s" % key_info.get("owner", ""))
    print("  等级: Premium")
    print("  激活时间: %s" % license_data["activated_at"])
    print()
    print("已解锁功能:")
    for feat in license_data["features"]:
        print("  ✅ %s" % feat)
    print()
    print("下一步: 请在 config.json 中填入你的 DeepL Pro API Key")
    print('  "deepl_api_key": "你的DeepL Pro API Key"')
    return True


def check_status():
    """检查激活状态"""
    if not os.path.exists(LICENSE_PATH):
        print("状态: 未激活 (免费版)")
        print()
        print("可用功能:")
        print("  ✅ MyMemory 免费翻译")
        print("  ✅ 剪贴板智能监控")
        print("  ✅ 外贸术语库")
        print()
        print("Premium 功能 (需激活):")
        print("  🔒 DeepL Pro 高精度翻译")
        print("  🔒 批量文档翻译")
        print("  🔒 无速率限制")
        print("  🔒 优先技术支持")
        print()
        print("购买 Premium:")
        show_payment_guide()
        return

    with open(LICENSE_PATH) as f:
        license_data = json.load(f)

    if license_data.get("activated"):
        print("状态: ✅ 已激活 (Premium)")
        print("  用户: %s" % license_data.get("owner", ""))
        print("  激活时间: %s" % license_data.get("activated_at", ""))
        print("  可用功能:")
        for feat in license_data.get("features", []):
            print("    ✅ %s" % feat)
    else:
        print("状态: 未激活")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--generate":
        owner = sys.argv[2] if len(sys.argv) > 2 else ""
        generate_key(owner)
    elif len(sys.argv) > 1 and sys.argv[1] == "--buy":
        print("购买 Premium 激活码:")
        show_payment_guide()
    elif len(sys.argv) > 1 and sys.argv[1] == "--key":
        if len(sys.argv) < 3:
            print("用法: python3 activate.py --key YOUR_KEY")
            sys.exit(1)
        force = "--force" in sys.argv
        if not activate(sys.argv[2], force):
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "--status":
        check_status()
    else:
        print("Global Auto Translator - Premium 激活工具")
        print()
        print("用法:")
        print("  python3 activate.py --buy               查看购买方式")
        print("  python3 activate.py --key YOUR_KEY      激活 Premium")
        print("  python3 activate.py --status            查看激活状态")
        print("  python3 activate.py --generate [user]   生成新激活码（发行方）")


if __name__ == "__main__":
    main()
