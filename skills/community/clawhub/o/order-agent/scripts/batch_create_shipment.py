#!/usr/bin/env python3
"""
批量创建发货单脚本
从 Excel 文件读取订单信息，批量调用 WMS API 创建发货单
"""
import json
import argparse
import pandas as pd
import requests
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# WMS API 配置
WMS_API_URL = "https://wms.example.com/api/v1/shipment/create"
WMS_API_KEY = ""

def create_shipment_api(
    order_data: Dict[str, Any],
    api_url: str = WMS_API_URL,
    api_key: str = WMS_API_KEY
) -> Dict[str, Any]:
    """调用 WMS API 创建单个发货单"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.post(api_url, json=order_data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"请求失败: {str(e)}",
            "error": str(e)
        }

def read_excel_orders(file_path: str) -> List[Dict[str, Any]]:
    """
    读取 Excel 文件中的订单信息
    
    标准列名映射:
    - 商品名称 -> item_name
    - 数量 -> quantity
    - ISBN -> isbn
    - 收件人名称 -> consignee_name
    - 手机号 -> phone
    - 地址 -> address
    """
    # 读取 Excel
    df = pd.read_excel(file_path)
    
    # 列名映射
    column_mapping = {
        '商品名称': 'item_name',
        '数量': 'quantity',
        'ISBN': 'isbn',
        '收件人名称': 'consignee_name',
        '手机号': 'phone',
        '地址': 'address',
        '备注': 'remark'
    }
    
    # 重命名列
    df = df.rename(columns=column_mapping)
    
    # 转换为订单列表
    orders = df.to_dict('records')
    
    # 验证必填字段
    required_fields = ['item_name', 'quantity', 'consignee_name', 'phone', 'address']
    valid_orders = []
    errors = []
    
    for idx, order in enumerate(orders):
        missing = [f for f in required_fields if not order.get(f)]
        if missing:
            errors.append(f"第{idx+1}行缺失必填字段: {missing}")
        else:
            valid_orders.append(order)
    
    if errors:
        print("⚠️ 数据校验警告:")
        for err in errors:
            print(f"  - {err}")
    
    return valid_orders

def build_payload(order: Dict[str, Any], warehouse_code: str, order_prefix: str = "ORDER") -> Dict[str, Any]:
    """构建 WMS API 请求体"""
    import uuid
    
    order_no = f"{order_prefix}{int(time.time())}{uuid.uuid4().hex[:4]}"
    
    payload = {
        "orderNo": order_no,
        "warehouseCode": warehouse_code,
        "consignee": {
            "name": order.get('consignee_name', ''),
            "phone": order.get('phone', ''),
            "address": order.get('address', '')
        },
        "items": [
            {
                "sku": order.get('isbn', order.get('item_name', '')),
                "name": order.get('item_name', ''),
                "quantity": int(order.get('quantity', 1))
            }
        ],
        "remark": order.get('remark', '')
    }
    
    return payload

def batch_create(
    excel_path: str,
    warehouse_code: str,
    max_workers: int = 5,
    api_url: str = WMS_API_URL,
    api_key: str = WMS_API_KEY
) -> Dict[str, Any]:
    """
    批量创建发货单
    
    Args:
        excel_path: Excel 文件路径
        warehouse_code: 仓库编码
        max_workers: 最大并发数
        api_url: WMS API 地址
        api_key: WMS API 密钥
    
    Returns:
        批量处理结果
    """
    print(f"📂 读取订单文件: {excel_path}")
    
    # 读取订单
    orders = read_excel_orders(excel_path)
    total = len(orders)
    print(f"✅ 有效订单数: {total}")
    
    if total == 0:
        return {
            "success": False,
            "message": "没有有效的订单数据",
            "total": 0,
            "success_count": 0,
            "failed_count": 0,
            "results": []
        }
    
    # 构建请求体
    payloads = [build_payload(order, warehouse_code) for order in orders]
    
    # 批量提交
    results = []
    success_count = 0
    failed_count = 0
    
    print(f"🚀 开始批量创建发货单 (并发: {max_workers})...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(create_shipment_api, payload, api_url, api_key): payload 
            for payload in payloads
        }
        
        for future in as_completed(futures):
            payload = futures[future]
            try:
                result = future.result()
                
                # 提取关键信息
                order_result = {
                    "orderNo": payload.get("orderNo"),
                    "itemName": payload["items"][0]["name"],
                    "consignee": payload["consignee"]["name"],
                    "success": result.get("success", False),
                    "message": result.get("message", ""),
                    "orderId": result.get("orderId", ""),
                    "trackingUrl": result.get("trackingUrl", "")
                }
                
                results.append(order_result)
                
                if result.get("success"):
                    success_count += 1
                    print(f"  ✅ {order_result['orderNo']} -> {result.get('orderId', 'N/A')}")
                else:
                    failed_count += 1
                    print(f"  ❌ {order_result['orderNo']} -> {result.get('message', '失败')}")
                    
            except Exception as e:
                failed_count += 1
                print(f"  ❌ {payload.get('orderNo')} -> 异常: {str(e)}")
                results.append({
                    "orderNo": payload.get("orderNo"),
                    "success": False,
                    "message": str(e)
                })
    
    # 汇总结果
    summary = {
        "success": failed_count == 0,
        "total": total,
        "success_count": success_count,
        "failed_count": failed_count,
        "results": results
    }
    
    print(f"\n📊 批量处理完成:")
    print(f"   总计: {total}")
    print(f"   成功: {success_count}")
    print(f"   失败: {failed_count}")
    
    return summary

def main():
    parser = argparse.ArgumentParser(description="批量创建WMS发货单")
    parser.add_argument("--excel", required=True, help="Excel订单文件路径")
    parser.add_argument("--warehouse", required=True, help="仓库编码")
    parser.add_argument("--max-workers", type=int, default=5, help="最大并发数")
    parser.add_argument("--api-url", default=WMS_API_URL, help="WMS API地址")
    parser.add_argument("--api-key", default=WMS_API_KEY, help="WMS API密钥")
    parser.add_argument("--output", help="输出JSON结果文件路径")
    
    args = parser.parse_args()
    
    result = batch_create(
        excel_path=args.excel,
        warehouse_code=args.warehouse,
        max_workers=args.max_workers,
        api_url=args.api_url,
        api_key=args.api_key
    )
    
    # 输出结果
    print("\n" + "="*50)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: {args.output}")
    
    return 0 if result.get("success") else 1

if __name__ == "__main__":
    exit(main())
