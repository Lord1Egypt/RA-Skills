#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Memory Retrieval Trigger
Only retrieve memories when needed to reduce API calls and costs
"""

import re
from typing import List, Tuple

# ============ 配置区域 ============

# 触发检索的关键词（包含这些词就检索）
TRIGGER_KEYWORDS = [
    "我记得", "之前", "说过", "提过", "那个", "上次",
    "以前", "曾经", "记得", "想起", "回忆",
    "查一下", "查找", "搜索", "找",
]

# 跳过检索的关键词（包含这些词就不检索）
SKIP_KEYWORDS = [
    "你好", "在吗", "在嘛", "早", "早安", "晚安", "拜拜", "再见",
    "吃了吗", "吃没吃", "在干嘛", "干嘛呢", "忙什么",
    "谢谢", "感谢", "辛苦了",
    "好的", "收到", "明白", "知道了",
    "哈哈", "呵呵", "嘻嘻", "嗯嗯",
]

# 问题模式（匹配这些模式就检索）
QUESTION_PATTERNS = [
    r".*\?.*",      # 包含？
    r".*吗.*",      # 包含吗
    r".*什么.*",    # 包含什么
    r".*怎么.*",    # 包含怎么
    r".*为什么.*",  # 包含为什么
    r".*哪里.*",    # 包含哪里
    r".*何时.*",    # 包含何时
    r".*多少.*",    # 包含多少
]

# 配置选项
CONFIG = {
    "min_length": 5,        # 最小消息长度（< 5 字不检索）
    "max_length": 500,      # 最大消息长度（> 500 字截断）
    "enable_cache": True,   # 启用缓存
    "debug": False,         # 调试模式（打印详细日志）
}

# ============ 核心逻辑 ============

class SmartRetrievalTrigger:
    """智能检索触发器"""
    
    def __init__(self, config: dict = None):
        self.config = {**CONFIG, **(config or {})}
        self.stats = {
            "total": 0,
            "triggered": 0,
            "skipped": 0,
        }
    
    def should_retrieve(self, message: str) -> Tuple[bool, str]:
        """
        判断是否需要检索记忆
        
        Args:
            message: 用户消息
        
        Returns:
            (是否检索，原因)
        """
        message = message.strip()
        self.stats["total"] += 1
        
        # 1. 检查空消息
        if not message:
            return False, "空消息"
        
        # 2. 检查消息长度
        if len(message) < self.config["min_length"]:
            return False, f"消息太短（{len(message)} < {self.config['min_length']}）"
        
        if len(message) > self.config["max_length"]:
            message = message[:self.config["max_length"]]
            if self.config["debug"]:
                print(f"[DEBUG] 消息截断：{len(message)} -> {self.config['max_length']}")
        
        # 3. 检查跳过关键词（问候、闲聊）
        for keyword in SKIP_KEYWORDS:
            if keyword in message:
                self.stats["skipped"] += 1
                if self.config["debug"]:
                    print(f"[DEBUG] 跳过检索（关键词 '{keyword}'）：'{message[:50]}...'")
                return False, f"跳过关键词：{keyword}"
        
        # 4. 检查触发关键词（记忆相关）
        for keyword in TRIGGER_KEYWORDS:
            if keyword in message:
                self.stats["triggered"] += 1
                if self.config["debug"]:
                    print(f"[DEBUG] 触发检索（关键词 '{keyword}'）：'{message[:50]}...'")
                return True, f"触发关键词：{keyword}"
        
        # 5. 检查问题模式
        for pattern in QUESTION_PATTERNS:
            if re.match(pattern, message):
                self.stats["triggered"] += 1
                if self.config["debug"]:
                    print(f"[DEBUG] 触发检索（问题模式 '{pattern}'）：'{message[:50]}...'")
                return True, f"问题模式：{pattern}"
        
        # 6. 长消息触发（> 15 字）
        if len(message) > 15:
            self.stats["triggered"] += 1
            if self.config["debug"]:
                print(f"[DEBUG] 触发检索（长消息 {len(message)} > 15）：'{message[:50]}...'")
            return True, f"长消息：{len(message)} 字"
        
        # 7. 默认不检索
        self.stats["skipped"] += 1
        if self.config["debug"]:
            print(f"[DEBUG] 默认跳过：'{message[:50]}...'")
        return False, "默认跳过"
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total = self.stats["total"]
        if total == 0:
            return self.stats
        
        return {
            **self.stats,
            "trigger_rate": f"{self.stats['triggered']/total*100:.1f}%",
            "skip_rate": f"{self.stats['skipped']/total*100:.1f}%",
            "estimated_savings": f"{self.stats['skipped']/total*100:.0f}%",
        }
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "total": 0,
            "triggered": 0,
            "skipped": 0,
        }


# ============ 全局实例 ============

_trigger = None

def get_trigger() -> SmartRetrievalTrigger:
    """获取或创建触发器实例"""
    global _trigger
    if _trigger is None:
        _trigger = SmartRetrievalTrigger()
    return _trigger


def should_retrieve(message: str, debug: bool = False) -> bool:
    """
    便捷函数：判断是否需要检索
    
    Args:
        message: 用户消息
        debug: 是否打印调试信息
    
    Returns:
        True 如果需要检索，False 否则
    """
    trigger = get_trigger()
    if debug:
        trigger.config["debug"] = True
    
    should_retrieve, reason = trigger.should_retrieve(message)
    
    if debug:
        print(f"[SMART] 消息：'{message[:50]}...' -> {'检索' if should_retrieve else '跳过'} ({reason})")
    
    return should_retrieve


# ============ 测试 ============

if __name__ == "__main__":
    print("=" * 70)
    print("Smart Retrieval Trigger Test")
    print("=" * 70)
    
    trigger = SmartRetrievalTrigger(debug=True)
    
    # 测试用例
    test_cases: List[Tuple[str, bool]] = [
        # 应该跳过的
        ("你好", False),
        ("在吗", False),
        ("早", False),
        ("吃了吗", False),
        ("在干嘛", False),
        ("谢谢", False),
        ("好的", False),
        ("哈哈", False),
        ("hi", False),
        
        # 应该触发的
        ("我记得你说过瀑布的事情", True),
        ("之前提到的 TTS 怎么用", True),
        ("那个天台瀑布在哪里", True),
        ("上次说的阿里云配置好了吗", True),
        ("帮我查一下之前的对话", True),
        ("TTS 应该怎么用？", True),
        ("阿里云 Embedding 配置好了吗？", True),
        ("为什么之前会失败", True),
        ("什么是向量数据库", True),
        ("今天天气不错，适合出去走走看看风景", True),  # 长消息
    ]
    
    print("\n[测试用例]")
    correct = 0
    total = len(test_cases)
    
    for message, expected in test_cases:
        result, reason = trigger.should_retrieve(message)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            correct += 1
        
        print(f"{status} '{message}' -> {'检索' if result else '跳过'} ({reason})")
        if result != expected:
            print(f"   期望：{'检索' if expected else '跳过'}")
    
    # 统计
    stats = trigger.get_stats()
    print(f"\n[统计]")
    print(f"  总数：{stats['total']}")
    print(f"  触发：{stats['triggered']}")
    print(f"  跳过：{stats['skipped']}")
    print(f"  触发率：{stats['trigger_rate']}")
    print(f"  跳过率：{stats['skip_rate']}")
    print(f"  预计节省：{stats['estimated_savings']}")
    
    # 准确率
    accuracy = correct / total * 100
    print(f"\n[准确率]")
    print(f"  {correct}/{total} = {accuracy:.1f}%")
    
    if accuracy >= 90:
        print("  ✅ 优秀！")
    elif accuracy >= 80:
        print("  👍 良好！")
    else:
        print("  ⚠️ 需要调整规则")
    
    print("\n" + "=" * 70)
