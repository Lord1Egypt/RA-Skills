#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片知识库整理工具 - 快速配置脚本（非交互模式）
用于 Skill 触发时自动运行，无需用户交互输入。

用法：
  python quick_setup.py --work-folder "D:\\WorkBuddy-Projects\\图片知识库"
"""

import os
import sys
import shutil


def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def quick_setup(work_folder):
    """快速创建文件夹结构和基础配置（非交互）"""
    print("\n" + "=" * 50)
    print("  快速配置模式（非交互）")
    print("=" * 50 + "\n")

    # 创建工作文件夹
    os.makedirs(work_folder, exist_ok=True)
    print(f"  ✅ 工作文件夹：{work_folder}")

    # 创建子文件夹
    folders = ["待处理图片", "已处理图片", "处理结果", "config", "logs"]
    for folder in folders:
        full_path = os.path.join(work_folder, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"  ✅ 已创建：{folder}")

    # 复制配置模板
    script_template = os.path.join(get_script_dir(), "config", "api_keys_template.txt")
    work_template = os.path.join(work_folder, "config", "api_keys_template.txt")
    if os.path.exists(script_template) and not os.path.exists(work_template):
        shutil.copy2(script_template, work_template)
        print(f"  ✅ 已复制配置模板")

    # 创建基础配置文件（使用本地 Tesseract）
    config_path = os.path.join(work_folder, "config", "api_keys.yaml")
    if not os.path.exists(config_path):
        config_content = """# 图片知识库配置文件
# 使用本地 Tesseract OCR（免费）

ocr:
  tencent:
    enabled: false
    secret_id: ''
    secret_key: ''
  baidu:
    enabled: false
    api_key: ''
    secret_key: ''
  tesseract:
    enabled: true
    path: tesseract
    lang: chi_sim+eng
llm:
  enabled: false
  provider: hunyuan
  hunyuan_api_key: ''
  kimi_api_key: ''
  doubao_api_key: ''
  siliconflow_api_key: ''
  siliconflow_base_url: https://api.siliconflow.cn/v1
ima:
  enabled: false
  client_id: ''
  api_key: ''

# 如需配置云端 OCR 或 LLM，请重新运行：python setup_wizard.py
"""
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"  ✅ 已创建基础配置：{config_path}")

    print("\n" + "=" * 50)
    print("  ✅ 快速配置完成！")
    print("=" * 50)
    print(f"\n📂 工作文件夹：{work_folder}")
    print(f"📂 待处理图片：{os.path.join(work_folder, '待处理图片')}")
    print(f"📂 处理结果：{os.path.join(work_folder, '处理结果')}")

    print("\n" + "-" * 50)
    print("  🔧 下一步：配置 API 密钥")
    print("-" * 50)
    print("\n请选择 OCR 方案（图片文字识别）：\n")
    print("  A. 推荐方案（腾讯云 + 百度云）")
    print("     ✅ 识别率高 | 腾讯1000次/月 + 百度50000次/天")
    print("     📝 需要注册云服务\n")
    print("  B. 免费方案（本地 Tesseract）")
    print("     ✅ 完全免费 | 无需注册")
    print("     ⚠️  识别率较低\n")
    print("  请回复 A 或 B 选择方案，我会帮你完成配置！\n")


if __name__ == "__main__":
    # 解析命令行参数
    work_folder = None
    for i, arg in enumerate(sys.argv):
        if arg == '--work-folder' and i + 1 < len(sys.argv):
            work_folder = sys.argv[i + 1]

    if not work_folder:
        print("用法：python quick_setup.py --work-folder <路径>")
        print("示例：python quick_setup.py --work-folder \"D:\\WorkBuddy-Projects\\图片知识库\"")
        sys.exit(1)

    quick_setup(work_folder)
