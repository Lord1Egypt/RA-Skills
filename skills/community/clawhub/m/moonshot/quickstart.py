#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 快速入门脚本
帮助用户快速配置和使用
"""

import os
import sys
from pathlib import Path


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════��════════════════════╗
║                                                           ║
║       大模型工具 - 快速入门                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_requirements():
    """检查依赖包"""
    print("📦 检查依赖包...")

    required_packages = [
        'openai',
        'python-dotenv',
        'pillow',
        'requests',
        'click',
        'rich'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} [未安装]")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n❌ 缺少 {len(missing_packages)} 个依赖包")
        print("\n安装命令:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    else:
        print("\n✅ 所有依赖包已安装")
        return True


def setup_env_file():
    """设置环境变量文件"""
    print("\n📝 配置环境变量...")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print("  ✓ .env 文件已存在")
        return True

    if env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("  ✓ 已从 .env.example 创建 .env 文件")
    else:
        with open(".env", 'w') as f:
            f.write("#  API Key\n")
            f.write("=\n")
        print("  ✓ 已创建 .env 文件")

    print("\n⚠️  请编辑 .env 文件，填入你的 API Key")
    print("   获取 API Key: https://platform./")

    return False


def check_api_key():
    """检查 API Key"""
    print("\n🔑 检查 API Key...")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("")

    if not api_key:
        print("  ✗ API Key 未配置")
        return False

    # 验证 API Key 格式（简单检查）
    if len(api_key) < 10:
        print("  ✗ API Key 格式不正确")
        return False

    print(f"  ✓ API Key 已配置: {api_key[:8]}...{api_key[-4:]}")
    return True


def test_connection():
    """测试 API 连接"""
    print("\n🌐 测试 API 连接...")

    try:
        from client import
        client = ()
        print("  ✓ 客户端初始化成功")
        return True
    except Exception as e:
        print(f"  ✗ 连接失败: {e}")
        return False


def create_directories():
    """创建必要的目录"""
    print("\n📁 创建目录结构...")

    directories = [
        "output",
        "output/images",
        "output/text",
        "examples/output"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}/")


def show_quick_commands():
    """显示快速命令"""
    print("\n" + "="*60)
    print("🚀 快速开始命令")
    print("="*60)

    commands = [
        ("分析图片", "python cli.py analyze <图片路径>"),
        ("OCR 提取", "python cli.py ocr <图片路径>"),
        ("文案创作", "python cli.py copywrite --image <图片路径>"),
        ("交互对话", "python cli.py chat"),
        ("批量处理", "python cli.py batch <图片1> <图片2> ..."),
        ("配置检查", "python cli.py config"),
        ("帮助信息", "python cli.py --help"),
    ]

    for i, (desc, cmd) in enumerate(commands, 1):
        print(f"\n{i}. {desc}")
        print(f"   {cmd}")


def show_examples():
    """显示示例代码"""
    print("\n" + "="*60)
    print("📚 示例代码")
    print("="*60)

    examples = [
        ("图像分析", "python examples/image_analysis.py"),
        ("OCR 提取", "python examples/ocr_demo.py"),
        ("文案创作", "python examples/copywriting.py"),
        ("多模态对话", "python examples/conversation.py"),
    ]

    for desc, cmd in examples:
        print(f"  • {desc}: {cmd}")


def show_model_info():
    """显示模型信息"""
    print("\n" + "="*60)
    print("🤖 可用模型")
    print("="*60)

    models = [
        ("", "基础模型", "8K", "适合一般任务"),
        ("", "扩展模型", "32K", "适合长文档"),
        ("", "大上下文", "128K", "适合超长文档"),
    ]

    for model, name, context, usage in models:
        print(f"\n{model}")
        print(f"  名称: {name}")
        print(f"  上下文: {context}")
        print(f"  适用: {usage}")


def show_next_steps():
    """显示后续步骤"""
    print("\n" + "="*60)
    print("📋 后续步骤")
    print("="*60)

    steps = [
        "1. 编辑 .env 文件，配置你的 API Key",
        "2. 运行 'python cli.py config' 验证配置",
        "3. 尝试简单的图像分析: python cli.py analyze <图片路径>",
        "4. 探索 examples/ 目录中的更多示例",
        "5. 阅读文档: skill.md 和 README.md",
    ]

    for step in steps:
        print(f"  {step}")


def main():
    """主函数"""
    print_banner()

    # 检查步骤
    steps_passed = 0

    # 1. 检查依赖
    if check_requirements():
        steps_passed += 1
    else:
        print("\n⚠️  请先安装缺少的依赖包")
        return

    # 2. 设置环境变量
    if setup_env_file():
        steps_passed += 1
    else:
        print("\n⚠️  请先配置 API Key")
        show_next_steps()
        return

    # 3. 检查 API Key
    if check_api_key():
        steps_passed += 1
    else:
        print("\n⚠️  请先配置有效的 API Key")
        show_next_steps()
        return

    # 4. 测试连接
    if test_connection():
        steps_passed += 1
    else:
        print("\n⚠️  请检查 API Key 和网络连接")
        return

    # 5. 创建目录
    create_directories()
    steps_passed += 1

    # 配置完成
    print("\n" + "="*60)
    print(f"✅ 配置完成! ({steps_passed}/5 步骤通过)")
    print("="*60)

    # 显示信息
    show_quick_commands()
    show_examples()
    show_model_info()
    show_next_steps()

    print("\n" + "="*60)
    print("🎉 准备就绪！开始使用  大模型工具吧")
    print("="*60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 安装已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)
