"""
自然语言处理模块
用于解析用户点餐意图和订单项
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class OrderIntent(Enum):
    """订单意图枚举"""
    VIEW_MENU = "view_menu"           # 查看菜单
    SEARCH_PRODUCT = "search_product" # 搜索产品
    CREATE_ORDER = "create_order"     # 创建订单
    FIND_STORE = "find_store"         # 查找门店
    CHECK_ORDER = "check_order"       # 查询订单
    CANCEL_ORDER = "cancel_order"     # 取消订单
    UNKNOWN = "unknown"               # 未知意图


@dataclass
class IntentResult:
    """意图识别结果"""
    intent: OrderIntent
    confidence: float
    entities: Dict[str, str]
    raw_text: str


@dataclass
class OrderItem:
    """订单项"""
    product_name: str
    quantity: int
    customizations: Dict[str, str]
    notes: Optional[str] = None


class McDonaldsNLPProcessor:
    """麦当劳自然语言处理器"""
    
    def __init__(self):
        # 意图关键词映射
        self.intent_keywords = {
            OrderIntent.VIEW_MENU: [
                '菜单', '有什么吃的', '看看吃的', '产品', '有什么',
                '看看菜单', '菜品', '食物', '吃的', '喝什么'
            ],
            OrderIntent.SEARCH_PRODUCT: [
                '找', '搜索', '想吃', '来一份', '想要', '点',
                '有没有', '什么', '哪个', '推荐'
            ],
            OrderIntent.CREATE_ORDER: [
                '点餐', '下单', '我要', '来一个', '订', '购买',
                '买', '要', '给我', '来份', '一份', '两份'
            ],
            OrderIntent.FIND_STORE: [
                '附近', '门店', '在哪里', '麦当劳', '地址',
                '位置', '哪家', '最近', '距离'
            ],
            OrderIntent.CHECK_ORDER: [
                '订单', '状态', '查一下', '查询', '查看',
                '进度', '到哪里了', '好了吗'
            ],
            OrderIntent.CANCEL_ORDER: [
                '取消', '不要了', '退单', '退了', '撤销',
                '不买了', '算了', '退订'
            ]
        }
        
        # 数量词映射
        self.quantity_map = {
            '一': 1, '两': 2, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '一个': 1, '两个': 2, '三个': 3, '四个': 4, '五个': 5,
            '一份': 1, '两份': 2, '三份': 3, '四份': 4, '五份': 5,
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9, '10': 10
        }
        
        # 产品类别关键词
        self.category_keywords = {
            '汉堡': ['汉堡', '堡', '巨无霸', '麦辣鸡腿堡', '安格斯'],
            '薯条': ['薯条', '薯', '薯格'],
            '饮料': ['饮料', '可乐', '雪碧', '果汁', '咖啡', '奶茶', '奶昔'],
            '甜品': ['甜品', '冰淇淋', '派', '麦旋风', '甜筒'],
            '早餐': ['早餐', '粥', '油条', '汉堡', '早餐堡'],
            '套餐': ['套餐', '组合', 'set', 'combo']
        }
        
        # 定制选项关键词
        self.customization_keywords = {
            'size': {
                '大': 'large', '中': 'medium', '小': 'small',
                '加大': 'extra_large', '标准': 'regular'
            },
            'ice': {
                '正常冰': 'normal', '少冰': 'less', '去冰': 'no',
                '热': 'hot', '温': 'warm'
            },
            'sugar': {
                '正常糖': 'normal', '少糖': 'less', '无糖': 'no',
                '半糖': 'half'
            },
            'spicy': {
                '辣': 'spicy', '微辣': 'mild', '不辣': 'no',
                '特辣': 'extra_spicy'
            }
        }
        
        # 麦当劳常见产品名称
        self.common_products = {
            '巨无霸': 'big_mac',
            '麦辣鸡腿堡': 'spicy_chicken_burger',
            '安格斯厚牛堡': 'angus_beef_burger',
            '板烧鸡腿堡': 'grilled_chicken_burger',
            '麦香鱼': 'filet_o_fish',
            '麦乐鸡': 'chicken_mcnuggets',
            '薯条': 'french_fries',
            '可乐': 'coke',
            '雪碧': 'sprite',
            '麦旋风': 'mcflurry',
            '甜筒': 'cone',
            '苹果派': 'apple_pie',
            '红豆派': 'red_bean_pie'
        }
    
    def recognize_intent(self, text: str) -> IntentResult:
        """
        识别用户意图
        
        Args:
            text: 用户输入文本
            
        Returns:
            意图识别结果
        """
        text_lower = text.lower()
        entities = self._extract_entities(text)
        
        # 计算每个意图的匹配分数
        intent_scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            intent_scores[intent] = score
        
        # 找出最高分意图
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        # 计算置信度
        total_keywords = sum(len(keywords) for keywords in self.intent_keywords.values())
        confidence = best_intent[1] / max(len(self.intent_keywords.get(best_intent[0], [])), 1)
        
        # 如果分数为0，则认为是未知意图
        if best_intent[1] == 0:
            best_intent = (OrderIntent.UNKNOWN, 0)
            confidence = 0.0
        
        return IntentResult(
            intent=best_intent[0],
            confidence=min(confidence, 1.0),
            entities=entities,
            raw_text=text
        )
    
    def _extract_entities(self, text: str) -> Dict[str, str]:
        """提取实体信息"""
        entities = {}
        
        # 提取数量
        quantity_match = re.search(r'([一二三四五六七八九十两]个?|[0-9]+个?|一份?|两份?|三份?|四份?|五份?)', text)
        if quantity_match:
            quantity_str = quantity_match.group(1)
            entities['quantity'] = str(self.quantity_map.get(quantity_str, 1))
        
        # 提取产品名称
        for product_cn, product_en in self.common_products.items():
            if product_cn in text:
                entities['product'] = product_en
                entities['product_cn'] = product_cn
                break
        
        # 提取尺寸
        for size_cn, size_en in self.customization_keywords['size'].items():
            if size_cn in text:
                entities['size'] = size_en
                break
        
        # 提取冰量
        for ice_cn, ice_en in self.customization_keywords['ice'].items():
            if ice_cn in text:
                entities['ice'] = ice_en
                break
        
        # 提取糖量
        for sugar_cn, sugar_en in self.customization_keywords['sugar'].items():
            if sugar_cn in text:
                entities['sugar'] = sugar_en
                break
        
        # 提取辣度
        for spicy_cn, spicy_en in self.customization_keywords['spicy'].items():
            if spicy_cn in text:
                entities['spicy'] = spicy_en
                break
        
        # 提取位置信息（简单匹配）
        location_patterns = [
            r'在(.{2,10}?)附近',
            r'到(.{2,10}?)的',
            r'(.{2,10}?)的麦当劳'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                entities['location'] = match.group(1)
                break
        
        return entities
    
    def parse_order_items(self, text: str, menu: List[Dict] = None) -> List[OrderItem]:
        """
        解析订单项
        
        Args:
            text: 用户点餐描述
            menu: 菜单数据（可选，用于产品匹配）
            
        Returns:
            解析后的订单项列表
        """
        items = []
        
        # 分割多个订单项（简单实现）
        # 使用逗号、和、还有等分隔符
        separators = ['，', ',', '、', '和', '还有', '再加']
        
        for sep in separators:
            if sep in text:
                parts = text.split(sep)
                break
        else:
            parts = [text]
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            # 解析单个订单项
            item = self._parse_single_item(part, menu)
            if item:
                items.append(item)
        
        return items
    
    def _parse_single_item(self, text: str, menu: List[Dict] = None) -> Optional[OrderItem]:
        """解析单个订单项"""
        # 提取数量
        quantity = 1
        for q_str, q_num in self.quantity_map.items():
            if q_str in text:
                quantity = q_num
                # 从文本中移除数量词以便后续匹配
                text = text.replace(q_str, '')
                break
        
        # 提取产品名称
        product_name = None
        product_id = None
        
        # 首先尝试匹配常见产品
        for cn_name, en_id in self.common_products.items():
            if cn_name in text:
                product_name = cn_name
                product_id = en_id
                text = text.replace(cn_name, '')
                break
        
        # 如果没有匹配到常见产品，尝试从菜单中匹配
        if not product_name and menu:
            for product in menu:
                if product.get('name') and product['name'] in text:
                    product_name = product['name']
                    product_id = product.get('id')
                    break
        
        if not product_name:
            # 如果还是没找到，使用文本中的关键词
            for category, keywords in self.category_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        product_name = keyword
                        break
                if product_name:
                    break
        
        # 提取定制选项
        customizations = {}
        for option_type, options in self.customization_keywords.items():
            for cn_option, en_option in options.items():
                if cn_option in text:
                    customizations[option_type] = en_option
                    text = text.replace(cn_option, '')
        
        # 提取备注（剩余文本）
        notes = text.strip() if text.strip() else None
        
        if product_name:
            return OrderItem(
                product_name=product_name,
                quantity=quantity,
                customizations=customizations,
                notes=notes
            )
        
        return None
    
    def generate_order_summary(self, items: List[OrderItem], 
                             store_name: str = None) -> str:
        """
        生成订单摘要
        
        Args:
            items: 订单项列表
            store_name: 门店名称
            
        Returns:
            订单摘要文本
        """
        if not items:
            return "订单为空"
        
        summary_parts = []
        
        if store_name:
            summary_parts.append(f"📍 门店：{store_name}")
        
        summary_parts.append("🛒 订单内容：")
        
        for i, item in enumerate(items, 1):
            item_text = f"  {i}. {item.product_name} ×{item.quantity}"
            
            if item.customizations:
                custom_text = []
                for opt_type, opt_value in item.customizations.items():
                    # 将英文选项转回中文显示
                    for cn_opt, en_opt in self.customization_keywords.get(opt_type, {}).items():
                        if en_opt == opt_value:
                            custom_text.append(cn_opt)
                            break
                
                if custom_text:
                    item_text += f" ({'，'.join(custom_text)})"
            
            if item.notes:
                item_text += f" 📝 {item.notes}"
            
            summary_parts.append(item_text)
        
        total_quantity = sum(item.quantity for item in items)
        summary_parts.append(f"\n📊 总计：{len(items)}种产品，{total_quantity}件商品")
        
        return "\n".join(summary_parts)
    
    def suggest_response(self, intent_result: IntentResult) -> str:
        """
        根据意图生成建议回复
        
        Args:
            intent_result: 意图识别结果
            
        Returns:
            建议回复文本
        """
        intent = intent_result.intent
        entities = intent_result.entities
        
        responses = {
            OrderIntent.VIEW_MENU: "好的，我来为您查看麦当劳的菜单。您想查看哪个分类的产品呢？",
            OrderIntent.SEARCH_PRODUCT: "好的，我来帮您搜索产品。您想找什么产品呢？",
            OrderIntent.CREATE_ORDER: "好的，我来帮您点餐。请告诉我您想要什么？",
            OrderIntent.FIND_STORE: "好的，我来帮您查找附近的麦当劳门店。请告诉我您的位置？",
            OrderIntent.CHECK_ORDER: "好的，我来帮您查询订单状态。请提供订单号？",
            OrderIntent.CANCEL_ORDER: "好的，我来帮您取消订单。请提供订单号？",
            OrderIntent.UNKNOWN: "抱歉，我没有理解您的意思。您可以告诉我想要点餐、查看菜单还是查找门店？"
        }
        
        response = responses.get(intent, responses[OrderIntent.UNKNOWN])
        
        # 根据提取的实体丰富回复
        if intent == OrderIntent.CREATE_ORDER and 'product' in entities:
            product_cn = entities.get('product_cn', '')
            quantity = entities.get('quantity', '1')
            response = f"好的，您要{quantity}份{product_cn}是吗？还需要其他什么吗？"
        
        elif intent == OrderIntent.FIND_STORE and 'location' in entities:
            location = entities['location']
            response = f"好的，我来查找{location}附近的麦当劳门店。"
        
        return response


# 使用示例
if __name__ == "__main__":
    processor = McDonaldsNLPProcessor()
    
    test_cases = [
        "我想看看麦当劳有什么吃的",
        "来一个巨无霸套餐",
        "我要大可乐和薯条",
        "附近有没有麦当劳",
        "我的订单到哪里了",
        "取消刚才的订单"
    ]
    
    print("=== NLP处理器测试 ===")
    
    for test_text in test_cases:
        print(f"\n输入: {test_text}")
        
        # 识别意图
        intent_result = processor.recognize_intent(test_text)
        print(f"意图: {intent_result.intent.value} (置信度: {intent_result.confidence:.2f})")
        if intent_result.entities:
            print(f"实体: {intent_result.entities}")
        
        # 生成建议回复
        response = processor.suggest_response(intent_result)
        print(f"回复: {response}")
        
        # 如果是点餐意图，尝试解析订单项
        if intent_result.intent == OrderIntent.CREATE_ORDER:
            items = processor.parse_order_items(test_text)
            if items:
                print("解析的订单项:")
                for item in items:
                    print(f"  - {item.product_name} ×{item.quantity}")
                    if item.customizations:
                        print(f"    定制: {item.customizations}")