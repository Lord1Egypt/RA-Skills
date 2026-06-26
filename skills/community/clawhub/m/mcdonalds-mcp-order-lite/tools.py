"""
OpenClaw工具集成
将麦当劳MCP点餐功能集成到OpenClaw中
"""

import os
import json
from typing import Dict, List, Optional, Any
from openclaw.skill import tool
from .client import McDonaldsMCPClient, McDonaldsMCPError
from .nlp_processor import McDonaldsNLPProcessor, OrderIntent, IntentResult

# 初始化客户端和NLP处理器
client = McDonaldsMCPClient()
nlp_processor = McDonaldsNLPProcessor()


@tool
async def mcdonalds_view_menu(store_id: str = None, language: str = "zh-CN") -> Dict:
    """
    查看麦当劳菜单
    
    Args:
        store_id: 门店ID（可选）
        language: 语言代码，默认zh-CN
        
    Returns:
        菜单数据
    """
    try:
        menu = client.get_menu(store_id, language)
        
        # 格式化返回结果
        categories = menu.get('categories', [])
        formatted_result = {
            'success': True,
            'store_id': store_id,
            'total_categories': len(categories),
            'categories': []
        }
        
        for category in categories[:10]:  # 限制返回数量
            category_info = {
                'id': category.get('id'),
                'name': category.get('name'),
                'description': category.get('description'),
                'product_count': len(category.get('products', []))
            }
            
            # 添加前几个产品作为示例
            sample_products = []
            for product in category.get('products', [])[:3]:
                sample_products.append({
                    'id': product.get('id'),
                    'name': product.get('name'),
                    'price': client.format_price(product.get('price_cents', 0)),
                    'description': product.get('description', '')[:50] + '...'
                })
            
            if sample_products:
                category_info['sample_products'] = sample_products
            
            formatted_result['categories'].append(category_info)
        
        return formatted_result
        
    except McDonaldsMCPError as e:
        return {
            'success': False,
            'error': str(e),
            'message': '获取菜单失败'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': '未知错误'
        }


@tool
async def mcdonalds_search_product(keyword: str, category: str = None, 
                                  store_id: str = None) -> Dict:
    """
    搜索麦当劳产品
    
    Args:
        keyword: 搜索关键词
        category: 产品类别（可选）
        store_id: 门店ID（可选）
        
    Returns:
        搜索结果
    """
    try:
        products = client.search_products(keyword, category, store_id)
        
        formatted_result = {
            'success': True,
            'keyword': keyword,
            'total_results': len(products),
            'products': []
        }
        
        for product in products[:20]:  # 限制返回数量
            product_info = {
                'id': product.get('id'),
                'name': product.get('name'),
                'price': client.format_price(product.get('price_cents', 0)),
                'category': product.get('category'),
                'description': product.get('description', '')[:100],
                'available': product.get('available', True)
            }
            
            # 添加图片URL（如果有）
            if product.get('image_url'):
                product_info['image_url'] = product.get('image_url')
            
            formatted_result['products'].append(product_info)
        
        return formatted_result
        
    except McDonaldsMCPError as e:
        return {
            'success': False,
            'error': str(e),
            'message': '搜索产品失败'
        }


@tool
async def mcdonalds_find_stores(latitude: float, longitude: float, 
                               radius: int = 5000, limit: int = 10) -> Dict:
    """
    查找附近麦当劳门店
    
    Args:
        latitude: 纬度
        longitude: 经度
        radius: 搜索半径（米），默认5000
        limit: 返回结果数量，默认10
        
    Returns:
        门店列表
    """
    try:
        stores = client.find_stores(latitude, longitude, radius, limit)
        
        formatted_result = {
            'success': True,
            'location': {'latitude': latitude, 'longitude': longitude},
            'radius': radius,
            'total_stores': len(stores),
            'stores': []
        }
        
        for store in stores:
            store_info = {
                'id': store.get('id'),
                'name': store.get('name'),
                'address': store.get('address'),
                'distance': f"{store.get('distance', 0)}米",
                'phone': store.get('phone'),
                'opening_hours': store.get('opening_hours')
            }
            
            # 添加营业状态
            if client.check_store_availability(store.get('id')):
                store_info['status'] = '营业中'
            else:
                store_info['status'] = '已打烊'
            
            formatted_result['stores'].append(store_info)
        
        return formatted_result
        
    except McDonaldsMCPError as e:
        return {
            'success': False,
            'error': str(e),
            'message': '查找门店失败'
        }


@tool
async def mcdonalds_create_order(items: List[Dict], store_id: str,
                                user_name: str = None, user_phone: str = None,
                                delivery_address: str = None,
                                coupon_code: str = None) -> Dict:
    """
    创建麦当劳订单
    
    Args:
        items: 订单项列表，每个项包含:
            - product_id: 产品ID
            - quantity: 数量
            - customizations: 定制选项（可选）
        store_id: 门店ID
        user_name: 用户姓名
        user_phone: 用户电话
        delivery_address: 配送地址（可选）
        coupon_code: 优惠券代码（可选）
        
    Returns:
        订单信息
    """
    try:
        # 准备用户信息
        user_info = {}
        if user_name:
            user_info['name'] = user_name
        if user_phone:
            user_info['phone'] = user_phone
        
        # 准备配送信息
        delivery_info = None
        if delivery_address:
            delivery_info = {
                'address': delivery_address,
                'type': 'delivery'
            }
        
        # 创建订单
        order = client.create_order(
            items=items,
            store_id=store_id,
            user_info=user_info if user_info else None,
            delivery_info=delivery_info,
            coupon_code=coupon_code
        )
        
        # 计算价格摘要
        price_summary = client.calculate_order_total(
            items,
            coupon_discount=order.get('discount_cents', 0)
        )
        
        formatted_result = {
            'success': True,
            'order_id': order.get('order_id'),
            'store_id': store_id,
            'status': order.get('status', 'created'),
            'created_at': order.get('created_at'),
            'estimated_ready_time': order.get('estimated_ready_time'),
            'price_summary': price_summary,
            'message': '订单创建成功'
        }
        
        # 添加订单项详情
        formatted_result['items'] = []
        for item in items:
            formatted_result['items'].append({
                'product_id': item.get('product_id'),
                'quantity': item.get('quantity'),
                'customizations': item.get('customizations', {})
            })
        
        return formatted_result
        
    except McDonaldsMCPError as e:
        return {
            'success': False,
            'error': str(e),
            'message': '创建订单失败'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'创建订单时发生错误: {str(e)}'
        }


@tool
async def mcdonalds_check_order(order_id: str) -> Dict:
    """
    查询订单状态
    
    Args:
        order_id: 订单ID
        
    Returns:
        订单状态信息
    """
    try:
        order_status = client.get_order_status(order_id)
        
        formatted_result = {
            'success': True,
            'order_id': order_id,
            'status': order_status.get('status'),
            'store_name': order_status.get('store_name'),
            'created_at': order_status.get('created_at'),
            'updated_at': order_status.get('updated_at'),
            'estimated_ready_time': order_status.get('estimated_ready_time'),
            'items_count': len(order_status.get('items', [])),
            'total_price': client.format_price(order_status.get('total_cents', 0))
        }
        
        # 添加状态描述
        status_descriptions = {
            'created': '订单已创建',
            'confirmed': '订单已确认',
            'preparing': '正在制作',
            'ready': '准备就绪',
            'delivering': '配送中',
            'delivered': '已送达',
            'cancelled': '已取消'
        }
        
        current_status = order_status.get('status')
        formatted_result['status_description'] = status_descriptions.get(
            current_status, '未知状态'
        )
        
        return formatted_result
        
    except McDonaldsMCPError as e:
        return {
            'success': False,
            'error': str(e),
            'message': '查询订单状态失败'
        }


@tool
async def mcdonalds_cancel_order(order_id: str, reason: str = None) -> Dict:
    """
    取消订单
    
    Args:
        order_id: 订单ID
        reason: 取消原因（可选）
        
    Returns:
        取消结果
    """
    try:
        result = client.cancel_order(order_id, reason)
        
        return {
            'success': True,
            'order_id': order_id,
            'cancelled': result.get('cancelled', False),
            'refund_amount': client.format_price(result.get('refund_cents', 0)),
            'message': result.get('message', '订单取消成功')
        }
        
    except McDonaldsMCPError as e:
        return {
            'success': False,
            'error': str(e),
            'message': '取消订单失败'
        }


@tool
async def mcdonalds_analyze_intent(user_input: str) -> Dict:
    """
    分析用户点餐意图
    
    Args:
        user_input: 用户输入文本
        
    Returns:
        意图分析结果
    """
    try:
        intent_result = nlp_processor.recognize_intent(user_input)
        
        formatted_result = {
            'success': True,
            'input': user_input,
            'intent': intent_result.intent.value,
            'confidence': intent_result.confidence,
            'entities': intent_result.entities,
            'suggested_response': nlp_processor.suggest_response(intent_result)
        }
        
        # 如果是点餐意图，尝试解析订单项
        if intent_result.intent == OrderIntent.CREATE_ORDER:
            # 获取菜单用于产品匹配
            menu = client.get_menu()
            all_products = []
            for category in menu.get('categories', []):
                all_products.extend(category.get('products', []))
            
            order_items = nlp_processor.parse_order_items(user_input, all_products)
            
            if order_items:
                formatted_result['parsed_items'] = []
                for item in order_items:
                    formatted_result['parsed_items'].append({
                        'product_name': item.product_name,
                        'quantity': item.quantity,
                        'customizations': item.customizations,
                        'notes': item.notes
                    })
                
                # 生成订单摘要
                formatted_result['order_summary'] = nlp_processor.generate_order_summary(order_items)
        
        return formatted_result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': '意图分析失败'
        }


@tool
async def mcdonalds_get_available_coupons(store_id: str = None) -> Dict:
    """
    获取可用优惠券
    
    Args:
        store_id: 门店ID（可选）
        
    Returns:
        优惠券列表
    """
    try:
        coupons = client.get_available_coupons(store_id)
        
        formatted_result = {
            'success': True,
            'total_coupons': len(coupons),
            'coupons': []
        }
        
        for coupon in coupons[:10]:  # 限制返回数量
            coupon_info = {
                'code': coupon.get('code'),
                'name': coupon.get('name'),
                'description': coupon.get('description'),
                'discount': coupon.get('discount_description'),
                'valid_until': coupon.get('valid_until'),
                'min_order_amount': client.format_price(coupon.get('min_order_cents', 0))
            }
            
            formatted_result['coupons'].append(coupon_info)
        
        return formatted_result
        
    except McDonaldsMCPError as e:
        return {
            'success': False,
            'error': str(e),
            'message': '获取优惠券失败'
        }


@tool
async def mcdonalds_suggest_combo(main_product: str) -> Dict:
    """
    推荐套餐组合
    
    Args:
        main_product: 主产品名称
        
    Returns:
        套餐推荐
    """
    try:
        # 搜索主产品
        products = client.search_products(main_product)
        
        if not products:
            return {
                'success': False,
                'message': f'未找到产品: {main_product}'
            }
        
        main_product_info = products[0]
        combos = client.suggest_combo(main_product_info)
        
        formatted_result = {
            'success': True,
            'main_product': main_product_info.get('name'),
            'total_combos': len(combos),
            'combos': []
        }
        
        for combo in combos:
            combo_info = {
                'name': combo.get('name'),
                'total_saving': combo.get('total_saving'),
                'items': []
            }
            
            for item in combo.get('items', []):
                combo_info['items'].append({
                    'name': item.get('name'),
                    'price': client.format_price(item.get('price_cents', 0))
                })
            
            formatted_result['combos'].append(combo_info)
        
        return formatted_result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': '推荐套餐失败'
        }


# 高级工具：智能点餐助手
@tool
async def mcdonalds_smart_order_assistant(user_input: str, 
                                         latitude: float = None,
                                         longitude: float = None) -> Dict:
    """
    智能点餐助手 - 一站式处理用户点餐需求
    
    Args:
        user_input: 用户输入文本
        latitude: 纬度（可选，用于查找门店）
        longitude: 经度（可选，用于查找门店）
        
    Returns:
        智能处理结果
    """
    try:
        # 分析用户意图
        intent_result = nlp_processor.recognize_intent(user_input)
        
        response = {
            'success': True,
            'input': user_input,
            'intent': intent_result.intent.value,
            'confidence': intent_result.confidence,
            'suggested_actions': [],
            'next_steps': []
        }
        
        # 根据意图提供不同的处理建议
        if intent_result.intent == OrderIntent.VIEW_MENU:
            response['suggested_actions'].append({
                'action': 'view_menu',
                'description': '查看麦当劳菜单',
                'tool': 'mcdonalds_view_menu'
            })
            response['next_steps'].append('请告诉我您想查看哪个门店的菜单（可选）')
            
        elif intent_result.intent == OrderIntent.SEARCH_PRODUCT:
            keyword = intent_result.entities.get('product_cn', '')
            if keyword:
                response['suggested_actions'].append({
                    'action': 'search_product',
                    'description': f'搜索产品: {keyword}',
                    'tool': 'mcdonalds_search_product',
                    'parameters': {'keyword': keyword}
                })
            else:
                response['next_steps'].append('请告诉我您想搜索什么产品？')
            
        elif intent_result.intent == OrderIntent.CREATE_ORDER:
            # 解析订单项
            menu = client.get_menu()
            all_products = []
            for category in menu.get('categories', []):
                all_products.extend(category.get('products', []))
            
            order_items = nlp_processor.parse_order_items(user_input, all_products)
            
            if order_items:
                response['parsed_order'] = {
                    'items': [],
                    'summary': nlp_processor.generate_order_summary(order_items)
                }
                
                for item in order_items:
                    response['parsed_order']['items'].append({
                        'product_name': item.product_name,
                        'quantity': item.quantity,
                        'customizations': item.customizations
                    })
                
                response['suggested_actions'].append({
                    'action': 'create_order',
                    'description': '创建订单',
                    'tool': 'mcdonalds_create_order',
                    'note': '需要提供门店ID和用户信息'
                })
                response['next_steps'].extend([
                    '请提供门店ID',
                    '请提供您的姓名和电话',
                    '是否需要配送？'
                ])
            else:
                response['next_steps'].append('请详细描述您想点的餐品')
            
        elif intent_result.intent == OrderIntent.FIND_STORE:
            if latitude and longitude:
                response['suggested_actions'].append({
                    'action': 'find_stores',
                    'description': '查找附近门店',
                    'tool': 'mcdonalds_find_stores',
                    'parameters': {
                        'latitude': latitude,
                        'longitude': longitude,
                        'radius': 3000
                    }
                })
            else:
                response['next_steps'].append('请提供您的位置信息（经纬度）或大致位置描述')
            
        elif intent_result.intent == OrderIntent.CHECK_ORDER:
            response['next_steps'].append('请提供您的订单号')
            
        elif intent_result.intent == OrderIntent.CANCEL_ORDER:
            response['next_steps'].append('请提供要取消的订单号')
        
        else:
            response['next_steps'] = [
                '我可以帮您：',
                '1. 查看麦当劳菜单',
                '2. 搜索特定产品',
                '3. 点餐下单',
                '4. 查找附近门店',
                '5. 查询订单状态',
                '6. 取消订单',
                '请告诉我您需要什么帮助？'
            ]
        
        return response
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': '智能助手处理失败'
        }


# 示例配置
@tool
async def mcdonalds_get_config() -> Dict:
    """
    获取麦当劳MCP配置信息
    
    Returns:
        配置信息
    """
    return {
        'success': True,
        'config': {
            'api_base_url': client.base_url,
            'token_masked': client.token[:8] + '...' if client.token else '未设置',
            'available_tools': [
                'mcdonalds_view_menu',
                'mcdonalds_search_product',
                'mcdonalds_find_stores',
                'mcdonalds_create_order',
                'mcdonalds_check_order',
                'mcdonalds_cancel_order',
                'mcdonalds_analyze_intent',
                'mcdonalds_get_available_coupons',
                'mcdonalds_suggest_combo',
                'mcdonalds_smart_order_assistant'
            ],
            'example_queries': [
                '查看麦当劳菜单',
                '搜索巨无霸',
                '查找附近的麦当劳',
                '我要点一个巨无霸套餐',
                '我的订单状态',
                '取消订单123456'
            ]
        }
    }


# 测试函数
if __name__ == "__main__":
    import asyncio
    
    async def test_tools():
        print("=== 麦当劳MCP工具测试 ===")
        
        # 测试配置
        print("\n1. 测试配置获取:")
        config = await mcdonalds_get_config()
        print(f"   API地址: {config['config']['api_base_url']}")
        print(f"   可用工具: {len(config['config']['available_tools'])}个")
        
        # 测试意图分析
        print("\n2. 测试意图分析:")
        test_inputs = [
            "我想看看麦当劳有什么吃的",
            "来一个巨无霸",
            "附近有没有麦当劳"
        ]
        
        for test_input in test_inputs:
            result = await mcdonalds_analyze_intent(test_input)
            print(f"   '{test_input}' -> {result['intent']} (置信度: {result['confidence']:.2f})")
        
        # 测试菜单查看
        print("\n3. 测试菜单查看:")
        menu_result = await mcdonalds_view_menu()
        if menu_result['success']:
            print(f"   找到 {menu_result['total_categories']} 个分类")
            for category in menu_result['categories'][:3]:
                print(f"   - {category['name']} ({category['product_count']}个产品)")
        
        # 测试智能助手
        print("\n4. 测试智能助手:")
        assistant_result = await mcdonalds_smart_order_assistant("我要点巨无霸套餐")
        print(f"   意图: {assistant_result['intent']}")
        if 'parsed_order' in assistant_result:
            print(f"   解析的订单: {assistant_result['parsed_order']['summary']}")
        
        print("\n✅ 所有工具测试完成！")
    
    # 运行测试
    asyncio.run(test_tools())