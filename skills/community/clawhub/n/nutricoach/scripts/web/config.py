"""
Web Dashboard Configuration
"""

import os

TEMPLATE_VERSION = "2026-03-29-008"

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOCATION_MAP = {
    '冰箱': 'fridge',
    '冷冻': 'freezer',
    '干货区': 'pantry',
    '台面': 'counter'
}

REVERSE_LOCATION_MAP = {
    'fridge': '冰箱',
    'freezer': '冷冻',
    'pantry': '干货区',
    'counter': '台面'
}

FOOD_STORAGE_DEFAULTS = {
    '鸡胸肉': '冰箱', '牛肉': '冷冻', '猪肉': '冰箱', '羊肉': '冷冻',
    '三文鱼': '冷冻', '虾仁': '冷冻', '鸡蛋': '冰箱',
    '西兰花': '冰箱', '菠菜': '冰箱', '西红柿': '冰箱', '黄瓜': '冰箱',
    '胡萝卜': '冰箱', '土豆': '干货区', '红薯': '干货区',
    '米饭': '冰箱', '燕麦': '干货区', '面条': '干货区',
    '豆腐': '冰箱', '牛奶': '冰箱', '酸奶': '冰箱',
}

# Default values (mirrored from db_schema)
DEFAULTS = {
    'user_height_cm': 170.0,
    'location_shelf_life': {
        'fridge': 7,
        'freezer': 90,
        'pantry': 30,
        'counter': 5,
    },
}
