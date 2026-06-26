#!/usr/bin/env python3
"""
hivulseAI OpenClaw Skill Implementation

标准化的OpenClaw技能实现，通过环境变量配置API密钥。
"""

import os
import sys
import json
import argparse
from pathlib import Path

def get_config():
    """从配置文件获取配置"""
    from config import ConfigManager
    config = ConfigManager()

    api_key = config.get_api_key()

    if not api_key:
        print("❌ 错误: API密钥未设置")
        print("\n📋 请选择配置方式:")
        print("1. 运行配置向导: python3 config.py")
        print("2. 手动编辑配置文件: ~/.hivulseai/config.json")
        print("\n📝 配置文件内容示例:")
        print('''{
  "api_key": "your-api-key-here",
  "last_used_directory": ""
}''')
        sys.exit(1)

    return {
        'api_key': api_key,
    }

def validate_directory(directory):
    """验证目录是否存在"""
    if not os.path.exists(directory):
        print(f"❌ 错误: 目录不存在: {directory}")
        sys.exit(1)

    if not os.path.isdir(directory):
        print(f"❌ 错误: 路径不是目录: {directory}")
        sys.exit(1)

    return os.path.abspath(directory)

def validate_doc_type(doc_type):
    """验证文档类型"""
    doc_types = {
        "19": "用户需求说明书",
        "2": "需求规格说明书",
        "4": "系统概要设计说明",
        "5": "系统详细设计说明",
        "8": "软件单元测试计划",
        "9": "软件单元测试用例",
        "10": "软件单元测试报告",
        "1": "系统测试计划",
        "12": "系统测试用例",
        "15": "系统测试报告",
        "13": "网络安全漏洞自评报告",
        "20": "软件用户测试用例",
        "21": "软件用户测试报告"
    }

    if doc_type not in doc_types:
        print(f"❌ 错误: 不支持的文档类型: {doc_type}")
        print("📄 支持的文档类型:")
        for key, value in doc_types.items():
            print(f"  {key}: {value}")
        sys.exit(1)

    return doc_type

def generate_task_name(directory, doc_type):
    """生成任务名称"""
    doc_names = {
        "19": "用户需求说明书",
        "2": "需求规格说明书",
        "4": "系统概要设计说明",
        "5": "系统详细设计说明",
        "8": "软件单元测试计划",
        "9": "软件单元测试用例",
        "10": "软件单元测试报告",
        "1": "系统测试计划",
        "12": "系统测试用例",
        "15": "系统测试报告",
        "13": "网络安全漏洞自评报告",
        "20": "软件用户测试用例",
        "21": "软件用户测试报告"
    }

    project_name = os.path.basename(os.path.abspath(directory))
    doc_name = doc_names.get(doc_type, "技术文档")

    return f"{project_name}项目{doc_name}生成"

def main():
    """主函数 - 标准OpenClaw技能入口"""
    parser = argparse.ArgumentParser(description='hivulseAI - 自动化技术文档生成')
    parser.add_argument('directory', nargs='?', help='项目目录路径')
    parser.add_argument('doc_type', nargs='?', help='文档类型编号')
    parser.add_argument('--task-name', help='任务名称', default=None)
    parser.add_argument('--interactive', action='store_true', help='交互式模式')
    parser.add_argument('--list-types', action='store_true', help='列出支持的文档类型')

    args = parser.parse_args()

    # 列出支持的文档类型
    if args.list_types:
        doc_types = {
            "19": "用户需求说明书",
            "2": "需求规格说明书",
            "4": "系统概要设计说明",
            "5": "系统详细设计说明",
            "8": "软件单元测试计划",
            "9": "软件单元测试用例",
            "10": "软件单元测试报告",
            "1": "系统测试计划",
            "12": "系统测试用例",
            "15": "系统测试报告",
            "13": "网络安全漏洞自评报告",
            "20": "软件用户测试用例",
            "21": "软件用户测试报告"
        }

        print("\n📋 支持的13种文档类型：")
        print("=" * 40)
        for key, value in doc_types.items():
            print(f"  {key}: {value}")
        print("=" * 40)
        print("\n💡 使用方法: python hivulseai_skill.py <目录> <文档类型编号>")
        print("💡 交互式模式: python hivulseai_skill.py --interactive")
        return

    # 交互式模式
    if args.interactive:
        # 导入交互式模块
        skill_dir = Path(__file__).parent
        interactive_path = skill_dir / "interactive.py"

        if interactive_path.exists():
            os.system(f"python {interactive_path}")
        else:
            print("❌ 交互式模块不存在")
        return

    # 获取配置
    config = get_config()

    # 验证参数
    if not args.directory or not args.doc_type:
        print("❌ 错误: 需要指定目录和文档类型")
        print("💡 用法: python hivulseai_skill.py <目录> <文档类型>")
        print("💡 或使用: python hivulseai_skill.py --interactive")
        print("💡 查看类型: python hivulseai_skill.py --list-types")
        sys.exit(1)

    directory = validate_directory(args.directory)
    doc_type = validate_doc_type(args.doc_type)

    # 生成任务名称
    if args.task_name:
        task_name = args.task_name
    else:
        task_name = generate_task_name(directory, doc_type)


    print(f"🚀 hivulseAI 开始处理")
    print(f"📁 目录: {directory}")
    print(f"📄 文档类型: {doc_type}")
    print(f"📋 任务名称: {task_name}")

    # 导入并执行主逻辑
    try:
        # 动态导入主模块
        skill_dir = Path(__file__).parent
        sys.path.insert(0, str(skill_dir))

        from hivulseAI import HivulseAI

        # 创建实例并执行
        ai = HivulseAI(api_key=config['api_key'])
        success = ai.run(directory, doc_type, task_name)

        if success:
            print("\n🎉 hivulseAI 处理完成！")
            print("📧 文档生成功后将通过邮件发送到您的邮箱")

            sys.exit(0)
        else:
            print("\n❌ hivulseAI 处理失败")
            sys.exit(1)

    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 确保hivulseAI.py文件存在")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
