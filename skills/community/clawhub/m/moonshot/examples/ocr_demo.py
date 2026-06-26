#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 文字提取示例
演示如何使用  进行 OCR 文字识别
"""

import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import, OutputFormat


def extract_simple_text():
    """简单文字提取"""
    print("=== 简单文字提取示例 ===\n")

    client = ()
    image_path = "path/to/document.jpg"

    try:
        result = client.extract_text(
            image_path=image_path,
            output_format=OutputFormat.TEXT,
            language="auto"
        )

        print("提取的文字内容:")
        print(result.text)
        print(f"\n识别语言: {result.language}")
        print(f"置信度: {result.confidence:.2%}")

    except Exception as e:
        print(f"提取失败: {e}")


def extract_structured_text():
    """结构化文字提取"""
    print("\n=== 结构化文字提取示例 ===\n")

    client = ()
    image_path = "path/to/document.jpg"

    try:
        result = client.extract_text(
            image_path=image_path,
            output_format=OutputFormat.STRUCTURED,
            language="zh"
        )

        print("结构化文本:")
        print(result.text)

        # 保存到文件
        output_file = "extracted_text.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.text)
        print(f"\n结果已保存到: {output_file}")

    except Exception as e:
        print(f"提取失败: {e}")


def extract_table():
    """表格数据提取"""
    print("\n=== 表格数据提取示例 ===\n")

    client = ()
    image_path = "path/to/table.jpg"

    try:
        result = client.extract_text(
            image_path=image_path,
            output_format=OutputFormat.STRUCTURED,
            language="zh"
        )

        print("提取的表格数据:")
        print(result.text)

    except Exception as e:
        print(f"提取失败: {e}")


def extract_handwriting():
    """手写文字识别"""
    print("\n=== 手写文字识别示例 ===\n")

    client = ()
    image_path = "path/to/handwriting.jpg"

    try:
        result = client.extract_text(
            image_path=image_path,
            output_format=OutputFormat.TEXT,
            language="zh"
        )

        print("识别的手写文字:")
        print(result.text)
        print(f"\n识别置信度: {result.confidence:.2%}")
        print("注意: 手写文字识别准确度依赖于图片清晰度和字迹工整程度")

    except Exception as e:
        print(f"识别失败: {e}")


def batch_extract_documents():
    """批量文档提取"""
    print("\n=== 批量文档提取示例 ===\n")

    client = ()
    image_paths = [
        "path/to/doc1.jpg",
        "path/to/doc2.jpg",
        "path/to/doc3.jpg"
    ]

    output_dir = "extracted_docs"
    os.makedirs(output_dir, exist_ok=True)

    for i, image_path in enumerate(image_paths, 1):
        print(f"\n处理文档 {i}: {os.path.basename(image_path)}")

        try:
            result = client.extract_text(
                image_path=image_path,
                output_format=OutputFormat.TEXT
            )

            # 保存结果
            output_file = os.path.join(output_dir, f"doc_{i}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.text)

            print(f"✓ 提取完成，保存到: {output_file}")
            print(f"  文字数量: {len(result.text)} 字符")
            print(f"  置信度: {result.confidence:.2%}")

        except Exception as e:
            print(f"✗ 提取失败: {e}")


def extract_multilingual_text():
    """多语言文字提取"""
    print("\n=== 多语言文字提取示例 ===\n")

    client = ()
    image_path = "path/to/multilingual_doc.jpg"

    try:
        # 自动检测语言
        result_auto = client.extract_text(
            image_path=image_path,
            output_format=OutputFormat.TEXT,
            language="auto"
        )

        print("自动语言检测:")
        print(result_auto.text)
        print(f"检测到的语言: {result_auto.language}")

    except Exception as e:
        print(f"提取失败: {e}")


def extract_with_context():
    """带上下文的文字提取"""
    print("\n=== 带上下文的文字提取示例 ===\n")

    client = ()
    image_path = "path/to/document.jpg"

    # 使用对话方式进行文字提取
    conversation = client.create_conversation()

    # 第一步：提取文字
    response1 = conversation.chat(
        message="请提取图片中的所有文字内容，保持原有格式。",
        image_path=image_path
    )
    print("提取的文字:")
    print(response1)

    # 第二步：总结内容
    response2 = conversation.chat(
        message="基于提取的文字内容，请总结文档的主要观点和关键信息。"
    )
    print("\n文档总结:")
    print(response2)

    # 第三步：提取关键信息
    response3 = conversation.chat(
        message="请从文档中提取以下信息：日期、金额、人名、地点等关键数据。"
    )
    print("\n关键信息:")
    print(response3)


def extract_receipt():
    """收据/发票信息提取"""
    print("\n=== 收据信息提取示例 ===\n")

    client = ()
    image_path = "path/to/receipt.jpg"

    try:
        result = client.extract_text(
            image_path=image_path,
            output_format=OutputFormat.STRUCTURED
        )

        print("提取的收据信息:")
        print(result.text)

        # 使用对话方式提取结构化信息
        conversation = client.create_conversation()
        structured_info = conversation.chat(
            message=f"""从以下收据文字中提取结构化信息：

{result.text}

请以 JSON 格式提取以下信息：
- 商家名称
- 日期时间
- 总金额
- 支付方式
- 商品明细（如果有）

只返回 JSON，不需要其他说明。""",
            image_path=image_path
        )

        print("\n结构化信息:")
        print(structured_info)

    except Exception as e:
        print(f"提取失败: {e}")


def extract_screenshot():
    """截图文字提取"""
    print("\n=== 截图文字提取示例 ===\n")

    client = ()
    image_path = "path/to/screenshot.png"

    try:
        result = client.extract_text(
            image_path=image_path,
            output_format=OutputFormat.TEXT
        )

        print("截图中的文字:")
        print(result.text)

        # 分析截图内容
        conversation = client.create_conversation()
        analysis = conversation.chat(
            message=f"""分析以下截图内容：

{result.text}

请识别：
1. 应用程序或网站名称
2. 主要功能和操作
3. 重要数据或信息
4. 用户界面元素
5. 潜在的问题或改进点

请给出详细的分析报告。"""
        )

        print("\n截图分析:")
        print(analysis)

    except Exception as e:
        print(f"提取失败: {e}")


if __name__ == '__main__':
    print(" 大模型 - OCR 文字提取示例\n")
    print("=" * 60)

    # 运行示例（根据需要选择）
    # extract_simple_text()
    # extract_structured_text()
    # extract_table()
    # extract_handwriting()
    # batch_extract_documents()
    # extract_multilingual_text()
    # extract_with_context()
    # extract_receipt()
    # extract_screenshot()

    print("\n提示：请取消注释想要运行的示例函数，并修改图片路径。")
