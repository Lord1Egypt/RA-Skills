"""
麦当劳MCP API客户端
基于麦当劳MCP平台的智能点餐客户端
"""

import os
import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from urllib.parse import urljoin


class McDonaldsMCPError(Exception):
    """麦当劳MCP异常基类"""
    pass


class AuthenticationError(McDonaldsMCPError):
    """认证错误"""
    pass


class MenuUnavailableError(McDonaldsMCPError):
    """菜单不可用"""
    pass


class OrderCreationError(McDonaldsMCPError):
    """订单创建失败"""
    pass


class StoreNotFoundError(McDonaldsMCPError):
    """门店未找到"""
    pass


class McDonaldsMCPClient:
    """麦当劳MCP API客户端"""
    
    def __init__(self, token: str = None, base_url: str = None):
        """
        初始化客户端
        
        Args:
            token: MCP Token，默认为环境变量 MCD_MCP_TOKEN
            base_url: MCP 服务地址，默认为环境变量 MCD_MCP_URL 或 https://mcp.mcd.cn
        """
        self.token = token or os.getenv('MCD_MCP_TOKEN', '')
        self.base_url = base_url or os.getenv('MCD_MCP_URL', 'https://mcp.mcd.cn')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'User-Agent': 'McDonaldsMCPClient/1.0.0'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def _make_request(self, method: str, endpoint: str, data: Dict = None, 
                     params: Dict = None) -> Dict:
        """
        发送API请求
        
        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE)
            endpoint: API端点
            data: 请求体数据
            params: URL参数
            
        Returns:
            API响应数据
            
        Raises:
            AuthenticationError: Token无效或过期
            MenuUnavailableError: 菜单不可用
            OrderCreationError: 订单创建失败
            McDonaldsMCPError: 其他API错误
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Token无效或已过期，请检查MCP Token")
            elif e.response.status_code == 404:
                if 'menu' in endpoint:
                    raise MenuUnavailableError("菜单暂时不可用")
                elif 'store' in endpoint:
                    raise StoreNotFoundError("未找到指定门店")
                else:
                    raise McDonaldsMCPError(f"资源未找到: {endpoint}")
            elif e.response.status_code == 400:
                error_msg = "请求参数错误"
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    pass
                raise OrderCreationError(f"订单创建失败: {error_msg}")
            elif e.response.status_code == 429:
                raise McDonaldsMCPError("请求过于频繁，请稍后再试")
            else:
                raise McDonaldsMCPError(f"API错误 ({e.response.status_code}): {e}")
                
        except requests.exceptions.ConnectionError:
            raise McDonaldsMCPError("网络连接失败，请检查网络设置")
        except requests.exceptions.Timeout:
            raise McDonaldsMCPError("请求超时，请稍后再试")
        except json.JSONDecodeError:
            raise McDonaldsMCPError("API响应格式错误")
        except Exception as e:
            raise McDonaldsMCPError(f"未知错误: {str(e)}")
    
    # ========== 菜单相关接口 ==========
    
    def get_menu(self, store_id: Optional[str] = None, 
                language: str = 'zh-CN') -> Dict:
        """
        获取麦当劳菜单
        
        Args:
            store_id: 门店ID，可选
            language: 语言代码，默认zh-CN
            
        Returns:
            菜单数据，包含分类和产品信息
        """
        endpoint = "v1/menu"
        params = {'language': language}
        if store_id:
            params['store_id'] = store_id
            
        return self._make_request('GET', endpoint, params=params)
    
    def get_categories(self, store_id: Optional[str] = None) -> List[Dict]:
        """
        获取菜单分类
        
        Args:
            store_id: 门店ID，可选
            
        Returns:
            分类列表
        """
        menu = self.get_menu(store_id)
        return menu.get('categories', [])
    
    def get_products_by_category(self, category_id: str, 
                               store_id: Optional[str] = None) -> List[Dict]:
        """
        获取指定分类的产品
        
        Args:
            category_id: 分类ID
            store_id: 门店ID，可选
            
        Returns:
            产品列表
        """
        menu = self.get_menu(store_id)
        for category in menu.get('categories', []):
            if category.get('id') == category_id:
                return category.get('products', [])
        return []
    
    # ========== 产品搜索接口 ==========
    
    def search_products(self, keyword: str, category: Optional[str] = None,
                       store_id: Optional[str] = None) -> List[Dict]:
        """
        搜索产品
        
        Args:
            keyword: 搜索关键词
            category: 产品类别，可选
            store_id: 门店ID，可选
            
        Returns:
            匹配的产品列表
        """
        endpoint = "v1/products/search"
        data = {'keyword': keyword}
        if category:
            data['category'] = category
        if store_id:
            data['store_id'] = store_id
            
        return self._make_request('POST', endpoint, data=data)
    
    def get_product_details(self, product_id: str, 
                          store_id: Optional[str] = None) -> Dict:
        """
        获取产品详情
        
        Args:
            product_id: 产品ID
            store_id: 门店ID，可选
            
        Returns:
            产品详情信息
        """
        endpoint = f"v1/products/{product_id}"
        params = {}
        if store_id:
            params['store_id'] = store_id
            
        return self._make_request('GET', endpoint, params=params)
    
    # ========== 门店相关接口 ==========
    
    def find_stores(self, latitude: float, longitude: float, 
                   radius: int = 5000, limit: int = 20) -> List[Dict]:
        """
        查找附近门店
        
        Args:
            latitude: 纬度
            longitude: 经度
            radius: 搜索半径（米），默认5000
            limit: 返回结果数量，默认20
            
        Returns:
            门店列表，包含距离信息
        """
        endpoint = "v1/stores/nearby"
        data = {
            'latitude': latitude,
            'longitude': longitude,
            'radius': radius,
            'limit': limit
        }
        
        return self._make_request('POST', endpoint, data=data)
    
    def get_store_details(self, store_id: str) -> Dict:
        """
        获取门店详情
        
        Args:
            store_id: 门店ID
            
        Returns:
            门店详情信息
        """
        endpoint = f"v1/stores/{store_id}"
        return self._make_request('GET', endpoint)
    
    def get_store_hours(self, store_id: str) -> Dict:
        """
        获取门店营业时间
        
        Args:
            store_id: 门店ID
            
        Returns:
            营业时间信息
        """
        endpoint = f"v1/stores/{store_id}/hours"
        return self._make_request('GET', endpoint)
    
    # ========== 订单相关接口 ==========
    
    def create_order(self, items: List[Dict], store_id: str,
                    user_info: Dict = None, 
                    delivery_info: Dict = None,
                    coupon_code: Optional[str] = None,
                    payment_method: str = 'online') -> Dict:
        """
        创建订单
        
        Args:
            items: 订单项列表，每个项包含:
                - product_id: 产品ID
                - quantity: 数量
                - customizations: 定制选项（可选）
            store_id: 门店ID
            user_info: 用户信息，包含姓名、电话等
            delivery_info: 配送信息（如果需要配送）
            coupon_code: 优惠券代码，可选
            payment_method: 支付方式，默认online
            
        Returns:
            订单信息，包含订单ID、总价等
        """
        endpoint = "v1/orders"
        data = {
            'items': items,
            'store_id': store_id,
            'payment_method': payment_method
        }
        
        if user_info:
            data['user_info'] = user_info
        if delivery_info:
            data['delivery_info'] = delivery_info
        if coupon_code:
            data['coupon_code'] = coupon_code
            
        return self._make_request('POST', endpoint, data=data)
    
    def get_order_status(self, order_id: str) -> Dict:
        """
        获取订单状态
        
        Args:
            order_id: 订单ID
            
        Returns:
            订单状态信息
        """
        endpoint = f"v1/orders/{order_id}"
        return self._make_request('GET', endpoint)
    
    def cancel_order(self, order_id: str, reason: Optional[str] = None) -> Dict:
        """
        取消订单
        
        Args:
            order_id: 订单ID
            reason: 取消原因，可选
            
        Returns:
            取消结果
        """
        endpoint = f"v1/orders/{order_id}/cancel"
        data = {'reason': reason} if reason else {}
        return self._make_request('POST', endpoint, data=data)
    
    def get_order_history(self, user_id: Optional[str] = None,
                         limit: int = 20, offset: int = 0) -> List[Dict]:
        """
        获取订单历史
        
        Args:
            user_id: 用户ID，可选
            limit: 返回数量，默认20
            offset: 偏移量，默认0
            
        Returns:
            订单历史列表
        """
        endpoint = "v1/orders/history"
        params = {'limit': limit, 'offset': offset}
        if user_id:
            params['user_id'] = user_id
            
        return self._make_request('GET', endpoint, params=params)
    
    # ========== 优惠券相关接口 ==========
    
    def get_available_coupons(self, store_id: Optional[str] = None) -> List[Dict]:
        """
        获取可用优惠券
        
        Args:
            store_id: 门店ID，可选
            
        Returns:
            优惠券列表
        """
        endpoint = "v1/coupons/available"
        params = {}
        if store_id:
            params['store_id'] = store_id
            
        return self._make_request('GET', endpoint, params=params)
    
    def validate_coupon(self, coupon_code: str, 
                       store_id: Optional[str] = None) -> Dict:
        """
        验证优惠券
        
        Args:
            coupon_code: 优惠券代码
            store_id: 门店ID，可选
            
        Returns:
            验证结果和优惠信息
        """
        endpoint = "v1/coupons/validate"
        data = {'code': coupon_code}
        if store_id:
            data['store_id'] = store_id
            
        return self._make_request('POST', endpoint, data=data)
    
    # ========== 工具方法 ==========
    
    def format_price(self, price_cents: int) -> str:
        """格式化价格（分转元）"""
        return f"¥{price_cents / 100:.2f}"
    
    def calculate_order_total(self, items: List[Dict], 
                            coupon_discount: int = 0) -> Dict:
        """
        计算订单总价
        
        Args:
            items: 订单项列表
            coupon_discount: 优惠券折扣（分）
            
        Returns:
            价格摘要
        """
        subtotal = 0
        for item in items:
            price = item.get('price_cents', 0)
            quantity = item.get('quantity', 1)
            subtotal += price * quantity
        
        # 假设税费为10%
        tax = int(subtotal * 0.1)
        # 假设配送费为500分（5元）
        delivery_fee = 500
        
        total = subtotal + tax + delivery_fee - coupon_discount
        
        return {
            'subtotal': self.format_price(subtotal),
            'tax': self.format_price(tax),
            'delivery_fee': self.format_price(delivery_fee),
            'discount': self.format_price(coupon_discount),
            'total': self.format_price(total),
            'subtotal_cents': subtotal,
            'total_cents': total
        }
    
    def suggest_combo(self, main_product: Dict) -> List[Dict]:
        """
        推荐套餐组合
        
        Args:
            main_product: 主产品
            
        Returns:
            推荐的套餐组合
        """
        # 简单的套餐推荐逻辑
        combos = []
        
        # 如果是汉堡类，推荐搭配薯条和饮料
        if '汉堡' in main_product.get('name', '') or '堡' in main_product.get('name', ''):
            combos.append({
                'name': '经典套餐',
                'items': [
                    main_product,
                    {'name': '中薯条', 'price_cents': 1500},
                    {'name': '中可乐', 'price_cents': 1000}
                ],
                'total_saving': '节省 ¥5.00'
            })
        
        return combos
    
    def check_store_availability(self, store_id: str) -> bool:
        """
        检查门店是否可用
        
        Args:
            store_id: 门店ID
            
        Returns:
            是否可用
        """
        try:
            store_info = self.get_store_details(store_id)
            hours = self.get_store_hours(store_id)
            
            # 检查是否在营业时间内
            current_hour = datetime.now().hour
            opening_hour = hours.get('opening_hour', 7)
            closing_hour = hours.get('closing_hour', 23)
            
            return opening_hour <= current_hour < closing_hour
            
        except Exception:
            return False


# 示例使用
if __name__ == "__main__":
    # 初始化客户端
    client = McDonaldsMCPClient()
    
    print("=== 麦当劳MCP点餐客户端测试 ===")
    
    try:
        # 测试获取菜单
        print("1. 获取菜单...")
        menu = client.get_menu()
        categories = client.get_categories()
        print(f"  找到 {len(categories)} 个分类")
        
        # 测试搜索产品
        print("2. 搜索产品...")
        products = client.search_products("巨无霸")
        print(f"  找到 {len(products)} 个相关产品")
        
        # 测试查找门店
        print("3. 查找附近门店...")
        # 上海坐标
        stores = client.find_stores(latitude=31.2304, longitude=121.4737, radius=3000)
        print(f"  找到 {len(stores)} 家附近门店")
        
        if stores:
            store_id = stores[0]['id']
            print(f"  选择门店: {stores[0]['name']}")
            
            # 测试创建订单
            print("4. 创建测试订单...")
            test_items = [
                {
                    'product_id': 'big_mac',
                    'quantity': 1,
                    'customizations': {'size': 'large'}
                },
                {
                    'product_id': 'coke',
                    'quantity': 1,
                    'customizations': {'ice': 'normal'}
                }
            ]
            
            # 在实际使用中需要真实的用户信息
            # order = client.create_order(
            #     items=test_items,
            #     store_id=store_id,
            #     user_info={'name': '测试用户', 'phone': '13800138000'}
            # )
            # print(f"  订单创建成功: {order.get('order_id')}")
        
        print("✅ 所有测试通过！")
        
    except AuthenticationError as e:
        print(f"❌ 认证失败: {e}")
    except MenuUnavailableError as e:
        print(f"❌ 菜单不可用: {e}")
    except OrderCreationError as e:
        print(f"❌ 订单创建失败: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")