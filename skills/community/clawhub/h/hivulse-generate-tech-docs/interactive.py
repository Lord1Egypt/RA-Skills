#!/usr/bin/env python3
"""
hivulseAI 交互式界面
"""

import os
import sys
from hivulseAI import HivulseAI
from config import ConfigManager, setup_config

def select_directory():
    """让用户选择目录"""
    while True:
        directory = input("📁 请输入项目目录路径: ").strip()

        if not directory:
            print("❌ 目录不能为空")
            continue

        if not os.path.exists(directory):
            print("❌ 目录不存在，请重新输入")
            continue

        if not os.path.isdir(directory):
            print("❌ 输入的不是目录，请重新输入")
            continue

        return directory

def select_document_type():
    """让用户选择文档类型"""
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

    print("\n📄 请选择要生成的文档类型:")
    for key, value in doc_types.items():
        print(f"  {key}: {value}")

    while True:
        choice = input("\n请输入文档类型编号: ").strip()

        if choice in doc_types:
            return choice
        else:
            print("❌ 无效的选择，请重新输入")

def get_task_name(directory: str, doc_type: str) -> str:
    """根据输入生成任务名称"""
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
    """主交互函数"""
    print("=" * 50)
    print("🚀 hivulseAI - 自动化技术文档生成工具")
    print("=" * 50)

    # 配置管理
    config = setup_config()

    if not config.has_valid_config():
        print("❌ 配置不完整，请先设置API密钥")
        return

    # 获取配置信息
    api_key = config.get_api_key()
    last_directory = config.get_last_directory()

    # 选择目录
    if last_directory and os.path.exists(last_directory):
        use_last = input(f"📁 是否使用上次的目录 ({last_directory})? (y/n): ").strip().lower()
        if use_last in ['y', 'yes', '是']:
            directory = last_directory
        else:
            directory = select_directory()
    else:
        directory = select_directory()

    # 保存当前目录
    config.set_last_directory(directory)

    # 选择文档类型
    doc_type = select_document_type()

    # 生成任务名称
    task_name = get_task_name(directory, doc_type)

    print(f"\n📋 任务信息:")
    print(f"   目录: {directory}")
    print(f"   文档类型: {doc_type}")
    print(f"   任务名称: {task_name}")

    confirm = input("\n确认开始处理? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '是']:
        print("👋 操作已取消")
        return

    # 创建实例并运行
    ai = HivulseAI(api_key=api_key)

    try:
        success = ai.run(directory, doc_type, task_name)
        if success:
            print("\n🎉 文档生成流程完成！完成后将会发送邮件，请查收")
        else:
            print("\n❌ 文档生成流程失败")
    except KeyboardInterrupt:
        print("\n\n👋 用户中断操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    main()
