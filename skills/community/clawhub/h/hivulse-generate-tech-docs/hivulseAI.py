#!/usr/bin/env python3
"""
hivulseAI - 自动化技术文档生成工具
"""

import os
import requests
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class HivulseAI:
    def __init__(self, api_key: str = None):
        # 优先使用传入的参数，否则尝试多种配置源
        self.api_key = api_key

        if not self.api_key:
            # 尝试从OpenClaw配置读取
            self.api_key = self._get_api_key_from_openclaw_config()

        if not self.api_key:
            # 尝试从本地配置文件读取
            from config import ConfigManager
            config = ConfigManager()
            self.api_key = config.get_api_key()

        self.base_url = 'https://cloud.hivulse.com'
        # self.base_url = 'http://127.0.0.1:8001'
        self.repo_id = None
        self.default_branch_id = None

        # 文档类型映射
        self.doc_types = {
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

        # 验证API密钥
        if not self.api_key:
            print("❌ API密钥未设置")
            print("\n📋 配置方式:")
            print("1. OpenClaw配置界面: 在skills.entries.hivulseAI.apiKey中设置")
            print("2. 本地配置文件: ~/.hivulseai/config.json")
            print("3. 运行配置向导: python3 config.py")
            print("\n💡 推荐使用OpenClaw配置界面设置API密钥")
            raise ValueError("API密钥未配置")

        # 设置请求头，包含API密钥
        self.headers = {}
        if self.api_key:
            self.headers['X-API-KEY'] = f'{self.api_key}'

        # 需要过滤的目录
        self.exclude_dirs = {'node_modules', 'venv', '.git', '__pycache__', '.idea', '.vscode'}
        # 需要过滤的文件后缀
        self.exclude_extensions = {'.pyc', '.log'}

    def _get_api_key_from_openclaw_config(self):
        """尝试从OpenClaw配置读取API密钥"""
        try:
            import subprocess
            import json

            # 尝试直接读取OpenClaw配置文件
            config_path = "/Users/superlk/.openclaw/openclaw.json"
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_content = f.read()

                # 解析JSON配置
                import re
                # 查找skills.entries.hivulseAI.apiKey字段
                pattern = r'"skills"\s*:\s*{[^}]*"entries"\s*:\s*{[^}]*"hivulseAI"\s*:\s*{[^}]*"apiKey"\s*:\s*"([^"]+)"[^}]*}'
                match = re.search(pattern, config_content)

                if match:
                    api_key = match.group(1)
                    if api_key != "__OPENCLAW_REDACTED__":
                        print(f"✅ 从OpenClaw配置读取API密钥")
                        return api_key
                    else:
                        print("⚠️ OpenClaw配置中API密钥被安全隐藏")
                        return None

        except Exception as e:
            print(f"⚠️ 读取OpenClaw配置失败: {e}")
            # 如果无法读取OpenClaw配置，回退到本地配置
            pass

        return None



    def get_directory_files(self, directory: str) -> List[str]:
        """获取目录下所有文件，过滤掉指定目录"""
        file_paths = []

        for root, dirs, files in os.walk(directory):
            # 过滤掉不需要的目录
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]

            for file in files:
                # 过滤掉不需要的文件后缀
                if any(file.endswith(ext) for ext in self.exclude_extensions):
                    continue
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

        return file_paths



    def upload_file(self, file_path: str, directory: str, branch_id: Optional[str] = None, unified_file_path: str = None) -> Dict:
        """上传单个文件到API"""
        url = f"{self.base_url}/api/v1/claw/upload/file/"

        # 修复路径格式化：使用项目名称开头的相对路径
        project_name = unified_file_path
        relative_path = os.path.relpath(file_path, directory)
        api_file_path = f"{project_name}/{relative_path}"

        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            data = {'file_path': api_file_path}

            if branch_id:
                data['branch_id'] = branch_id

            response = requests.post(url, files=files, data=data, headers=self.headers)

            # 如果返回"项目已存在"错误，直接抛出异常，强制重新上传
            if response.status_code == 412 and "项目已经存在" in response.text:
                print(f"⚠️ 项目已存在，API响应: {response.text}")
                raise Exception("项目已存在，需要重新上传")

            response.raise_for_status()
            result = response.json()
            print(f"🔍 API响应详情: {result}")
            return result

    def upload_all_files(self, directory: str) -> bool:
        """上传目录下所有文件"""
        file_paths = self.get_directory_files(directory)

        if not file_paths:
            print("❌ 目录中没有找到文件")
            return False

        print(f"📁 找到 {len(file_paths)} 个文件，开始上传...")

        # 生成统一的file_path：用户目录最后一层_时间戳
        import datetime
        dir_name = os.path.basename(os.path.normpath(directory))
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unified_file_path = f"{dir_name}_{timestamp}"
        print(f"📝 统一file_path: {unified_file_path}")

        # 直接执行文件上传，不检查已存在项目
        for i, file_path in enumerate(file_paths):
            try:
                print(f"📤 上传文件 {i+1}/{len(file_paths)}: {file_path}")

                relative_path = os.path.relpath(file_path, directory)

                if i == 0:
                    # 第一个文件不带branch_id
                    result = self.upload_file(file_path,directory=directory, unified_file_path=unified_file_path)
                    self.repo_id = result.get('data',{}).get('repo_id')
                    self.default_branch_id = result.get('data',{}).get('default_branch_id')
                    print(f"✅ 第一个文件上传成功，repo_id: {self.repo_id}, branch_id: {self.default_branch_id}")
                else:
                    # 后续文件带branch_id，使用相同的统一file_path
                    result = self.upload_file(file_path,directory=directory,branch_id= self.default_branch_id, unified_file_path=unified_file_path)
                    print(f"✅ 文件上传成功")

            except Exception as e:
                print(f"❌ 文件上传失败: {file_path}, 错误: {e}")
                return False

        return True

    def check_upload_status(self) -> bool:
        """检查上传状态"""
        if not self.default_branch_id:
            print("❌ 没有有效的branch_id")
            return False

        url = f"{self.base_url}/api/v1/claw/upload/status/"
        data = {"uuid": self.default_branch_id}

        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()

            result = response.json()
            print(f"📊 上传状态: {result}")
            return True

        except Exception as e:
            print(f"❌ 检查上传状态失败: {e}")
            return False

    def generate_document(self, doc_type: str, task_name: str) -> bool:
        """生成指定类型的文档"""
        if not self.repo_id or not self.default_branch_id:
            print("❌ 缺少必要的参数 (repo_id 或 branch_id)")
            return False

        if doc_type not in self.doc_types:
            print(f"❌ 不支持的文档类型: {doc_type}")
            print(f"支持的文档类型: {list(self.doc_types.keys())}")
            return False

        url = f"{self.base_url}/api/v1/claw/template_wiki/"
        data = {
            "task_name": task_name,
            "template_base_id": [{"prefix": "", "uuid": doc_type}],
            "branch_id": self.default_branch_id,
            "repo_id": self.repo_id,
            "is_advanced": False
        }
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()

            result = response.json()
            return True

        except Exception as e:
            print(f"❌ 文档生成失败: {e}")
            return False

    def run(self, directory: str, doc_type: str, task_name: str) -> bool:
        """运行完整的文档生成流程"""
        print(f"🚀 开始处理目录: {directory}")
        print(f"📄 文档类型: {self.doc_types.get(doc_type, doc_type)}")

        # 1. 上传文件
        if not self.upload_all_files(directory):
            return False
        time.sleep(5)
        # 2. 检查上传状态
        if not self.check_upload_status():
            return False

        # 3. 生成文档
        # generate_document 返回 task_id（或 False），这里只关心是否调用成功
        if not self.generate_document(doc_type, task_name):
            return False
        print("文档开始生成，完成后将发送邮件给您")
        return True


def show_document_types():
    """显示所有支持的文档类型"""
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
    print("\n💡 使用方法: python hivulseAI.py <目录> <文档类型编号>")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='hivulseAI - 自动化技术文档生成工具')
    parser.add_argument('directory', nargs='?', help='项目目录路径')
    parser.add_argument('doc_type', nargs='?', help='文档类型编号')
    parser.add_argument('--task-name', help='任务名称', default='自动生成技术文档')
    parser.add_argument('--list-types', action='store_true', help='显示所有支持的文档类型')

    args = parser.parse_args()

    # 如果指定了--list-types，显示文档类型列表
    if args.list_types:
        show_document_types()
        return

    # 检查必需参数
    if not args.directory or not args.doc_type:
        print("❌ 错误: 需要指定目录和文档类型")
        print("\n💡 使用方法: python hivulseAI.py <目录> <文档类型编号>")
        print("💡 查看文档类型: python hivulseAI.py --list-types")
        return

    if not os.path.exists(args.directory):
        print(f"❌ 目录不存在: {args.directory}")
        return

    # 验证文档类型
    doc_types = {
        "19": "用户需求说明书", "2": "需求规格说明书", "4": "系统概要设计说明",
        "5": "系统详细设计说明", "8": "软件单元测试计划", "9": "软件单元测试用例",
        "10": "软件单元测试报告", "1": "系统测试计划", "12": "系统测试用例",
        "15": "系统测试报告", "13": "网络安全漏洞自评报告", "20": "软件用户测试用例",
        "21": "软件用户测试报告"
    }

    if args.doc_type not in doc_types:
        print(f"❌ 不支持的文档类型: {args.doc_type}")
        print("💡 使用 --list-types 查看支持的文档类型")
        return

    # 创建实例并运行
    ai = HivulseAI()
    ai.run(args.directory, args.doc_type, args.task_name)


if __name__ == "__main__":
    main()
