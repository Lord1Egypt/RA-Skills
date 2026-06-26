#!/usr/bin/env python3
"""
OWS - 初始化卖家配置
"""

import json
import pathlib

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"

def init_seller_config():
    """初始化卖家配置"""
    config_file = STATE_DIR / "seller_config.json"
    
    if config_file.exists():
        print("✅ 卖家配置已存在")
        return
    
    config = {
        "seller_id": input("卖家 ID (如 seller-xxx): ").strip() or "seller-demo",
        "seller_name": input("店铺名称: ").strip() or "演示卖家",
        "contact": input("联系方式: ").strip() or "客服微信: demo",
        "products": [],
        "credentials": [],
        "logistics": {
            "methods": ["顺丰快递"],
            "regions": ["全国"]
        },
        "reputation": {
            "total_transactions": 0,
            "success_rate": 1.0,
            "disputes": 0,
            "platform_verified": False
        }
    }
    
    # 添加商品
    while True:
        add_product = input("\n添加商品？(y/n): ").strip().lower()
        if add_product != 'y':
            break
        
        product = {
            "name": input("  商品名称: ").strip(),
            "category": input("  商品类别: ").strip(),
            "cost": float(input("  成本价: ").strip() or "0"),
            "stock": int(input("  库存数量: ").strip() or "0")
        }
        config["products"].append(product)
    
    # 保存
    config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    print(f"\n✅ 配置已保存到 {config_file}")

if __name__ == "__main__":
    init_seller_config()