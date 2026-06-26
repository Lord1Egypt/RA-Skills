#!/usr/bin/env python3
"""
宠物话术生成器
根据宠物人格配置动态生成话术，支持自定义和扩展
"""

import json
import random
from pathlib import Path
from datetime import datetime

class PetMessageGenerator:
    """宠物话术生成器"""
    
    def __init__(self, pet_config, user_preferences=None):
        """
        初始化话术生成器
        
        Args:
            pet_config: 宠物人格配置（JSON）
            user_preferences: 用户偏好（可选）
        """
        self.pet = pet_config
        self.user_prefs = user_preferences or {}
        self.template_path = Path(__file__).parent.parent / "templates"
        
        # 加载自定义话术模板（如果存在）
        self.custom_templates = self.load_custom_templates()
    
    def load_custom_templates(self):
        """加载用户自定义话术模板"""
        custom_path = self.template_path / f"{self.pet['pet_id']}_custom.json"
        
        if custom_path.exists():
            with open(custom_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {}
    
    def generate(self, trigger_type, data=None):
        """
        生成宠物话术
        
        Args:
            trigger_type: 触发类型（greeting_morning, market_down, etc.）
            data: 动态数据（如{percent: 3.2}）
        
        Returns:
            生成的话术字符串
        """
        # 1. 获取话术模板（优先级：自定义 > 默认）
        template = self.get_template(trigger_type)
        
        if not template:
            return self.generate_fallback(trigger_type, data)
        
        # 2. 填充动态数据
        if data:
            try:
                message = template.format(**data)
            except KeyError as e:
                print(f"模板数据缺失：{e}")
                message = template
        else:
            message = template
        
        # 3. 应用沟通风格
        style = self.pet['communication_style']
        message = self.apply_communication_style(message, style)
        
        # 4. 应用详细度
        verbosity = self.pet.get('verbosity_level') or self.pet.get('personality_traits', {}).get('verbosity_level', 50)
        message = self.apply_verbosity(message, verbosity, trigger_type, data)
        
        # 5. 应用用户偏好
        message = self.apply_user_preferences(message)
        
        return message
    
    def get_template(self, trigger_type):
        """获取话术模板（支持自定义）"""
        # 优先使用自定义模板
        if trigger_type in self.custom_templates:
            templates = self.custom_templates[trigger_type]
            if isinstance(templates, list):
                return random.choice(templates)
            return templates
        
        # 使用默认模板
        if 'talk_templates' in self.pet:
            templates = self.pet['talk_templates'].get(trigger_type)
            if isinstance(templates, list):
                return random.choice(templates)
            return templates
        
        return None
    
    def apply_communication_style(self, message, style):
        """应用沟通风格"""
        style_handlers = {
            'warm': self.add_warm_tone,
            'calm': self.add_calm_tone,
            'rational': self.add_rational_tone,
            'decisive': self.add_decisive_tone,
            'witty': self.add_witty_tone,
            'friendly': self.add_friendly_tone,
            'visionary': self.add_visionary_tone,
            'energetic': self.add_energetic_tone
        }
        
        handler = style_handlers.get(style, lambda x: x)
        return handler(message)
    
    def add_warm_tone(self, message):
        """添加温暖语气"""
        warm_words = ['~', '哦', '啦', '呀', '☀️', '🌰', '💕']
        if not any(word in message for word in warm_words):
            message += random.choice(['~', '哦'])
        return message
    
    def add_calm_tone(self, message):
        """添加平静语气"""
        # 平静风格：简短，少表情，多句号
        message = message.replace('!', '。')
        message = message.replace('~', '。')
        # 移除过多表情
        emojis = ['🎉', '😱', '💪', '🔥']
        for emoji in emojis:
            message = message.replace(emoji, '')
        return message
    
    def add_rational_tone(self, message):
        """添加理性语气"""
        # 理性风格：数据支撑，逻辑清晰
        if '数据' not in message and '历史' not in message:
            message += " 数据不会说谎。"
        return message
    
    def add_decisive_tone(self, message):
        """添加果断语气"""
        # 果断风格：简短，有力，多感叹号
        if not message.endswith('!'):
            message += '！'
        return message
    
    def add_witty_tone(self, message):
        """添加机智语气"""
        witty_words = ['~', '哈哈', '机智如我', '🦊']
        if not any(word in message for word in witty_words):
            message += ' 机智如我~'
        return message
    
    def add_friendly_tone(self, message):
        """添加友好语气"""
        friendly_words = ['呀', '呢', '~', '🐬', '🌊']
        if not any(word in message for word in friendly_words):
            message += '呀~'
        return message
    
    def add_visionary_tone(self, message):
        """添加远见语气"""
        visionary_words = ['未来', '愿景', '🦄', '🚀']
        if not any(word in message for word in visionary_words):
            message += ' 未来已来！'
        return message
    
    def add_energetic_tone(self, message):
        """添加活力语气"""
        energetic_words = ['！', '🐎', '💨', '冲']
        if not any(word in message for word in energetic_words):
            message += ' 换道超车！'
        return message
    
    def apply_verbosity(self, message, verbosity, trigger_type, data=None):
        """应用详细度"""
        if verbosity < 30:
            # 简短风格：截断过长消息
            if len(message) > 30:
                message = message[:30] + '...'
        elif verbosity > 70:
            # 详细风格：添加额外信息
            extra_info = self.get_extra_info(trigger_type, data)
            if extra_info:
                message += f"\n\n{extra_info}"
        
        return message
    
    def get_extra_info(self, trigger_type, data=None):
        """获取额外信息（用于详细风格）"""
        extra_templates = {
            'market_down': "历史数据显示，跌幅>3% 后 3 个月内涨回的概率是 91.6%。",
            'market_up': "继续持有，让复利发挥作用。",
            'sip_reminder': "定投的核心是纪律，不是择时。",
            'greeting_morning': "今日宜：定投、学习、保持耐心。"
        }
        
        return extra_templates.get(trigger_type, "")
    
    def apply_user_preferences(self, message):
        """应用用户偏好"""
        # 如果用户讨厌专业术语
        if self.user_prefs.get('hates_jargon', False):
            jargon_map = {
                '估值': '价格便宜程度',
                'PE': '回本年限',
                'PB': '股价相对于净资产的倍数',
                '回撤': '从最高点跌了多少'
            }
            for jargon, plain in jargon_map.items():
                message = message.replace(jargon, plain)
        
        # 如果用户喜欢数据支撑
        if self.user_prefs.get('prefers_data', False):
            if '数据' not in message and '历史' not in message:
                message += "（数据支撑）"
        
        return message
    
    def generate_fallback(self, trigger_type, data=None):
        """降级话术（当模板缺失时）"""
        fallback_templates = {
            'greeting_morning': "早上好！",
            'greeting_night': "晚安！",
            'market_down': "市场波动，保持冷静。",
            'market_up': "市场上涨，继续持有。",
            'sip_reminder': "定投日到了。",
            'achievement': "恭喜你！"
        }
        
        base_message = fallback_templates.get(trigger_type, "...")
        
        if data:
            try:
                base_message = base_message.format(**data)
            except KeyError:
                pass
        
        return base_message
    
    def add_emoji(self, message):
        """根据宠物添加 emoji"""
        emoji_map = {
            'songguo': '🐿️',
            'wugui': '🐢',
            'maotouying': '🦉',
            'lang': '🐺',
            'daxiang': '🐘',
            'ying': '🦅',
            'huli': '🦊',
            'haitun': '🐬',
            'shizi': '🦁',
            'mayi': '🐜',
            'luotuo': '🐪',
            'dunjiaoshou': '🦄',
            'junma': '🐎'
        }
        
        pet_emoji = emoji_map.get(self.pet['pet_id'], '🐾')
        
        # 如果消息中已有 emoji，不添加
        if any(c in message for c in '🐿️🐢🦉🐺🐘🦅🦊🐬🦁🐜🐪🦄🐎'):
            return message
        
        return f"{pet_emoji} {message}"


def test_generator():
    """测试话术生成器"""
    # 加载松果配置
    pet_path = Path(__file__).parent / '..' / 'pets' / "pets" / "songguo.json"
    with open(pet_path, 'r', encoding='utf-8') as f:
        songguo_config = json.load(f)
    
    # 创建生成器
    generator = PetMessageGenerator(songguo_config)
    
    # 测试不同场景
    print("🐿️ 松果的话术测试：\n")
    
    scenarios = [
        ('greeting_morning', None),
        ('greeting_night', None),
        ('market_down', {'percent': 3.2}),
        ('market_up', {'percent': 2.5}),
        ('sip_reminder', None),
        ('achievement', {'achievement': '连续打卡 7 天'})
    ]
    
    for trigger_type, data in scenarios:
        message = generator.generate(trigger_type, data)
        message = generator.add_emoji(message)
        print(f"{trigger_type}: {message}")
    
    # 测试慢慢
    print("\n" + "="*50 + "\n")
    
    wugui_path = Path(__file__).parent.parent / "pets" / "wugui.json"
    with open(wugui_path, 'r', encoding='utf-8') as f:
        wugui_config = json.load(f)
    
    generator = PetMessageGenerator(wugui_config)
    
    print("🐢 慢慢的话术测试：\n")
    
    for trigger_type, data in scenarios:
        message = generator.generate(trigger_type, data)
        message = generator.add_emoji(message)
        print(f"{trigger_type}: {message}")


if __name__ == "__main__":
    test_generator()
