#!/usr/bin/env python3
"""
OWS 产品清单管理
添加、编辑、删除产品
"""

import json
import pathlib
import sys
from datetime import datetime
from typing import Dict, List, Optional

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"
CATALOG_FILE = STATE_DIR / "product_catalog.json"
MATCHES_DIR = STATE_DIR / "matches"

def load_catalog() -> Dict:
    """加载产品清单"""
    if CATALOG_FILE.exists():
        return json.loads(CATALOG_FILE.read_text())
    return {
        "seller_id": "seller-demo",
        "seller_name": "演示卖家",
        "products": [],
        "auto_match": {
            "enabled": True,
            "scan_interval_minutes": 30,
            "price_match_tolerance": 0.3,
            "keywords_weight": 0.6,
            "category_weight": 0.4,
            "min_match_score": 0.5
        }
    }

def save_catalog(catalog: Dict):
    """保存产品清单"""
    CATALOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))

def add_product(product: Dict) -> Dict:
    """添加产品"""
    catalog = load_catalog()
    
    # 生成产品ID
    if "product_id" not in product:
        product["product_id"] = f"PROD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # 设置默认值
    product.setdefault("active", True)
    product.setdefault("keywords", [])
    product.setdefault("price_range", [0, 999999])
    product.setdefault("stock", 0)
    product.setdefault("auth_docs", [])
    product.setdefault("shop_links", [])
    
    catalog["products"].append(product)
    save_catalog(catalog)
    
    return product

def update_product(product_id: str, updates: Dict) -> Optional[Dict]:
    """更新产品"""
    catalog = load_catalog()
    
    for product in catalog["products"]:
        if product["product_id"] == product_id:
            product.update(updates)
            save_catalog(catalog)
            return product
    
    return None

def remove_product(product_id: str) -> bool:
    """删除产品"""
    catalog = load_catalog()
    
    for i, product in enumerate(catalog["products"]):
        if product["product_id"] == product_id:
            catalog["products"].pop(i)
            save_catalog(catalog)
            return True
    
    return False

def list_products(active_only: bool = True) -> List[Dict]:
    """列出所有产品"""
    catalog = load_catalog()
    products = catalog.get("products", [])
    
    if active_only:
        products = [p for p in products if p.get("active", True)]
    
    return products

def get_product(product_id: str) -> Optional[Dict]:
    """获取单个产品"""
    catalog = load_catalog()
    
    for product in catalog["products"]:
        if product["product_id"] == product_id:
            return product
    
    return None

def configure_auto_match(config: Dict) -> Dict:
    """配置自动匹配参数"""
    catalog = load_catalog()
    catalog["auto_match"].update(config)
    save_catalog(catalog)
    return catalog["auto_match"]

def format_product(product: Dict) -> str:
    """格式化产品信息"""
    output = f"""
📦 产品ID: {product.get('product_id', 'N/A')}
   名称: {product.get('name', 'N/A')}
   类别: {product.get('category', 'N/A')}
   品牌: {product.get('brand', 'N/A')}
   关键词: {', '.join(product.get('keywords', []))}
   价格区间: ¥{product.get('price_range', [0, 0])[0]} - ¥{product.get('price_range', [0, 0])[1]}
   库存: {product.get('stock', 0)}
   状态: {'✅ 在售' if product.get('active', True) else '❌ 下架'}
"""
    return output

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="OWS 产品清单管理")
    parser.add_argument("action", choices=["list", "add", "update", "remove", "config", "show"])
    parser.add_argument("--product-id", help="产品ID")
    parser.add_argument("--name", help="产品名称")
    parser.add_argument("--category", help="产品类别")
    parser.add_argument("--keywords", help="关键词（逗号分隔）")
    parser.add_argument("--price-min", type=float, help="最低价格")
    parser.add_argument("--price-max", type=float, help="最高价格")
    parser.add_argument("--stock", type=int, help="库存数量")
    parser.add_argument("--active", type=lambda x: x.lower() == 'true', help="是否在售")
    parser.add_argument("--scan-interval", type=int, help="扫描间隔（分钟）")
    
    args = parser.parse_args()
    
    if args.action == "list":
        products = list_products()
        print(f"📦 产品清单 ({len(products)} 个产品)\n")
        for p in products:
            print(format_product(p))
    
    elif args.action == "add":
        product = {}
        if args.name:
            product["name"] = args.name
        if args.category:
            product["category"] = args.category
        if args.keywords:
            product["keywords"] = args.keywords.split(",")
        if args.price_min is not None and args.price_max is not None:
            product["price_range"] = [args.price_min, args.price_max]
        if args.stock is not None:
            product["stock"] = args.stock
        if args.active is not None:
            product["active"] = args.active
        
        result = add_product(product)
        print(f"✅ 产品已添加\n{format_product(result)}")
    
    elif args.action == "update":
        if not args.product_id:
            print("❌ 请指定 --product-id")
            return
        
        updates = {}
        if args.name:
            updates["name"] = args.name
        if args.category:
            updates["category"] = args.category
        if args.keywords:
            updates["keywords"] = args.keywords.split(",")
        if args.price_min is not None and args.price_max is not None:
            updates["price_range"] = [args.price_min, args.price_max]
        if args.stock is not None:
            updates["stock"] = args.stock
        if args.active is not None:
            updates["active"] = args.active
        
        result = update_product(args.product_id, updates)
        if result:
            print(f"✅ 产品已更新\n{format_product(result)}")
        else:
            print(f"❌ 产品不存在: {args.product_id}")
    
    elif args.action == "remove":
        if not args.product_id:
            print("❌ 请指定 --product-id")
            return
        
        if remove_product(args.product_id):
            print(f"✅ 产品已删除: {args.product_id}")
        else:
            print(f"❌ 产品不存在: {args.product_id}")
    
    elif args.action == "config":
        config = {}
        if args.scan_interval is not None:
            config["scan_interval_minutes"] = args.scan_interval
        
        if config:
            result = configure_auto_match(config)
            print("✅ 配置已更新:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            catalog = load_catalog()
            print("当前配置:")
            print(json.dumps(catalog.get("auto_match", {}), indent=2, ensure_ascii=False))
    
    elif args.action == "show":
        if not args.product_id:
            print("❌ 请指定 --product-id")
            return
        
        product = get_product(args.product_id)
        if product:
            print(format_product(product))
        else:
            print(f"❌ 产品不存在: {args.product_id}")

if __name__ == "__main__":
    main()