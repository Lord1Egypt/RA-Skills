#!/usr/bin/env python3
"""
Telegram Bot - 使用 entities 发送格式化消息（最安全方式）
不依赖 parse_mode，直接控制文本格式
"""

import requests
import json

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # 替换为你的 Bot Token
CHAT_ID = "TARGET_CHAT_ID"          # 替换为目标聊天ID

def send_message_with_entities(text: str, entities: list):
    """
    使用 entities 数组发送格式化消息
    
    entities 格式: [{"type": "bold", "offset": 0, "length": 5}, ...]
    - type: bold, italic, code, pre, text_link, spoiler, etc.
    - offset: 起始位置（UTF-16 编码单位）
    - length: 长度（UTF-16 编码单位）
    - url: (可选，用于 text_link)
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "entities": entities
    }
    
    response = requests.post(url, json=payload)
    return response.json()


def calculate_utf16_length(text: str) -> int:
    """计算 UTF-16 编码长度（Telegram 使用）"""
    return len(text.encode('utf-16-le')) // 2


def build_entities_example():
    """构建一个完整的 entities 示例"""
    
    # 纯文本（没有任何标记符号）
    text = "Hello World! 这是粗体和斜体文本，还有代码片段和链接。"
    
    # 计算每个部分的 UTF-16 长度
    # Telegram 使用 UTF-16 编码单位计算 offset 和 length
    
    entities = [
        # "粗体" 两个字加粗 (offset=15, length=2)
        {
            "type": "bold",
            "offset": 15,
            "length": 2
        },
        # "斜体" 两个字斜体 (offset=18, length=2)  
        {
            "type": "italic",
            "offset": 18,
            "length": 2
        },
        # "代码片段" 四个字代码格式 (offset=24, length=4)
        {
            "type": "code",
            "offset": 24,
            "length": 4
        },
        # "链接" 两个字做成可点击链接 (offset=31, length=2)
        {
            "type": "text_link",
            "offset": 31,
            "length": 2,
            "url": "https://google.com"
        },
        # "Hello World!" 加粗 (offset=0, length=12)
        {
            "type": "bold",
            "offset": 0,
            "length": 12
        }
    ]
    
    return text, entities


def send_complex_message():
    """发送一个复杂的多格式消息"""
    
    # 示例1：嵌套格式（粗体+斜体）
    text1 = "粗体斜体混合文本"
    entities1 = [
        # 整句粗体
        {"type": "bold", "offset": 0, "length": 8},
        # "斜体" 两个字在粗体内再加斜体（嵌套）
        {"type": "italic", "offset": 2, "length": 2}
    ]
    
    # 示例2：带剧透的消息
    text2 = "这是一段普通文本||这是剧透内容||继续普通文本"
    entities2 = [
        # "||这是剧透内容||" 中的内容设为 spoiler
        # 注意：实际 offset 不包含 || 符号
        {"type": "spoiler", "offset": 8, "length": 8}
    ]
    
    # 示例3：代码块
    text3 = """查看下面的代码：
def hello():
    print("Hello World")
运行结果：Hello World"""
    
    entities3 = [
        # 整段代码块
        {"type": "pre", "offset": 9, "length": 37, "language": "python"}
    ]
    
    return [
        (text1, entities1, "嵌套格式示例"),
        (text2, entities2, "剧透示例"),
        (text3, entities3, "代码块示例")
    ]


# ============== 实用工具函数 ==============

def format_helper(text: str, formats: list) -> list:
    """
    辅助函数：简化 entities 创建
    
    formats: [(type, start_idx, end_idx, extra), ...]
    extra: 如 url 等可选参数
    
    示例：
        text = "Hello World"
        formats = [("bold", 0, 5), ("italic", 6, 11)]
    """
    entities = []
    for fmt in formats:
        entity = {
            "type": fmt[0],
            "offset": fmt[1],
            "length": fmt[2] - fmt[1]
        }
        if len(fmt) > 3 and fmt[3]:  # 有额外参数如 url
            entity.update(fmt[3])
        entities.append(entity)
    return entities


def main():
    """主函数：演示发送各种 entities 消息"""
    
    print("=" * 50)
    print("Telegram Entities 消息发送示例")
    print("=" * 50)
    
    # 示例1：基础格式
    text, entities = build_entities_example()
    print(f"\n【示例1】基础格式")
    print(f"纯文本: {text}")
    print(f"Entities: {json.dumps(entities, ensure_ascii=False, indent=2)}")
    
    # 发送（取消注释后使用）
    # result = send_message_with_entities(text, entities)
    # print(f"发送结果: {result}")
    
    # 示例2：使用辅助函数
    print(f"\n【示例2】使用辅助函数")
    text2 = "*星号只是普通字符，不会被解析*"
    # 即使文本中有 * 符号，entities 只作用于指定位置，不受符号影响
    entities2 = format_helper(text2, [
        ("bold", 0, 5),      # "*星号" 加粗
        ("italic", 7, 12),   # "只是" 斜体
        ("code", 14, 18)     # "普通" 代码
    ])
    print(f"纯文本: {text2}")
    print(f"Entities: {json.dumps(entities2, ensure_ascii=False, indent=2)}")
    
    print(f"\n【优点】")
    print("✅ 文本中可以有任意特殊符号（* _ ` 等），不会影响格式")
    print("✅ 不需要转义字符")
    print("✅ 精确控制每个字符的格式")
    print("✅ 支持嵌套格式（粗体内加斜体）")
    
    # 示例3：完整复杂消息
    print(f"\n【示例3】复杂消息")
    examples = send_complex_message()
    for text, entities, desc in examples:
        print(f"\n{desc}:")
        print(f"文本: {text[:50]}...")
        print(f"Entities: {len(entities)} 个")


if __name__ == "__main__":
    main()
