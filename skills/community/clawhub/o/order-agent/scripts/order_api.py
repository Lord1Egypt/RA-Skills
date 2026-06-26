#!/usr/bin/env python3
"""
WMS 订单处理脚本 - 调用真实后端API
"""
import json
import argparse
import requests
from typing import Dict, Any, Optional, List

# 后端 API 配置
BASE_URL = "https://aifx.tushu.cloud/prod-api/dispatch"

# 超时设置（查询接口较慢，设置120秒）
TIMEOUT = 120


def query_goods(
    book_name: Optional[str] = None,
    isbn: Optional[str] = None,
    stock_id: Optional[int] = None,
    page_num: int = 1,
    page_size: int = 20
) -> Dict[str, Any]:
    """
    查询商品信息
    """
    url = f"{BASE_URL}/goods/queryGoods"
    
    payload = {
        "pageNum": page_num,
        "pageSize": page_size
    }
    
    if book_name:
        payload["bookName"] = book_name
    if isbn:
        payload["isbn"] = isbn
    if stock_id:
        payload["stockId"] = stock_id
    
    try:
        response = requests.post(url, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, dict):
            if result.get("code") == 200 or result.get("success"):
                return {
                    "success": True,
                    "data": result.get("data", []),
                    "message": "查询成功"
                }
            else:
                return {
                    "success": False,
                    "message": result.get("msg", "查询失败"),
                    "data": []
                }
        return {"success": True, "data": result}
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"请求失败: {str(e)}",
            "data": []
        }


def create_order(
    # ============ 订单基础信息 (shopOrder) ============
    name: str,                    # 收货人姓名
    phone: str,                   # 收货人手机号
    province: str,                # 省份
    city: str,                    # 城市
    district: str,                # 区/县
    detail: str,                  # 详细地址
    # 可选参数
    countryside_name: str = "",    # 乡镇/街道
    town: str = "",               # 镇
    remark: str = "",             # 订单备注
    buyer_remark: str = "",       # 买家留言
    seller_message: str = "",     # 卖家备注
    order_source: int = 15,       # 订单来源: 1淘宝 2京东 3天猫 4苏宁 5拼多多 6转转 7孔夫子 9当当 10快手 12真快乐 13抖音 15线下
    shop_name: str = "",          # 店铺名称
    warehouse_id: int = 0,        # 仓库ID
    shop_num: str = "",           # 店铺编号
    session_key: str = "",        # 店铺Key
    # ============ 订单商品列表 (orderInfoList) ============
    book_name: str = "",          # 书名
    buy_count: int = 1,           # 购买数量
    stock_id: int = 0,           # 库存ID（必填）
    stock_name: str = "",         # 库存名称
    isbn: str = "",               # ISBN
    product_name: str = "",       # 产品名称
    product_code: str = "",       # 货号
    img: str = "",               # 图片URL
    sale_price: float = 0.0,      # 售价
    wholesale_price: float = 0.0, # 批发价/供货价
    author: str = "",             # 作者
    press: str = "",             # 出版社
    make_price: float = 0.0,      # 制作价格
) -> Dict[str, Any]:
    """
    创建订单
    """
    url = f"{BASE_URL}/order/createOrder"
    
    # 构建订单基础信息
    shop_order = {
        "name": name,
        "phone": phone,
        "province": province,
        "city": city,
        "district": district,
        "countrysideName": countryside_name,
        "town": town,
        "detail": detail,
        "remark": remark,
        "buyerRemark": buyer_remark,
        "sellerMessage": seller_message,
        "orderSource": order_source,
        "shopName": shop_name,
        "warehouseId": warehouse_id,
        "shopNum": shop_num,
        "sessionKey": session_key,
        "initOrderNum": "",  # 原始订单号
    }
    
    # 构建商品详情
    order_info = {
        "bookName": book_name,
        "buyCount": buy_count,
        "stockId": stock_id,
        "stockName": stock_name,
        "isbn": isbn,
        "productName": product_name,
        "productCode": product_code,
        "img": img,
        "salePrice": sale_price,
        "wholesalePrice": wholesale_price,
        "author": author,
        "press": press,
        "makePrice": make_price,
    }
    
    payload = {
        "shopOrder": shop_order,
        "orderInfoList": [order_info]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, dict):
            if result.get("code") == 200 or result.get("success"):
                data = result.get("data", {})
                return {
                    "success": True,
                    "orderNum": data.get("orderNum", ""),
                    "detailUrl": data.get("detailUrl", ""),
                    "message": "订单创建成功"
                }
            else:
                return {
                    "success": False,
                    "message": result.get("msg", "创建失败")
                }
        return {"success": True, "message": "操作完成"}
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"请求失败: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="WMS订单处理")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # ============ 查询商品 ============
    query_parser = subparsers.add_parser("query", help="查询商品")
    query_parser.add_argument("--book-name", help="书名")
    query_parser.add_argument("--isbn", help="ISBN")
    query_parser.add_argument("--stock-id", type=int, help="库存ID")
    query_parser.add_argument("--page-size", type=int, default=20, help="每页数量")
    
    # ============ 创建订单 ============
    create_parser = subparsers.add_parser("create", help="创建订单")
    
    # 订单基础信息（必填）
    create_parser.add_argument("--name", required=True, help="收货人姓名")
    create_parser.add_argument("--phone", required=True, help="收货人手机号")
    create_parser.add_argument("--province", required=True, help="省份")
    create_parser.add_argument("--city", required=True, help="城市")
    create_parser.add_argument("--district", required=True, help="区/县")
    create_parser.add_argument("--detail", required=True, help="详细地址")
    
    # 订单基础信息（可选）
    create_parser.add_argument("--countryside-name", default="", help="乡镇/街道")
    create_parser.add_argument("--town", default="", help="镇")
    create_parser.add_argument("--remark", default="", help="订单备注")
    create_parser.add_argument("--buyer-remark", default="", help="买家留言")
    create_parser.add_argument("--seller-message", default="", help="卖家备注")
    create_parser.add_argument("--order-source", type=int, default=15, help="订单来源(默认15=线下)")
    create_parser.add_argument("--shop-name", default="", help="店铺名称")
    create_parser.add_argument("--warehouse-id", type=int, default=0, help="仓库ID")
    create_parser.add_argument("--shop-num", default="", help="店铺编号")
    create_parser.add_argument("--session-key", default="", help="店铺Key")
    
    # 订单商品信息（必填）
    create_parser.add_argument("--book-name", required=True, help="书名")
    create_parser.add_argument("--buy-count", type=int, required=True, help="购买数量")
    create_parser.add_argument("--stock-id", type=int, required=True, help="库存ID")
    create_parser.add_argument("--stock-name", default="", help="库存名称")
    
    # 订单商品信息（可选）
    create_parser.add_argument("--isbn", default="", help="ISBN")
    create_parser.add_argument("--product-name", default="", help="产品名称")
    create_parser.add_argument("--product-code", default="", help="货号")
    create_parser.add_argument("--img", default="", help="图片URL")
    create_parser.add_argument("--sale-price", type=float, default=0.0, help="售价")
    create_parser.add_argument("--wholesale-price", type=float, default=0.0, help="批发价")
    create_parser.add_argument("--author", default="", help="作者")
    create_parser.add_argument("--press", default="", help="出版社")
    create_parser.add_argument("--make-price", type=float, default=0.0, help="制作价格")
    
    # 输出
    parser.add_argument("--output", help="输出JSON文件路径")
    
    args = parser.parse_args()
    
    if args.command == "query":
        result = query_goods(
            book_name=args.book_name,
            isbn=args.isbn,
            stock_id=args.stock_id,
            page_size=args.page_size
        )
    elif args.command == "create":
        result = create_order(
            name=args.name,
            phone=args.phone,
            province=args.province,
            city=args.city,
            district=args.district,
            detail=args.detail,
            countryside_name=args.countryside_name,
            town=args.town,
            remark=args.remark,
            buyer_remark=args.buyer_remark,
            seller_message=args.seller_message,
            order_source=args.order_source,
            shop_name=args.shop_name,
            warehouse_id=args.warehouse_id,
            shop_num=args.shop_num,
            session_key=args.session_key,
            book_name=args.book_name,
            buy_count=args.buy_count,
            stock_id=args.stock_id,
            stock_name=args.stock_name,
            isbn=args.isbn,
            product_name=args.product_name,
            product_code=args.product_code,
            img=args.img,
            sale_price=args.sale_price,
            wholesale_price=args.wholesale_price,
            author=args.author,
            press=args.press,
            make_price=args.make_price,
        )
    else:
        parser.print_help()
        return 1
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    exit(main())
