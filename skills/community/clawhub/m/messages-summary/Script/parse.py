#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书消息解析脚本
用于解析和处理飞书消息数据，生成结构化的摘要信息
"""

import json
from typing import List, Dict, Any


class MessageParser:
    """飞书消息解析器"""

    def __init__(self):
        self.messages = []

    def parse_messages(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        解析消息列表，提取关键信息

        Args:
            messages: 消息列表，每个消息包含 sender, content, timestamp 等字段

        Returns:
            包含摘要信息的字典
        """
        self.messages = messages

        summary = {
            "total_messages": len(messages),
            "participants": self._extract_participants(),
            "key_topics": self._extract_topics(),
            "action_items": self._extract_action_items(),
            "time_range": self._get_time_range(),
        }

        return summary

    def _extract_participants(self) -> List[str]:
        """提取参与者列表"""
        participants = set()
        for msg in self.messages:
            if "sender" in msg:
                participants.add(msg["sender"])
        return list(participants)

    def _extract_topics(self) -> List[str]:
        """提取关键话题（简单实现，可扩展）"""
        # TODO: 实现更智能的话题提取逻辑
        return []

    def _extract_action_items(self) -> List[Dict[str, str]]:
        """提取待办事项"""
        action_items = []
        for msg in self.messages:
            content = msg.get("content", "")
            # 简单匹配包含 "TODO" 或 "待办" 的消息
            if "TODO" in content or "待办" in content:
                action_items.append({
                    "content": content,
                    "sender": msg.get("sender", ""),
                    "timestamp": msg.get("timestamp", ""),
                })
        return action_items

    def _get_time_range(self) -> Dict[str, str]:
        """获取消息的时间范围"""
        if not self.messages:
            return {"start": "", "end": ""}

        timestamps = [msg.get("timestamp", "") for msg in self.messages if msg.get("timestamp")]
        if not timestamps:
            return {"start": "", "end": ""}

        return {
            "start": min(timestamps),
            "end": max(timestamps),
        }


def main():
    """主函数示例"""
    # 示例数据
    sample_messages = [
        {
            "sender": "张三",
            "content": "我们需要在本周五前完成这个功能 TODO",
            "timestamp": "2026-04-01 10:00:00",
        },
        {
            "sender": "李四",
            "content": "好的，我负责前端部分",
            "timestamp": "2026-04-01 10:05:00",
        },
    ]

    parser = MessageParser()
    summary = parser.parse_messages(sample_messages)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


# ============================================================================
# 测试说明 (Test Documentation)
# ============================================================================
"""
## 测试方式

### 1. 单元测试
运行单元测试（需要先安装 pytest）：
```bash
pip install pytest
pytest test_parse.py -v
```

### 2. 手动测试
直接运行脚本查看示例输出：
```bash
python parse.py
```

### 3. 集成测试
使用真实飞书消息数据测试：
```python
from parse import MessageParser

# 从飞书API获取的消息数据
real_messages = [
    # ... 真实消息数据
]

parser = MessageParser()
result = parser.parse_messages(real_messages)
print(result)
```

## 测试用例

### 测试用例 1: 空消息列表
输入：[]
期望输出：total_messages = 0, participants = []

### 测试用例 2: 单条消息
输入：包含1条消息的列表
期望输出：正确解析sender、content、timestamp

### 测试用例 3: 多条消息含待办事项
输入：包含 "TODO" 或 "待办" 关键词的消息
期望输出：action_items 列表不为空

### 测试用例 4: 时间范围计算
输入：包含不同时间戳的消息列表
期望输出：正确的 start 和 end 时间

## 性能测试

测试大量消息的处理性能：
```python
import time

# 生成 10000 条测试消息
large_messages = [
    {
        "sender": f"user_{i % 100}",
        "content": f"Message content {i}",
        "timestamp": f"2026-04-01 {i % 24:02d}:00:00",
    }
    for i in range(10000)
]

parser = MessageParser()
start_time = time.time()
result = parser.parse_messages(large_messages)
elapsed = time.time() - start_time

print(f"处理 {len(large_messages)} 条消息耗时: {elapsed:.2f} 秒")
```

## Mock 数据生成

生成测试用的 Mock 数据：
```python
def generate_mock_messages(count: int) -> List[Dict[str, Any]]:
    import random
    from datetime import timedelta

    senders = ["张三", "李四", "王五", "赵六"]
    contents = [
        "这个功能什么时候上线？",
        "TODO: 完成代码审查",
        "我负责这部分",
        "待办：更新文档",
        "会议改到明天下午",
    ]

    base_time = datetime(2026, 4, 1, 9, 0, 0)
    messages = []

    for i in range(count):
        msg = {
            "sender": random.choice(senders),
            "content": random.choice(contents),
            "timestamp": (base_time + timedelta(minutes=i*5)).strftime("%Y-%m-%d %H:%M:%S"),
        }
        messages.append(msg)

    return messages
```

## 注意事项

1. **权限验证**：测试时确保有飞书消息的访问权限
2. **数据隐私**：测试数据中不要包含真实的敏感信息
3. **边界条件**：测试空值、特殊字符、超长文本等情况
4. **性能监控**：大量消息时注意内存和时间开销
5. **编码问题**：确保正确处理中英文混合内容
"""
