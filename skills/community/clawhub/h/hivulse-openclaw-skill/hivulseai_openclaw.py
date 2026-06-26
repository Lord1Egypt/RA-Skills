#!/usr/bin/env python3
"""
hivulseAI OpenClaw Skill Implementation

从OpenClaw配置中读取API密钥，支持技能页面直接配置
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def get_config_value(path):
    """从OpenClaw配置中获取值"""
    try:
        # 直接读取配置文件
        config_file = Path.home() / ".openclaw" / "openclaw.json"

        if config_file.exists():
            with open(config_file, 'r') as f:
                config_data = json.load(f)

            # 从配置中提取apiKey
            if 'skills' in config_data and 'entries' in config_data['skills']:
                hivulse_config = config_data['skills']['entries'].get('hivulseAI', {})
                if path == 'skills.entries.hivulseAI.apiKey':
                    api_key = hivulse_config.get('apiKey', '')
                    # 检查是否是占位符值
                    if api_key and api_key != 'your-hivulse-api-key-here':
                        return api_key
                    return ''


        return ''
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")
        return ''

def get_api_key():
    """获取API密钥，优先从OpenClaw配置中读取"""
    # 1. 先尝试从OpenClaw配置中读取
    api_key = get_config_value('skills.entries.hivulseAI.apiKey')

    if api_key and api_key != 'your-hivulse-api-key-here':
        return api_key

    # 2. 再尝试从环境变量中读取
    api_key = os.getenv('HIVULSE_API_KEY')
    if api_key:
        return api_key

    # 3. 如果都没有，提示用户配置
    print("❌ 错误: hivulseAI API密钥未配置")
    print("💡 请在OpenClaw技能页面中配置API密钥:")
    print("   1. 打开OpenClaw配置界面")
    print("   2. 找到 skills.entries.hivulseAI.apiKey")
    print("   3. 输入您的hivulseAI API密钥")
    print("   4. 保存配置")
    print("")
    print("💡 或者设置环境变量:")
    print("   export HIVULSE_API_KEY='your-api-key'")

    return ''



    # 2. 默认使用 http://localhost:8001
    return 'http://localhost:8001'

def validate_directory(directory):
    """验证目录是否存在"""
    if not os.path.exists(directory):
        print(f"❌ 错误: 目录不存在: {directory}")
        return False

    if not os.path.isdir(directory):
        print(f"❌ 错误: 路径不是目录: {directory}")
        return False

    return True

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
        return False

    return True

def main():
    """主函数 - 从命令行参数获取信息"""
    if len(sys.argv) < 3:
        print("❌ 用法: python hivulseai_openclaw.py <目录> <文档类型> [任务名称]")
        print("")
        print("📄 支持的文档类型:")
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
        for key, value in doc_types.items():
            print(f"  {key}: {value}")
        sys.exit(1)

    directory = sys.argv[1]
    doc_type = sys.argv[2]
    task_name = sys.argv[3] if len(sys.argv) > 3 else None

    # 验证参数
    if not validate_directory(directory):
        sys.exit(1)

    if not validate_doc_type(doc_type):
        sys.exit(1)

    # 获取API配置
    api_key = get_api_key()
    if not api_key:
        sys.exit(1)


    # 生成任务名称
    if not task_name:
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
        task_name = f"{project_name}项目{doc_name}生成"

    print(f"🚀 hivulseAI 开始处理")
    print(f"📁 目录: {directory}")
    print(f"📄 文档类型: {doc_type}")
    print(f"📋 任务名称: {task_name}")
    print(f"🔑 API密钥: {api_key[:10]}...")

    # 设置环境变量，供主技能使用
    os.environ['HIVULSE_API_KEY'] = api_key

    # 调用主技能
    try:
        skill_dir = Path(__file__).parent
        main_script = skill_dir / "hivulseai_skill.py"

        if main_script.exists():
            # 调用主技能脚本
            cmd = [
                'python3', str(main_script),
                directory, doc_type,
                '--task-name', task_name
            ]

            result = subprocess.run(cmd, cwd=skill_dir)
            sys.exit(result.returncode)
        else:
            print("❌ 主技能脚本不存在")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 执行错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
