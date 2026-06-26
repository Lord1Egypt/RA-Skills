#!/usr/bin/env python3
"""
OpenSpace LLM Skill — MiniMax-M2.7 调用接口

让 OpenClaw 可以直接使用 MiniMax 官方 API（包月 6000 次/周）
支持短/中/长 prompt，自动代理，5 分钟超时

Commands:
  chat <prompt>              单次对话
  write <topic>              写文章（长文本）
  analyze <text>             分析文本
  code <task>                生成代码
  test                       测试连接
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# 导入 OpenSpace
try:
    from openspace.llm.client import LLMClient
    from openspace.host_detection.resolver import build_llm_kwargs
except ImportError:
    print("❌ 错误：需要安装 OpenSpace")
    print("   pip install openspace")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

# 从环境变量读取配置
DEFAULT_MODEL = os.environ.get("OPENSPACE_MODEL", "minimax/MiniMax-M2.7")
DEFAULT_API_BASE = os.environ.get("OPENSPACE_API_BASE", "https://api.minimax.chat/v1")
DEFAULT_API_KEY = os.environ.get("OPENSPACE_API_KEY", "")
DEFAULT_PROXY = os.environ.get("HTTP_PROXY", "http://127.0.0.1:10810")
DEFAULT_TIMEOUT = int(os.environ.get("OPENSPACE_TIMEOUT", "300"))  # 5 分钟
DEFAULT_MAX_RETRIES = int(os.environ.get("OPENSPACE_MAX_RETRIES", "3"))

# ---------------------------------------------------------------------------
# LLM 客户端
# ---------------------------------------------------------------------------

def create_client():
    """创建 LLMClient 实例"""
    
    # 设置环境变量
    if not os.environ.get("OPENSPACE_MODEL"):
        os.environ["OPENSPACE_MODEL"] = DEFAULT_MODEL
    if not os.environ.get("OPENSPACE_API_BASE"):
        os.environ["OPENSPACE_API_BASE"] = DEFAULT_API_BASE
    if not os.environ.get("OPENSPACE_API_KEY"):
        os.environ["OPENSPACE_API_KEY"] = DEFAULT_API_KEY
    if not os.environ.get("HTTP_PROXY"):
        os.environ["HTTP_PROXY"] = DEFAULT_PROXY
    if not os.environ.get("HTTPS_PROXY"):
        os.environ["HTTPS_PROXY"] = DEFAULT_PROXY
    
    # 构建配置
    model, llm_kwargs = build_llm_kwargs(DEFAULT_MODEL)
    
    # 创建客户端
    client = LLMClient(
        model=model,
        timeout=DEFAULT_TIMEOUT,
        max_retries=DEFAULT_MAX_RETRIES,
        retry_delay=10,
        **llm_kwargs
    )
    
    return client

async def chat(prompt: str):
    """单次对话"""
    
    client = create_client()
    messages = [{"role": "user", "content": prompt}]
    
    result = await client.complete(messages=messages, execute_tools=False)
    return result['message']['content']

async def write_article(topic: str, word_count: int = 1000):
    """写文章"""
    
    prompt = f"""请写一篇关于"{topic}"的文章

要求：
1. 字数：{word_count}字以上
2. 结构清晰，包含引言、正文（3-5 个论点）、结论
3. 论点要有深度，包含具体例子
4. 语言流畅，逻辑严密

请认真写作，确保文章质量。"""
    
    return await chat(prompt)

async def analyze_text(text: str):
    """分析文本"""
    
    prompt = f"""请分析以下文本：

{text}

请从以下角度分析：
1. 主要内容总结
2. 核心观点
3. 论证结构
4. 语言特点
5. 可能的改进建议

请详细分析。"""
    
    return await chat(prompt)

async def generate_code(task: str, language: str = "Python"):
    """生成代码"""
    
    prompt = f"""请用{language}语言完成以下任务：

{task}

要求：
1. 代码完整、可运行
2. 包含必要的注释
3. 遵循最佳实践
4. 如果有依赖，请说明如何安装

请提供完整的代码实现。"""
    
    return await chat(prompt)

def test_connection():
    """测试连接"""
    
    print("测试 OpenSpace LLM 连接...")
    print(f"Model: {DEFAULT_MODEL}")
    print(f"API Base: {DEFAULT_API_BASE}")
    print(f"Proxy: {DEFAULT_PROXY}")
    print(f"Timeout: {DEFAULT_TIMEOUT}s")
    print()
    
    async def run_test():
        client = create_client()
        
        # 测试配置
        print("✓ LLMClient 创建成功")
        print(f"✓ Model: {client.model}")
        print(f"✓ Proxy: {client.proxy}")
        print(f"✓ Timeout: {client.timeout}s")
        print()
        
        # 测试调用
        print("测试调用...")
        messages = [{"role": "user", "content": "你好，请回复'测试成功'"}]
        result = await client.complete(messages=messages, execute_tools=False)
        
        response = result['message']['content']
        print(f"✓ 调用成功")
        print(f"✓ 响应：{response}")
        print()
        
        return True
    
    try:
        asyncio.run(run_test())
        print("=" * 60)
        print("✅ 连接测试成功！OpenSpace LLM 可以正常使用")
        print("=" * 60)
        return True
    except Exception as e:
        print("=" * 60)
        print(f"❌ 连接测试失败：{type(e).__name__}: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

# ---------------------------------------------------------------------------
# 命令行接口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="OpenSpace LLM Skill - MiniMax-M2.7 调用接口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s chat "你好"
  %(prog)s write "人工智能的未来"
  %(prog)s analyze "这是一段需要分析的文本..."
  %(prog)s code "写一个快速排序算法"
  %(prog)s test
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # chat 命令
    chat_parser = subparsers.add_parser("chat", help="单次对话")
    chat_parser.add_argument("prompt", type=str, help="对话内容")
    
    # write 命令
    write_parser = subparsers.add_parser("write", help="写文章")
    write_parser.add_argument("topic", type=str, help="文章主题")
    write_parser.add_argument("--words", type=int, default=1000, help="目标字数（默认 1000）")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析文本")
    analyze_parser.add_argument("text", type=str, help="要分析的文本")
    
    # code 命令
    code_parser = subparsers.add_parser("code", help="生成代码")
    code_parser.add_argument("task", type=str, help="编程任务")
    code_parser.add_argument("--lang", type=str, default="Python", help="编程语言（默认 Python）")
    
    # test 命令
    subparsers.add_parser("test", help="测试连接")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 执行命令
    if args.command == "chat":
        print(f"Prompt: {args.prompt}")
        print("\n调用中...")
        response = asyncio.run(chat(args.prompt))
        print(f"\n响应：{response}")
        
    elif args.command == "write":
        print(f"主题：{args.topic}")
        print(f"目标字数：{args.words}")
        print("\n写作中...（可能需要 1-3 分钟）")
        article = asyncio.run(write_article(args.topic, args.words))
        print(f"\n文章完成！字数：{len(article)}")
        print("\n" + "=" * 60)
        print(article[:500] + "..." if len(article) > 500 else article)
        
    elif args.command == "analyze":
        print("分析中...")
        analysis = asyncio.run(analyze_text(args.text))
        print(f"\n分析结果：{analysis}")
        
    elif args.command == "code":
        print(f"任务：{args.task}")
        print(f"语言：{args.lang}")
        print("\n生成代码中...")
        code = asyncio.run(generate_code(args.task, args.lang))
        print(f"\n代码生成完成！")
        print("\n" + "=" * 60)
        print(code)
        
    elif args.command == "test":
        success = test_connection()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
