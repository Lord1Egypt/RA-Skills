#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模态对话示例
演示如何使用  进行多模态对话
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import


def simple_text_conversation():
    """简单文本对话"""
    print("=== 简单文本对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    # 第一轮对话
    print("用户: 你好，请介绍一下自己")
    response1 = conversation.chat("你好，请介绍一下自己")
    print(f"AI: {response1}\n")

    # 第二轮对话
    print("用户: 你能帮我做什么？")
    response2 = conversation.chat("你能帮我做什么？")
    print(f"AI: {response2}\n")

    # 第三轮对话
    print("用户: 给我一个使用示例")
    response3 = conversation.chat("给我一个使用示例")
    print(f"AI: {response3}\n")


def image_text_conversation():
    """图片+文本对话"""
    print("\n=== 图片+文本对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    image_path = "path/to/image.jpg"

    # 第一轮：发送图片
    print("用户: 请分析这张图片")
    response1 = conversation.chat(
        message="请详细分析这张图片，包括内容、风格、情感等",
        image_path=image_path
    )
    print(f"AI: {response1}\n")

    # 第二轮：追问
    print("用户: 基于分析结果，给出营销建议")
    response2 = conversation.chat("基于上面的分析，给出一些营销建议")
    print(f"AI: {response2}\n")

    # 第三轮：深化
    print("用户: 能否再具体一点？")
    response3 = conversation.chat("能否给出更具体、可执行的营销方案？")
    print(f"AI: {response3}\n")


def multi_image_conversation():
    """多图片对话"""
    print("\n=== 多图片对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    images = [
        "path/to/image1.jpg",
        "path/to/image2.jpg",
        "path/to/image3.jpg"
    ]

    # 逐个发送图片
    for i, image_path in enumerate(images, 1):
        print(f"\n用户: 发送第 {i} 张图片，请分析")
        response = conversation.chat(
            message=f"这是第{i}张图片，请分析其内容和特点",
            image_path=image_path
        )
        print(f"AI: {response}")

    # 最后综合分析
    print("\n用户: 请综合分析这组图片")
    final_response = conversation.chat(
        "请综合分析以上所有图片，找出它们之间的关联和差异"
    )
    print(f"AI: {final_response}")


def brainstorming_session():
    """头脑风暴对话"""
    print("\n=== 头脑风暴对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    print("开始头脑风暴：新产品创意\n")

    # 第一步：确定方向
    print("[阶段 1] 确定产品方向")
    response1 = conversation.chat(
        "我想开发一款面向大学生的App，帮我 brainstorm 一些创意方向"
    )
    print(f"AI: {response1}\n")

    # 第二步：深入探讨
    print("[阶段 2] 深入探讨某个方向")
    response2 = conversation.chat(
        "我对第二个方向很感兴趣，请详细展开，包括核心功能、目标用户、商业模式等"
    )
    print(f"AI: {response2}\n")

    # 第三步：可行性分析
    print("[阶段 3] 可行性分析")
    response3 = conversation.chat(
        "请分析这个创意的技术可行性、市场竞争度和潜在风险"
    )
    print(f"AI: {response3}\n")

    # 第四步：行动建议
    print("[阶段 4] 行动建议")
    response4 = conversation.chat(
        "基于以上分析，请给出具体的行动计划和里程碑"
    )
    print(f"AI: {response4}\n")


def creative_writing_session():
    """创意写作对话"""
    print("\n=== 创意写作对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    print("开始创意写作：短篇小说\n")

    # 第一步：设定背景
    print("[步骤 1] 设定故事背景")
    response1 = conversation.chat(
        "我想写一个科幻短篇故事，背景设定在2050年的上海。请帮我构思世界观和背景设定。"
    )
    print(f"AI: {response1}\n")

    # 第二步：角色设定
    print("[步骤 2] 创建主角")
    response2 = conversation.chat(
        "很好。现在请设计主角的身份、性格和动机。"
    )
    print(f"AI: {response2}\n")

    # 第三步：情节发展
    print("[步骤 3] 构思情节")
    response3 = conversation.chat(
        "请构思一个引人入胜的开头，并规划故事的主要冲突和转折点。"
    )
    print(f"AI: {response3}\n")

    # 第四步：写作示例
    print("[步骤 4] 开头示例")
    response4 = conversation.chat(
        "请根据以上设定，写出故事的开头（约500字）。"
    )
    print(f"AI: {response4}\n")


def learning_assistant():
    """学习助手对话"""
    print("\n=== 学习助手对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    topic = "机器学习基础"

    # 第一课：概念介绍
    print(f"[第1课] {topic} - 概念介绍")
    response1 = conversation.chat(
        f"请为我介绍{topic}的核心概念，包括定义、历史发展和重要性。"
    )
    print(f"AI: {response1}\n")

    # 第二课：深入讲解
    print("[第2课] 深入讲解关键概念")
    response2 = conversation.chat(
        "请深入讲解最核心的3个概念，用简单的语言和例子说明。"
    )
    print(f"AI: {response2}\n")

    # 第三课：实践应用
    print("[第3课] 实践应用")
    response3 = conversation.chat(
        "请给出2个实际应用案例，并说明如何实施。"
    )
    print(f"AI: {response3}\n")

    # 第四课：学习建议
    print("[第4课] 学习建议")
    response4 = conversation.chat(
        "作为一个初学者，请给出学习建议和资源推荐。"
    )
    print(f"AI: {response4}\n")


def image_creative_writing():
    """看图创作对话"""
    print("\n=== 看图创作对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    image_path = "path/to/inspiring_image.jpg"

    # 第一步：图片启发
    print("[步骤 1] 从图片获取灵感")
    response1 = conversation.chat(
        message="请详细描述这张图片，包括所有细节、情感和可能的背景故事",
        image_path=image_path
    )
    print(f"AI: {response1}\n")

    # 第二步：构思故事
    print("[步骤 2] 构思故事情节")
    response2 = conversation.chat(
        "基于这张图片，构思一个短篇故事的核心情节"
    )
    print(f"AI: {response2}\n")

    # 第三步：创作正文
    print("[步骤 3] 创作故事正文")
    response3 = conversation.chat(
        "请写出这个故事的完整版本（约1000字）"
    )
    print(f"AI: {response3}\n")


def business_consultation():
    """商业咨询对话"""
    print("\n=== 商业咨询对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    # 第一步：问题定义
    print("[阶段 1] 定义商业问题")
    response1 = conversation.chat(
        "我的公司是一家B2B SaaS初创企业，目前面临用户增长放缓的问题。请帮我分析可能的原因。"
    )
    print(f"AI: {response1}\n")

    # 第二步：诊断分析
    print("[阶段 2] 深度诊断")
    response2 = conversation.chat(
        "我们主要做中小企业客户，采用freemium模式。获客成本在上升，付费转化率约5%。请给出诊断。"
    )
    print(f"AI: {response2}\n")

    # 第三步：解决方案
    print("[阶段 3] 解决方案")
    response3 = conversation.chat(
        "请给出3-5个具体的改进建议，按优先级排序，并说明每个建议的预期效果和实施难度。"
    )
    print(f"AI: {response3}\n")

    # 第四步：执行计划
    print("[阶段 4] 执行计划")
    response4 = conversation.chat(
        "请制定一个90天的执行计划，包括关键里程碑和成功指标。"
    )
    print(f"AI: {response4}\n")


def code_review_conversation():
    """代码审查对话"""
    print("\n=== 代码审查对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    # 第一步：描述代码
    print("[步骤 1] 描述代码需求")
    response1 = conversation.chat(
        "我写了一个Python函数来处理用户登录，使用了JWT token。请帮我review这段代码，关注安全性、性能和最佳实践。"
    )
    print(f"AI: {response1}\n")

    # 第二步：提供代码
    print("[步骤 2] 提供代码")
    code_snippet = """
def login(username, password):
    user = db.query(User).filter_by(username=username).first()
    if user and check_password(user.password, password):
        token = create_token(user.id)
        return {"success": True, "token": token}
    return {"success": False, "message": "Invalid credentials"}
"""
    response2 = conversation.chat(
        f"这是我的代码：\n```python\n{code_snippet}\n```\n请审查并给出改进建议。"
    )
    print(f"AI: {response2}\n")

    # 第三步：优化建议
    print("[步骤 3] 优化建议")
    response3 = conversation.chat(
        "请给出优化后的代码版本，并解释每个改进点。"
    )
    print(f"AI: {response3}\n")


def role_play_conversation():
    """角色扮演对话"""
    print("\n=== 角色扮演对话示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    # 设定场景
    response1 = conversation.chat(
        "请扮演一位资深的用户体验设计师，我要向你请教一个产品设计问题。"
    )
    print(f"AI: {response1}\n")

    # 开始对话
    print("用户: 我正在设计一个在线教育平台的课程页面")
    response2 = conversation.chat(
        "我正在设计一个在线教育平台的课程详情页。目标用户是职场人士，他们想快速了解课程价值和适合性。请问这个页面应该包含哪些核心元素？"
    )
    print(f"AI: {response2}\n")

    # 深入讨论
    print("用户: 如何平衡信息量和简洁性？")
    response3 = conversation.chat(
        "很好的建议。但我的担心是，如果信息太多，用户可能会被淹没；如果太少，又无法传达足够的价值。如何平衡这个问题？"
    )
    print(f"AI: {response3}\n")


def get_conversation_history():
    """获取对话历史"""
    print("\n=== 对话历史示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    # 进行几轮对话
    conversation.chat("你好")
    conversation.chat("你能做什么？")
    conversation.chat("给我一个例子")

    # 获取历史
    history = conversation.get_history()

    print("对话历史:")
    for i, message in enumerate(history, 1):
        role = message["role"]
        content = message["content"]
        content_preview = content[:50] + "..." if len(content) > 50 else content
        print(f"{i}. [{role.upper()}] {content_preview}")

    print(f"\n总轮数: {len(history)}")


if __name__ == '__main__':
    print(" 大模型 - 多模态对话示例\n")
    print("=" * 60)

    # 运行示例（根据需要选择）
    # simple_text_conversation()
    # image_text_conversation()
    # multi_image_conversation()
    # brainstorming_session()
    # creative_writing_session()
    # learning_assistant()
    # image_creative_writing()
    # business_consultation()
    # code_review_conversation()
    # role_play_conversation()
    # get_conversation_history()

    print("\n提示：请取消注释想要运行的示例函数，并修改图片路径。")
