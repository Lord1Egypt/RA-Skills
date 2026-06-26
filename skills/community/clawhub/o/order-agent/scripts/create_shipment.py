#!/usr/bin/env python3
"""
WMS 创建发货单脚本
"""
import json
import argparse
import requests
from typing import Dict, Any, Optional

# WMS API 配置 (可配置化)
WMS_API_URL = "https://wms.example.com/api/v1/shipment/create"
WMS_API_KEY = ""  # 用户配置

def create_shipment(
    order_no: str,
    warehouse_code: str,
    item_name: str,
    quantity: int,
    consignee_name: str,
    phone: str,
    address: str,
    isbn: Optional[str] = None,
    remark: str = "",
    api_url: str = WMS_API_URL,
    api_key: str = WMS_API_KEY
) -> Dict[str, Any]:
    """
    创建发货单
    
    Args:
        order_no: 客户订单号
        warehouse_code: 仓库编码
        item_name: 商品名称
        quantity: 数量
        consignee_name: 收件人姓名
        phone: 收件人电话
        address: 收件人地址
        isbn: ISBN (可选)
        remark: 备注
        api_url: WMS API 地址
        api_key: WMS API 密钥
    
    Returns:
        WMS 响应结果
    """
    # 构建请求体
    payload = {
        "orderNo": order_no,
        "warehouseCode": warehouse_code,
        "consignee": {
            "name": consignee_name,
            "phone": phone,
            "address": address
        },
        "items": [
            {
                "sku": isbn if isbn else item_name,
                "name": item_name,
                "quantity": quantity
            }
        ],
        "remark": remark
    }
    
    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"请求失败: {str(e)}",
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="创建WMS发货单")
    parser.add_argument("--order-no", required=True, help="客户订单号")
    parser.add_argument("--warehouse", required=True, help="仓库编码")
    parser.add_argument("--item-name", required=True, help="商品名称")
    parser.add_argument("--quantity", type=int, required=True, help="数量")
    parser.add_argument("--isbn", help="ISBN (可选)")
    parser.add_argument("--consignee", required=True, help="收件人姓名")
    parser.add_argument("--phone", required=True, help="收件人电话")
    parser.add_argument("--address", required=True, help="收件人地址")
    parser.add_argument("--remark", default="", help="备注")
    parser.add_argument("--api-url", default=WMS_API_URL, help="WMS API地址")
    parser.add_argument("--api-key", default=WMS_API_KEY, help="WMS API密钥")
    parser.add_argument("--output", help="输出JSON文件路径")
    
    args = parser.parse_args()
    
    result = create_shipment(
        order_no=args.order_no,
        warehouse_code=args.warehouse,
        item_name=args.item_name,
        quantity=args.quantity,
        consignee_name=args.consignee,
        phone=args.phone,
        address=args.address,
        isbn=args.isbn,
        remark=args.remark,
        api_url=args.api_url,
        api_key=args.api_key
    )
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 返回码
    return 0 if result.get("success") else 1

if __name__ == "__main__":
    exit(main())
