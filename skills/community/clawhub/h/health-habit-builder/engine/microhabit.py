"""
Health Habit Builder - Micro Habit Generator
健康习惯养成师 - 微习惯生成器
"""

from typing import Dict, Any, List


def generate_microhabits(habit_name: str, difficulty: int) -> List[Dict[str, Any]]:
    """
    生成微习惯序列
    
    Args:
        habit_name: 习惯名称
        difficulty: 难度等级 (1-10)
        
    Returns:
        微习惯序列
    """
    microhabits = []
    
    # 第一阶段：启动期 (1-2周)
    gateway_task = _get_gateway_task(habit_name)
    microhabits.append({
        "week": "第1周",
        "focus": "建立仪式感",
        "dailyTask": gateway_task,
        "successCriteria": "连续7天完成",
        "reward": "内在：完成后的成就感；外在：解锁下一阶段"
    })
    
    # 第二阶段：学习期 (3-4周)
    microhabits.append({
        "week": "第2周",
        "focus": "适应节奏",
        "dailyTask": _get_level2_task(habit_name),
        "successCriteria": "完成率>=80%",
        "reward": "内在：感受到进步；外在：成就徽章"
    })
    
    # 第三阶段：整合期 (5-8周)
    if difficulty <= 5:
        microhabits.append({
            "week": "第3-4周",
            "focus": "形成习惯",
            "dailyTask": _get_standard_task(habit_name),
            "successCriteria": "能够自然完成，不需要提醒",
            "reward": "习惯初步形成"
        })
    else:
        microhabits.append({
            "week": "第3-4周",
            "focus": "延长时间/强度",
            "dailyTask": _get_level3_task(habit_name),
            "successCriteria": "连续14天稳定完成",
            "reward": "进入巩固期"
        })
    
    # 第四阶段：维持期 (9-12周)
    microhabits.append({
        "week": "第5-8周",
        "focus": "巩固与自动化",
        "dailyTask": _get_maintenance_task(habit_name),
        "successCriteria": "不需意志力即可完成",
        "reward": "习惯进入自动化阶段"
    })
    
    return microhabits


def _get_gateway_task(habit_name: str) -> str:
    """获取入门级微习惯"""
    gateways = {
        "冥想": "坐下，深呼吸3次",
        "运动": "穿上运动鞋",
        "跑步": "系好鞋带",
        "健身": "做1个俯卧撑",
        "瑜伽": "铺开瑜伽垫",
        "阅读": "打开书到第一页",
        "写作": "写下一句话",
        "早起": "比平时早5分钟起床",
        "早睡": "提前10分钟躺在床上",
        "喝水": "喝一口水",
        "学习": "打开学习资料",
        "英语": "背诵一个单词",
    }
    
    for key, task in gateways.items():
        if key in habit_name:
            return task
    
    return f"做{habit_name}相关的最小行动"


def _get_level2_task(habit_name: str) -> str:
    """获取第二级微习惯"""
    tasks = {
        "冥想": "引导冥想1分钟",
        "运动": "做5分钟热身",
        "跑步": "慢跑1分钟",
        "健身": "做3组简单动作",
        "瑜伽": "做1个基础体式",
        "阅读": "阅读1页",
        "写作": "写50字",
        "早起": "早起10分钟",
        "早睡": "提前15分钟上床",
        "喝水": "喝半杯水",
        "学习": "学习5分钟",
        "英语": "学习3个单词",
    }
    
    for key, task in tasks.items():
        if key in habit_name:
            return task
    
    return f"完成{habit_name}的基础版本"


def _get_level3_task(habit_name: str) -> str:
    """获取第三级微习惯"""
    tasks = {
        "冥想": "冥想3分钟",
        "运动": "运动10分钟",
        "跑步": "跑步10分钟",
        "健身": "完成15分钟训练",
        "瑜伽": "练习10分钟",
        "阅读": "阅读10分钟",
        "写作": "写100字",
        "早起": "早起15分钟",
        "早睡": "提前20分钟上床",
        "喝水": "喝完一杯水",
        "学习": "学习15分钟",
        "英语": "学习5个单词并造句",
    }
    
    for key, task in tasks.items():
        if key in habit_name:
            return task
    
    return f"完成{habit_name}的标准版本"


def _get_standard_task(habit_name: str) -> str:
    """获取标准微习惯"""
    tasks = {
        "冥想": "冥想5-10分钟",
        "运动": "运动15-20分钟",
        "跑步": "跑步20分钟",
        "健身": "完成30分钟训练",
        "瑜伽": "练习15-20分钟",
        "阅读": "阅读20页",
        "写作": "写200字",
        "早起": "按时早起",
        "早睡": "按时入睡",
        "喝水": "分次喝完8杯水",
        "学习": "学习30分钟",
        "英语": "学习并复习10个单词",
    }
    
    for key, task in tasks.items():
        if key in habit_name:
            return task
    
    return f"完成{habit_name}的正常版本"


def _get_maintenance_task(habit_name: str) -> str:
    """获取维持期任务"""
    return f"保持{habit_name}的习惯，尝试优化和调整"
