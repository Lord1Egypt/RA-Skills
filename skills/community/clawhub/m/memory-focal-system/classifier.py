#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Message Classifier - 消息分类器

根据关键词快速判断消息类型，决定是否需要读取记忆。

分类规则：
1. 简单对话 - 直接回复，不读取记忆
2. 任务执行 - 读取相关记忆后执行
3. 情感/偏好相关 - 读取完整记忆
4. 新问题/新信息 - 直接写入记忆
"""

from typing import Tuple, Dict, List


class MessageClassifier:
    """消息分类器"""
    
    def __init__(self):
        # 简单对话关键词（直接回复，不读取记忆）
        self.simple_keywords = [
            "在吗", "在嘛", "你好", "早", "好", "嗯", "哦", "好的", "收到",
            "谢谢", "感谢", "辛苦了", "拜拜", "再见", "晚安", "早安",
            "哈哈", "呵呵", "嘻嘻", "笑死", "666", "👍", "✅", "好嘞",
            "休息", "待命", "待机", "暂停", "停一下", "等一下",
        ]
        
        # 任务执行关键词（读取相关记忆后执行）
        self.task_keywords = [
            "查", "搜索", "找", "下载", "安装", "配置", "设置",
            "发", "发送", "邮件", "报告", "生成", "创建", "写",
            "打开", "关闭", "启动", "停止", "运行", "执行",
        ]
        
        # 情感/偏好相关关键词（读取完整记忆）
        self.memory_keywords = [
            "记得", "记住", "记忆", "上次", "之前", "以前", "曾经",
            "偏好", "喜欢", "讨厌", "不喜欢", "习惯", "规则",
            "我说", "我说过", "你记得", "别忘了",
        ]
        
        # 新信息关键词（直接写入记忆）
        self.new_info_keywords = [
            "新", "新增", "添加", "记录", "保存", "存一下",
            "记下来", "写进去", "以后", "从现在开始", "以后都",
        ]
        
        # 否定词关键词（不写入记忆）
        self.negation_keywords = [
            "别记住", "不要记", "别记", "忘了", "忘掉",
            "不用记", "无需记", "不必记", "别存", "不要存",
            "别写", "不要写", "别记录", "不要记录",
            "别用", "不要用", "别开启", "不要开启",
            "别用这", "别用这个", "不要用这", "不要用这个",
        ]
    
    def classify(self, message: str) -> Tuple[str, Dict]:
        """
        分类消息（权重计分版）
        
        Returns:
            (category, config)
            category: "simple" | "task" | "memory" | "new_info"
            config: {
                "load_focal": bool,     # 是否加载 memory-focal
                "write_memory": bool,   # 是否写入新记忆
            }
        """
        message_lower = message.lower()
        
        # 1. 否定词优先（直接返回 simple）
        for keyword in self.negation_keywords:
            if keyword in message_lower:
                return "simple", {
                    "load_focal": False,
                    "write_memory": False,
                }
        
        # 2. 权重计分
        scores = {
            "simple": 0,
            "task": 0,
            "memory": 0,
            "new_info": 0
        }
        
        # 简单对话关键词
        for keyword in self.simple_keywords:
            if keyword in message_lower:
                scores["simple"] += 1
        
        # 任务执行关键词
        for keyword in self.task_keywords:
            if keyword in message_lower:
                scores["task"] += 1
        
        # 情感/偏好关键词
        for keyword in self.memory_keywords:
            if keyword in message_lower:
                scores["memory"] += 1
        
        # 新信息关键词
        for keyword in self.new_info_keywords:
            if keyword in message_lower:
                scores["new_info"] += 1
        
        # 3. 取最高分（如果有平局，优先级：new_info > memory > task > simple）
        max_score = max(scores.values())
        
        if max_score == 0:
            # 无匹配，默认简单对话
            return "simple", {
                "load_focal": False,
                "write_memory": False,
            }
        
        # 按优先级排序的类别
        priority_order = ["new_info", "memory", "task", "simple"]
        
        for category in priority_order:
            if scores[category] == max_score:
                return self._get_category_config(category)
        
        # fallback
        return "simple", {
            "load_focal": False,
            "write_memory": False,
        }
    
    def _get_category_config(self, category: str) -> Tuple[str, Dict]:
        """根据分类返回配置"""
        configs = {
            "simple": {
                "load_focal": False,
                "write_memory": False,
            },
            "task": {
                "load_focal": True,
                "write_memory": False,
            },
            "memory": {
                "load_focal": True,
                "write_memory": True,
            },
            "new_info": {
                "load_focal": True,
                "write_memory": True,
            }
        }
        
        return category, configs.get(category, configs["simple"])
    
    def should_write_memory(self, message: str) -> bool:
        """
        判断是否需要写入记忆
        
        Args:
            message: 用户消息
        
        Returns:
            bool - 是否需要写入
        """
        message_lower = message.lower()
        
        # 否定词优先
        for keyword in self.negation_keywords:
            if keyword in message_lower:
                return False
        
        # 包含记忆相关关键词
        for keyword in self.memory_keywords:
            if keyword in message_lower:
                return True
        
        # 包含新信息关键词
        for keyword in self.new_info_keywords:
            if keyword in message_lower:
                return True
        
        # 用户明确要求记住
        if "记住" in message or "记下来" in message or "存一下" in message:
            return True
        
        return False
    
    def get_memory_priority(self, message: str) -> str:
        """
        获取记忆优先级
        
        Returns:
            "high" | "medium" | "low"
        """
        # 高优先级：用户的偏好、规则、决策
        high_keywords = ["规则", "偏好", "禁止", "必须", "一定", "永远"]
        for keyword in high_keywords:
            if keyword in message:
                return "high"
        
        # 中优先级：任务相关、配置相关
        medium_keywords = ["配置", "设置", "任务", "工作", "项目"]
        for keyword in medium_keywords:
            if keyword in message:
                return "medium"
        
        # 低优先级：其他
        return "low"


# 测试
if __name__ == "__main__":
    classifier = MessageClassifier()
    
    test_cases = [
        "在吗",
        "用户偏好早上 8 点起床",
        "查一下配置",
        "记得上次说的规则吗",
        "新增一条：以后每天晚上提醒我断电",
        "谢谢",
        "帮我生成报告",
        "记住了，以后都这样",
        "记住，以后别用这功能了",
    ]
    
    print("🧪 消息分类测试\n")
    for msg in test_cases:
        category, config = classifier.classify(msg)
        should_write = classifier.should_write_memory(msg)
        priority = classifier.get_memory_priority(msg)
        print(f"消息：{msg}")
        print(f"  分类：{category}")
        print(f"  配置：{config}")
        print(f"  写入：{should_write}")
        print(f"  优先级：{priority}")
        print()
