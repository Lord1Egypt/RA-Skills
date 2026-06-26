#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦当劳MCP客户端
集成麦当劳MCP Server的20个工具功能
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional

# 优先使用coze_workload_identity，如果不可用则使用标准requests
try:
    from coze_workload_identity import requests
except ImportError:
    import requests


class McDonaldMCPClient:
    """麦当劳MCP客户端"""
    
    def __init__(self):
        """初始化客户端"""
        self.base_url = "https://mcp.mcd.cn"
        self.token = self._get_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def _get_token(self) -> str:
        """获取MCP Token"""
        token = os.getenv("MCD_MCP_TOKEN")
        if not token:
            raise ValueError(
                "缺少麦当劳MCP Token凭证配置。\n"
                "请访问 https://open.mcd.cn 注册并创建应用获取Token，"
                "然后在凭证配置中填写。"
            )
        return token
    
    def _make_request(
        self, 
        tool_name: str, 
        arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发送MCP请求（JSON-RPC 2.0协议）
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            响应数据
        """
        # MCP使用JSON-RPC 2.0协议，端点为根路径
        url = self.base_url + "/"
        
        # JSON-RPC 2.0标准请求格式
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # 检查HTTP状态码
            if response.status_code == 401:
                raise ValueError(
                    "MCP Token无效或已失效。\n"
                    "请访问 https://open.mcd.cn 重新获取Token并更新凭证配置。"
                )
            elif response.status_code >= 400:
                raise Exception(
                    f"HTTP请求失败: 状态码 {response.status_code}, "
                    f"响应内容: {response.text}"
                )
            
            data = response.json()
            
            # 检查JSON-RPC错误
            if "error" in data:
                error = data["error"]
                raise Exception(
                    f"JSON-RPC错误: {error.get('message', str(error))}"
                )
            
            # 提取结果
            result = data.get("result", {})
            
            # MCP返回格式: result.structuredContent 或 result.content[].text
            if "structuredContent" in result:
                return result["structuredContent"]
            elif "content" in result and result["content"]:
                # 如果有content数组，提取第一个text内容
                content = result["content"][0]
                if content.get("type") == "text":
                    # 尝试解析文本内容中的JSON
                    text = content.get("text", "")
                    # 提取"Original Response"部分的JSON
                    if "## Original Response\n\n" in text:
                        json_str = text.split("## Original Response\n\n")[1].strip()
                        try:
                            return json.loads(json_str)
                        except:
                            pass
                    return {"text": text}
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"响应解析失败: {str(e)}")
    
    # ========== 餐品信息查询 ==========
    
    def list_nutrition_foods(self) -> Dict[str, Any]:
        """查询餐品营养信息列表"""
        return self._make_request("list-nutrition-foods")
    
    def query_meals(
        self, 
        store_code: str, 
        be_code: str
    ) -> Dict[str, Any]:
        """
        查询当前门店可售卖的餐品列表
        
        Args:
            store_code: 门店编码
            be_code: BE编码
        """
        return self._make_request(
            "query-meals",
            {"storeCode": store_code, "beCode": be_code}
        )
    
    def query_meal_detail(self, meal_code: str) -> Dict[str, Any]:
        """
        查询餐品详情
        
        Args:
            meal_code: 餐品编码
        """
        return self._make_request(
            "query-meal-detail",
            {"mealCode": meal_code}
        )
    
    # ========== 配送地址管理 ==========
    
    def delivery_query_addresses(self) -> Dict[str, Any]:
        """获取用户可配送地址列表"""
        return self._make_request("delivery-query-addresses")
    
    def delivery_create_address(
        self,
        address: str,
        lat: str,
        lng: str,
        contact: str,
        phone: str
    ) -> Dict[str, Any]:
        """
        新增配送地址
        
        Args:
            address: 详细地址
            lat: 纬度
            lng: 经度
            contact: 联系人
            phone: 联系电话
        """
        return self._make_request(
            "delivery-create-address",
            {
                "address": address,
                "lat": lat,
                "lng": lng,
                "contact": contact,
                "phone": phone
            }
        )
    
    # ========== 外送点餐流程 ==========
    
    def query_store_coupons(self, store_code: str) -> Dict[str, Any]:
        """
        查询用户在当前门店可用券
        
        Args:
            store_code: 门店编码
        """
        return self._make_request(
            "query-store-coupons",
            {"storeCode": store_code}
        )
    
    def calculate_price(
        self,
        store_code: str,
        be_code: str,
        items: List[Dict[str, Any]],
        coupons: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        商品价格计算
        
        Args:
            store_code: 门店编码
            be_code: BE编码
            items: 商品列表
            coupons: 优惠券ID列表
        """
        arguments = {
            "storeCode": store_code,
            "beCode": be_code,
            "items": items
        }
        if coupons:
            arguments["coupons"] = coupons
        
        return self._make_request("calculate-price", arguments)
    
    def create_order(
        self,
        store_code: str,
        be_code: str,
        address_id: str,
        items: List[Dict[str, Any]],
        coupons: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        创建外送订单
        
        Args:
            store_code: 门店编码
            be_code: BE编码
            address_id: 配送地址ID
            items: 商品列表
            coupons: 优惠券ID列表
        """
        arguments = {
            "storeCode": store_code,
            "beCode": be_code,
            "addressId": address_id,
            "items": items
        }
        if coupons:
            arguments["coupons"] = coupons
        
        return self._make_request("create-order", arguments)
    
    def query_order(self, order_id: str) -> Dict[str, Any]:
        """
        查询订单详情
        
        Args:
            order_id: 订单ID
        """
        return self._make_request(
            "query-order",
            {"orderId": order_id}
        )
    
    # ========== 优惠券管理 ==========
    
    def available_coupons(self) -> Dict[str, Any]:
        """麦麦省券列表查询"""
        return self._make_request("available-coupons")
    
    def auto_bind_coupons(self) -> Dict[str, Any]:
        """麦麦省一键领券"""
        return self._make_request("auto-bind-coupons")
    
    def query_my_coupons(self) -> Dict[str, Any]:
        """我的优惠券查询"""
        return self._make_request("query-my-coupons")
    
    # ========== 积分账户管理 ==========
    
    def query_my_account(self) -> Dict[str, Any]:
        """我的积分查询"""
        return self._make_request("query-my-account")
    
    # ========== 积分商城兑换 ==========
    
    def mall_points_products(self) -> Dict[str, Any]:
        """积分兑换商品列表"""
        return self._make_request("mall-points-products")
    
    def mall_product_detail(self, product_id: str) -> Dict[str, Any]:
        """
        积分兑换商品详情
        
        Args:
            product_id: 商品ID
        """
        return self._make_request(
            "mall-product-detail",
            {"productId": product_id}
        )
    
    def mall_create_order(self, product_id: str) -> Dict[str, Any]:
        """
        积分兑换商品下单
        
        Args:
            product_id: 商品ID
        """
        return self._make_request(
            "mall-create-order",
            {"productId": product_id}
        )
    
    # ========== 营销活动 ==========
    
    def campaign_calendar(self) -> Dict[str, Any]:
        """活动日历查询"""
        return self._make_request("campaign-calendar")
    
    # ========== 工具辅助 ==========
    
    def now_time_info(self) -> Dict[str, Any]:
        """获取当前时间信息"""
        return self._make_request("now-time-info")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="麦当劳MCP客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="可用命令"
    )
    
    # ========== 餐品信息查询 ==========
    
    # list-nutrition-foods
    subparsers.add_parser(
        "list-nutrition-foods",
        help="查询餐品营养信息列表"
    )
    
    # query-meals
    meals_parser = subparsers.add_parser(
        "query-meals",
        help="查询当前门店可售卖的餐品列表"
    )
    meals_parser.add_argument("--store-code", required=True, help="门店编码")
    meals_parser.add_argument("--be-code", required=True, help="BE编码")
    
    # query-meal-detail
    meal_detail_parser = subparsers.add_parser(
        "query-meal-detail",
        help="查询餐品详情"
    )
    meal_detail_parser.add_argument("--meal-code", required=True, help="餐品编码")
    
    # ========== 配送地址管理 ==========
    
    # delivery-query-addresses
    subparsers.add_parser(
        "delivery-query-addresses",
        help="获取用户可配送地址列表"
    )
    
    # delivery-create-address
    create_addr_parser = subparsers.add_parser(
        "delivery-create-address",
        help="新增配送地址"
    )
    create_addr_parser.add_argument("--address", required=True, help="详细地址")
    create_addr_parser.add_argument("--lat", required=True, help="纬度")
    create_addr_parser.add_argument("--lng", required=True, help="经度")
    create_addr_parser.add_argument("--contact", required=True, help="联系人")
    create_addr_parser.add_argument("--phone", required=True, help="联系电话")
    
    # ========== 外送点餐流程 ==========
    
    # query-store-coupons
    store_coupons_parser = subparsers.add_parser(
        "query-store-coupons",
        help="查询用户在当前门店可用券"
    )
    store_coupons_parser.add_argument("--store-code", required=True, help="门店编码")
    
    # calculate-price
    calc_price_parser = subparsers.add_parser(
        "calculate-price",
        help="商品价格计算"
    )
    calc_price_parser.add_argument("--store-code", required=True, help="门店编码")
    calc_price_parser.add_argument("--be-code", required=True, help="BE编码")
    calc_price_parser.add_argument("--items", required=True, help="商品列表(JSON格式)")
    calc_price_parser.add_argument("--coupons", help="优惠券ID列表(JSON格式)")
    
    # create-order
    create_order_parser = subparsers.add_parser(
        "create-order",
        help="创建外送订单"
    )
    create_order_parser.add_argument("--store-code", required=True, help="门店编码")
    create_order_parser.add_argument("--be-code", required=True, help="BE编码")
    create_order_parser.add_argument("--address-id", required=True, help="配送地址ID")
    create_order_parser.add_argument("--items", required=True, help="商品列表(JSON格式)")
    create_order_parser.add_argument("--coupons", help="优惠券ID列表(JSON格式)")
    
    # query-order
    query_order_parser = subparsers.add_parser(
        "query-order",
        help="查询订单详情"
    )
    query_order_parser.add_argument("--order-id", required=True, help="订单ID")
    
    # ========== 优惠券管理 ==========
    
    subparsers.add_parser(
        "available-coupons",
        help="麦麦省券列表查询"
    )
    
    subparsers.add_parser(
        "auto-bind-coupons",
        help="麦麦省一键领券"
    )
    
    subparsers.add_parser(
        "query-my-coupons",
        help="我的优惠券查询"
    )
    
    # ========== 积分账户管理 ==========
    
    subparsers.add_parser(
        "query-my-account",
        help="我的积分查询"
    )
    
    # ========== 积分商城兑换 ==========
    
    subparsers.add_parser(
        "mall-points-products",
        help="积分兑换商品列表"
    )
    
    mall_detail_parser = subparsers.add_parser(
        "mall-product-detail",
        help="积分兑换商品详情"
    )
    mall_detail_parser.add_argument("--product-id", required=True, help="商品ID")
    
    mall_order_parser = subparsers.add_parser(
        "mall-create-order",
        help="积分兑换商品下单"
    )
    mall_order_parser.add_argument("--product-id", required=True, help="商品ID")
    
    # ========== 营销活动 ==========
    
    subparsers.add_parser(
        "campaign-calendar",
        help="活动日历查询"
    )
    
    # ========== 工具辅助 ==========
    
    subparsers.add_parser(
        "now-time-info",
        help="获取当前时间信息"
    )
    
    # 解析参数
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 创建客户端
    client = McDonaldMCPClient()
    
    try:
        result = None
        
        # 餐品信息查询
        if args.command == "list-nutrition-foods":
            result = client.list_nutrition_foods()
        
        elif args.command == "query-meals":
            result = client.query_meals(args.store_code, args.be_code)
        
        elif args.command == "query-meal-detail":
            result = client.query_meal_detail(args.meal_code)
        
        # 配送地址管理
        elif args.command == "delivery-query-addresses":
            result = client.delivery_query_addresses()
        
        elif args.command == "delivery-create-address":
            result = client.delivery_create_address(
                args.address, args.lat, args.lng, args.contact, args.phone
            )
        
        # 外送点餐流程
        elif args.command == "query-store-coupons":
            result = client.query_store_coupons(args.store_code)
        
        elif args.command == "calculate-price":
            items = json.loads(args.items)
            coupons = json.loads(args.coupons) if args.coupons else None
            result = client.calculate_price(
                args.store_code, args.be_code, items, coupons
            )
        
        elif args.command == "create-order":
            items = json.loads(args.items)
            coupons = json.loads(args.coupons) if args.coupons else None
            result = client.create_order(
                args.store_code, args.be_code, args.address_id, items, coupons
            )
        
        elif args.command == "query-order":
            result = client.query_order(args.order_id)
        
        # 优惠券管理
        elif args.command == "available-coupons":
            result = client.available_coupons()
        
        elif args.command == "auto-bind-coupons":
            result = client.auto_bind_coupons()
        
        elif args.command == "query-my-coupons":
            result = client.query_my_coupons()
        
        # 积分账户管理
        elif args.command == "query-my-account":
            result = client.query_my_account()
        
        # 积分商城兑换
        elif args.command == "mall-points-products":
            result = client.mall_points_products()
        
        elif args.command == "mall-product-detail":
            result = client.mall_product_detail(args.product_id)
        
        elif args.command == "mall-create-order":
            result = client.mall_create_order(args.product_id)
        
        # 营销活动
        elif args.command == "campaign-calendar":
            result = client.campaign_calendar()
        
        # 工具辅助
        elif args.command == "now-time-info":
            result = client.now_time_info()
        
        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except ValueError as e:
        print(f"配置错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"操作失败: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
