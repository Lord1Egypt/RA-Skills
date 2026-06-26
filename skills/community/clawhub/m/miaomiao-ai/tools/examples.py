#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
秒秒AI助理 功能调用示例
运行前请确保已安装依赖: pip install python-dotenv
并在项目根目录配置好 .env 文件
"""

from miaomiao_client import MiaoMiaoClient, chat

def example_basic_chat():
    """基础聊天示例"""
    print("=== 基础聊天示例 ===")
    response = chat("你好，介绍一下你自己")
    print(f"回复: {response}\n")

def example_weather_query():
    """天气查询示例"""
    print("=== 天气查询示例 ===")
    response = chat("北京今天天气怎么样")
    print(f"回复: {response}\n")

def example_news_query():
    """新闻查询示例"""
    print("=== 新闻早报示例 ===")
    response = chat("今天的新闻早报")
    print(f"回复: {response}\n")

def example_express_query():
    """快递查询示例"""
    print("=== 快递查询示例 ===")
    # 替换为实际快递单号
    response = chat("查询快递单号 1234567890")
    print(f"回复: {response}\n")

def example_image_generation():
    """图像生成示例"""
    print("=== 图像生成示例 ===")
    response = chat("生成一张春日樱花的图片，风格是水彩画")
    print(f"回复: {response}\n")

def example_web_search():
    """网页搜索示例"""
    print("=== 网页搜索示例 ===")
    response = chat("搜索2026年人工智能最新发展趋势")
    print(f"回复: {response}\n")

def example_content_summary():
    """内容总结示例"""
    print("=== 内容总结示例 ===")
    long_text = """
    人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器，该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，将会是人类智慧的“容器”。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。
    """
    response = chat(f"总结这段内容：{long_text}")
    print(f"回复: {response}\n")

def example_chart_generation():
    """图表生成示例"""
    print("=== 图表生成示例 ===")
    response = chat("生成一个柱状图，展示一季度各月销售额：1月10万，2月15万，3月20万")
    print(f"回复: {response}\n")

def example_map_query():
    """地图查询示例"""
    print("=== 地图查询示例 ===")
    response = chat("从北京天安门到八达岭长城的自驾路线")
    print(f"回复: {response}\n")

def example_train_ticket_query():
    """车票查询示例"""
    print("=== 火车票查询示例 ===")
    response = chat("查询明天北京到上海的高铁票")
    print(f"回复: {response}\n")

def example_with_history():
    """带历史消息的对话示例"""
    print("=== 多轮对话示例 ===")
    client = MiaoMiaoClient()
    
    # 第一轮对话
    messages = [
        {"role": "user", "content": "我想去上海旅游三天"}
    ]
    response = client.chat_with_history(messages)
    print(f"第一轮回复: {response}")
    messages.append({"role": "assistant", "content": response})
    
    # 第二轮对话
    messages.append({"role": "user", "content": "推荐一些必去的景点"})
    response = client.chat_with_history(messages)
    print(f"第二轮回复: {response}\n")

def example_stream_response():
    """流式响应示例（如需使用请取消注释）"""
    # print("=== 流式响应示例 ===")
    # client = MiaoMiaoClient()
    # response = client.chat("写一个300字的春天散文", stream=True)
    # 处理流式响应的逻辑...

if __name__ == "__main__":
    # 运行所有示例
    example_basic_chat()
    example_weather_query()
    example_news_query()
    # 可根据需要注释不需要运行的示例
    # example_express_query()
    # example_image_generation()
    # example_web_search()
    # example_content_summary()
    # example_chart_generation()
    # example_map_query()
    # example_train_ticket_query()
    # example_with_history()
