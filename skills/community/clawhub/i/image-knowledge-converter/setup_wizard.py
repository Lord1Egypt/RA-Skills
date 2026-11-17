#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片知识库整理工具 - 新手初始化向导（修复版 v1.1.3）

修复内容（v1.1.3）：
1. P0-1: 自动安装缺失的核心依赖（无需手动pip）
2. P0-2: 可选依赖（pytesseract）缺失仅警告，不阻止运行
3. P1-1: 改进错误提示，提供解决方案
"""

import os
import sys
import yaml
import shutil
import subprocess

# ============================================================
# 路径和配置辅助函数
# ============================================================

def get_script_dir():
    """获取脚本所在目录（统一基准路径）"""
    return os.path.dirname(os.path.abspath(__file__))


def get_config_path(filename="api_keys.yaml"):
    """获取配置文件路径（基于脚本目录）"""
    return os.path.join(get_script_dir(), "config", filename)


def get_template_path():
    """获取模板文件路径（基于脚本目录）"""
    return os.path.join(get_script_dir(), "config", "api_keys_template.txt")


def ensure_template_file():
    """确保模板文件存在于脚本目录"""
    template_path = get_template_path()
    if not os.path.exists(template_path):
        # 尝试从工作目录复制
        work_template = os.path.join(os.getcwd(), "config", "api_keys_template.txt")
        if os.path.exists(work_template):
            os.makedirs(os.path.dirname(template_path), exist_ok=True)
            shutil.copy2(work_template, template_path)
    return template_path


def load_existing_config():
    """
    P0-1: 增量更新 - 加载已有配置，与新配置合并
    返回：dict，已存在的配置
    """
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                existing = yaml.safe_load(f)
                if existing is None:
                    return {}
                return existing
        except Exception as e:
            print_warn(f"读取已有配置失败：{e}，将创建新配置")
    return {}


def save_config(config):
    """
    P0-1: 增量更新 - 保存配置（合并后写回）
    """
    config_path = get_config_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    print_success(f"配置已保存到 {config_path}")


def validate_api_key(key):
    """
    P1-2: 校验 API Key 是否有效
    - 非空
    - 不包含占位符（"替换"、"your-"等）
    - 长度合理（>10字符）
    """
    if not key:
        return False
    key = key.strip()
    if len(key) < 10:
        return False
    invalid_patterns = ['替换', 'your-', 'your_', 'YOUR', 'xxx', 'XXXX', 'TODO', '示例', 'example']
    for pattern in invalid_patterns:
        if pattern.lower() in key.lower():
            return False
    return True


# ============================================================
# 依赖检查
# ============================================================

def install_package(package):
    """安装单个包"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package, '-q'],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0
    except Exception as e:
        print_warn(f"安装 {package} 失败：{e}")
        return False


def check_dependencies():
    """检查并安装必要的依赖（自动处理）"""
    print("\n" + "="*50)
    print("  步骤 0：检查依赖包")
    print("="*50)

    # 核心依赖（配置向导必须）—— 锁定版本范围，防止供应链投毒
    core_packages = {
        'pyyaml>=6.0,<7': 'yaml',
        'requests>=2.31,<3': 'requests',
        'python-dotenv>=1.0,<2': 'dotenv',
        'Pillow>=10.0,<12': 'PIL',
    }

    # 可选依赖（主处理脚本需要，缺失时仅警告）
    optional_packages = {
        'pytesseract>=0.3.10,<1': 'pytesseract',
    }

    missing_core = []
    missing_optional = []

    # 检查核心依赖
    for pip_name, import_name in core_packages.items():
        try:
            __import__(import_name)
            print(f"  ✅ {pip_name} 已安装")
        except ImportError:
            print(f"  ⏳ {pip_name} 未安装，正在安装...")
            if install_package(pip_name):
                print(f"  ✅ {pip_name} 安装成功")
            else:
                missing_core.append(pip_name)

    # 检查可选依赖
    for pip_name, import_name in optional_packages.items():
        try:
            __import__(import_name)
            print(f"  ✅ {pip_name} 已安装")
        except ImportError:
            print(f"  ⚠️ {pip_name} 未安装（Tesseract OCR 将不可用）")
            missing_optional.append(pip_name)

    # 核心依赖缺失则退出
    if missing_core:
        print(f"\n  ❌ 核心依赖缺失：{', '.join(missing_core)}")
        print(f"\n  请在终端手动运行：")
        print(f"  pip install {' '.join(missing_core)}")
        print(f"\n  或使用完整安装包：pip install -r requirements_full.txt")
        sys.exit(1)
    else:
        print("\n  ✅ 核心依赖检查完成！")


# ============================================================
# 打印辅助函数
# ============================================================

def print_step(step, text):
    print(f"\n{'='*50}")
    print(f"  第{step}步：{text}")
    print('='*50)

def print_info(text):
    print(f"  ℹ️  {text}")

def print_success(text):
    print(f"  ✅ {text}")

def print_warn(text):
    print(f"  ⚠️  {text}")

def ask_yes_no(prompt):
    while True:
        ans = input(f"{prompt} (y/n): ").strip().lower()
        if ans in ['y', 'yes', '是', '好']:
            return True
        if ans in ['n', 'no', '否', '不']:
            return False
        print("  请输入 y/是 或 n/否")

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        print_success(f"已创建文件夹：{path}")
    else:
        print_info(f"文件夹已存在：{path}")


# ============================================================
# 配置教程函数
# ============================================================

def show_tencent_tutorial():
    print("\n  📖 腾讯云 OCR 密钥获取教程：")
    print("  1. 打开：https://console.cloud.tencent.com/cam/capi")
    print("  2. 登录腾讯云账号（没有的话先注册）")
    print("  3. 点击「新建密钥」")
    print("  4. 记录下「SecretId」和「SecretKey」")
    print("  5. 注意：SecretKey 只显示一次，记得保存！")
    print("\n  免费额度：1000次/月（足够个人使用）")

def show_baidu_tutorial():
    print("\n  📖 百度云 OCR 密钥获取教程：")
    print("  1. 打开：https://console.bce.baidu.com/")
    print("  2. 登录百度云账号")
    print("  3. 进入「产品服务」→「文字识别 OCR」")
    print("  4. 点击「创建应用」，名称随便填")
    print("  5. 创建完成后，记录「API Key」和「Secret Key」")
    print("\n  免费额度：50000次/天")

def show_llm_tutorial(provider):
    """显示 LLM API 获取教程"""
    tutorials = {
        'hunyuan': {
            'name': '混元 Lite',
            'url': 'https://console.cloud.tencent.com/cam/capi',
            'steps': [
                '混元使用与腾讯云 OCR 相同的 SecretId/SecretKey，无需单独获取',
                '打开：https://console.cloud.tencent.com/cam/capi',
                '登录腾讯云账号（没有的话先注册）',
                '点击「新建密钥」，记录 SecretId 和 SecretKey',
                '在上方 OCR 配置中填写相同的密钥即可启用混元'
            ]
        },
        'kimi': {
            'name': 'Kimi',
            'url': 'https://platform.moonshot.cn/',
            'steps': [
                '打开：https://platform.moonshot.cn/',
                '注册并登录账号',
                '进入「API Key 管理」',
                '创建新的 API Key 并复制'
            ]
        },
        'doubao': {
            'name': 'Doubao',
            'url': 'https://www.volcengine.com/product/doubao',
            'steps': [
                '打开：https://www.volcengine.com/product/doubao',
                '注册并登录火山引擎账号',
                '进入「访问控制」→「API Key 管理」',
                '创建新的 API Key 并复制'
            ]
        },
        'siliconflow': {
            'name': '硅基动力',
            'url': 'https://cloud.siliconflow.cn/',
            'steps': [
                '打开：https://cloud.siliconflow.cn/',
                '注册并登录账号',
                '进入「API 密钥管理」',
                '创建新的 API Key 并复制'
            ]
        }
    }

    t = tutorials.get(provider, {})
    print(f"\n  📖 {t.get('name', provider)} API Key 获取教程：")
    for i, step in enumerate(t.get('steps', []), 1):
        print(f"  {i}. {step}")


# ============================================================
# 模板文件读取
# ============================================================

def read_api_from_template():
    """
    P0-2: 从模板文件读取 API 密钥（统一使用脚本目录）
    返回：dict
    """
    template_path = get_template_path()

    # P0-2: 确保模板文件存在
    if not os.path.exists(template_path):
        template_path = ensure_template_file()

    if not os.path.exists(template_path):
        print_warn(f"模板文件不存在：{template_path}")
        return {}

    result = {}
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")

                    if key in ['tencent_secret_id', 'tencent_secret_key',
                              'baidu_api_key', 'baidu_secret_key',
                              'hunyuan_api_key', 'kimi_api_key', 'doubao_api_key',
                              'ima_api_key', 'ima_client_id',
                              'siliconflow_api_key', 'siliconflow_base_url']:
                        result[key] = value

        return result
    except Exception as e:
        print_warn(f"读取模板文件失败：{e}")
        return {}


# ============================================================
# 主向导函数
# ============================================================

def wizard(work_folder_arg=None, non_interactive=False):
    """
    修复后的向导函数 - 按照 6 步流程：
    第1步：指定工作文件夹
    第2步：配置 OCR API（菜单位置修复）
    第3步：配置 LLM API（混元/Kimi/Doubao）
    第4步：配置 IMA 同步（可选）
    第5步：放入待处理图片
    第6步：开始处理

    参数：
    work_folder_arg: 命令行传入的工作文件夹（非交互模式使用）
    non_interactive: 是否非交互模式
    """

    print("\n" + "="*50)
    print("  欢迎使用 图片知识库整理工具！")
    print("  我是你的智能助手，第一次使用我来帮你完成配置")
    print("  只需 6 步，大概 3 分钟\n")
    print("  如果你有任何问题，随时问我！")
    print("="*50)

    # P0-1: 增量更新 - 先加载已有配置
    existing_config = load_existing_config()
    if existing_config:
        print_info("检测到已有配置，将保留之前配置并增量更新")
        config = existing_config
    else:
        config = {}

    # ============================================================
    # 第1步：指定工作文件夹
    # ============================================================
    print_step(1, "指定工作文件夹")
    print_info("这是存放图片和生成文档的地方。")
    print()
    print("  建议选择一个容易找到的文件夹，")
    print("  比如：D:\\WorkBuddy-Projects\\图片知识库\n")

    # 默认使用脚本所在目录
    default_dir = get_script_dir()
    print_info(f"默认位置：{default_dir}")

    if work_folder_arg:
        print_info(f"使用命令行参数指定的工作文件夹：{work_folder_arg}")
        custom_dir = work_folder_arg
    elif non_interactive:
        print_info("非交互模式：使用默认位置")
        custom_dir = ''
    else:
        print_info("（可以直接回车使用默认位置，或输入自定义路径）\n")
        custom_dir = input("  请输入文件夹路径 (直接回车=使用默认): ").strip()

    if not custom_dir:
        work_dir = default_dir
    else:
        work_dir = custom_dir

    # 创建文件夹结构
    try:
        os.makedirs(work_dir, exist_ok=True)
        print_success(f"工作文件夹已设置为：{work_dir}")

        # 创建子文件夹
        print("\n  📁 创建文件夹结构...")
        folders = ["待处理图片", "已处理图片", "处理结果", "config", "logs"]
        for folder in folders:
            full_path = os.path.join(work_dir, folder)
            create_folder(full_path)

        print_success("文件夹结构创建完成！")
        print_info(f"📂 你可以随时把图片放到：{os.path.join(work_dir, '待处理图片')}")
        print_info(f"📂 生成的文档会保存到：{os.path.join(work_dir, '处理结果')}\n")

    except Exception as e:
        print_warn(f"创建文件夹失败：{e}")
        print_info("将使用当前目录作为工作目录")
        work_dir = os.getcwd()

    # 保存工作目录到配置（确保每次都更新）
    config['work_dir'] = work_dir

    # 切换到工作目录（重要！后续所有操作都在这个目录）
    os.chdir(work_dir)
    print_info(f"已切换到工作目录：{os.getcwd()}\n")

    # P0-2: 复制模板文件到工作目录（如果不存在）
    work_template = os.path.join(work_dir, "config", "api_keys_template.txt")
    script_template = get_template_path()
    if not os.path.exists(work_template) and os.path.exists(script_template):
        os.makedirs(os.path.dirname(work_template), exist_ok=True)
        shutil.copy2(script_template, work_template)
        print_success(f"已复制配置模板到：{work_template}")

    # ============================================================
    # 第2步：配置 OCR API（修复：菜单位置移到开头）
    # ============================================================
    print_step(2, "配置 OCR API（图片文字识别）")
    print()
    print("  🌟 请选择配置方案：\n")
    print("  [1] 推荐配置（腾讯云 + 百度云）")
    print("      ✅ 识别率高")
    print("      ✅ 免费额度充足（腾讯云1000次/月 + 百度云50000次/天）")
    print("      ⚠️  需要注册云服务（有邮箱即可）\n")
    print("  [2] 免费方案（只用本地 Tesseract）")
    print("      ✅ 完全免费")
    print("      ✅ 无需注册，离线运行")
    print("      ⚠️  识别率比云端低\n")
    print("  [1,2] 组合使用（推荐！）")
    print("      ✅ 云端优先，本地兜底")
    print("      ✅ 最稳定，不怕网络问题\n")

    choice = input("  请输入选项编号 (1 / 2 / 1,2): ").strip()

    # P0-1: 增量更新 - 确保 ocr 键存在
    if 'ocr' not in config:
        config['ocr'] = {}

    # 根据选择配置 OCR 服务
    if '1' in choice:
        print("\n" + "="*50)
        print("  🌟 方案1：配置腾讯云 + 百度云 OCR")
        print("="*50)
        print("\n  你需要注册两个云服务（都有免费额度）：\n")

        # 腾讯云 OCR
        print("  【第1个】腾讯云 OCR（1000次/月免费）")
        print("  ────────────────────────────────")
        show_tencent_tutorial()

        print("\n  " + "-"*50)
        print("  📝 接下来：")
        print("    1. 获取密钥后，请填入 config/api_keys_template.txt")
        print("    2. 填写 tencent_secret_id: 和 tencent_secret_key: 这两行")
        print("    3. 填写完成后保存文件，然后按回车继续")
        print("  " + "-"*50 + "\n")

        input("  按回车键继续（假设你已填写 config/api_keys_template.txt）...")

        keys = read_api_from_template()
        sid = keys.get('tencent_secret_id', '')
        sk = keys.get('tencent_secret_key', '')

        # P1-2: 使用增强的密钥校验
        if validate_api_key(sid) and validate_api_key(sk):
            config['ocr']['tencent'] = {'secret_id': sid, 'secret_key': sk}
            print_success("腾讯云 OCR 配置成功！")
        else:
            print_warn("腾讯云密钥无效或未填写，请检查 config/api_keys_template.txt")
            print_info("你可以稍后重新运行向导来添加")

        # 百度云 OCR
        print("\n  【第2个】百度云 OCR（50000次/天免费）")
        print("  ────────────────────────────────")
        show_baidu_tutorial()

        print("\n  " + "-"*50)
        print("  📝 接下来：")
        print("    1. 获取密钥后，请填入 config/api_keys_template.txt")
        print("    2. 填写 baidu_api_key: 和 baidu_secret_key: 这两行")
        print("    3. 填写完成后保存文件，然后按回车继续")
        print("  " + "-"*50 + "\n")

        input("  按回车键继续（假设你已填写 config/api_keys_template.txt）...")

        keys = read_api_from_template()
        ak = keys.get('baidu_api_key', '')
        sk = keys.get('baidu_secret_key', '')

        if validate_api_key(ak) and validate_api_key(sk):
            config['ocr']['baidu'] = {'api_key': ak, 'secret_key': sk}
            print_success("百度云 OCR 配置成功！")
        else:
            print_warn("百度云密钥无效或未填写，请检查 config/api_keys_template.txt")
            print_info("你可以稍后重新运行向导来添加")

    if '2' in choice:
        print("\n" + "="*50)
        print("  💰 方案2：配置本地 Tesseract（免费方案）")
        print("="*50)
        print("\n  本地 Tesseract 配置：")
        print("  1. 下载地址：https://github.com/UB-Mannheim/tesseract/wiki")
        print("  2. 安装时记得勾选「中文语言包」")
        print("  3. 安装完成后，需要把 Tesseract 加到系统 PATH")
        print("\n  如果你已经安装过了，直接回车继续...\n")

        input("  按回车键继续...")

        config['ocr']['tesseract'] = {'path': 'tesseract', 'lang': 'chi_sim+eng'}
        print_success("本地 Tesseract 配置完成！")
        print_warn("注意：本地识别率比云端低，建议还是用云端服务。\n")

    # ============================================================
    # 第3步：配置 LLM API
    # ============================================================
    print_step(3, "配置 LLM API（AI 智能分析）")
    print()
    print("  LLM 用于智能分析和命名你的图片内容。")
    print("  配置后，系统会自动：")
    print("    • 分析图片内容")
    print("    • 智能分类（不限定预设类别）")
    print("    • 智能命名（根据内容生成文档名）\n")

    if ask_yes_no("  是否现在配置 LLM API？（推荐配置，能获得更好效果）"):
        print("\n  🌟 请选择 LLM 提供商：\n")
        print("  [1] 混元 Lite（腾讯，推荐）")
        print("      ✅ 免费额度充足")
        print("      ✅ 兼容 OpenAI 格式")
        print("      📖 获取 Key：https://hunyuan.tencent.com/\n")
        print("  [2] Kimi（月之暗面）")
        print("      ✅ 长文本处理能力强")
        print("      📖 获取 Key：https://platform.moonshot.cn/\n")
        print("  [3] Doubao（字节跳动）")
        print("      ✅ 响应速度快")
        print("      📖 获取 Key：https://www.volcengine.com/product/doubao")
        print("="*50 + "\n")

        llm_choice = input("  请输入选项编号 (1/2/3): ").strip()

        llm_provider = None
        llm_api_key = None

        if llm_choice == '1':
            llm_provider = 'hunyuan'
        elif llm_choice == '2':
            llm_provider = 'kimi'
        elif llm_choice == '3':
            llm_provider = 'doubao'

        if llm_provider:
            show_llm_tutorial(llm_provider)

            print("\n  " + "-"*50)
            print("  📝 接下来：")
            print(f"    1. 获取 Key 后，请填入 config/api_keys_template.txt")
            print(f"    2. 填写 {llm_provider}_api_key: 那一行")
            print("    3. 填写完成后保存文件，然后按回车继续")
            print("  " + "-"*50 + "\n")

            input("  按回车键继续（假设你已填写 config/api_keys_template.txt）...")

            keys = read_api_from_template()
            llm_api_key = keys.get(f'{llm_provider}_api_key', '')

            # P1-2: 使用增强的密钥校验
            if validate_api_key(llm_api_key):
                # 配置 LLM（使用与 wizard_processor.py / api_keys.yaml 一致的结构）
                config['llm'] = {
                    'enabled': True,
                    'provider': llm_provider,
                    'hunyuan_api_key': llm_api_key if llm_provider == 'hunyuan' else '',
                    'kimi_api_key': llm_api_key if llm_provider == 'kimi' else '',
                    'doubao_api_key': llm_api_key if llm_provider == 'doubao' else '',
                    'siliconflow_api_key': '',
                    'siliconflow_base_url': 'https://api.siliconflow.cn/v1'
                }
                print_success(f"LLM API 配置完成！（{llm_provider}）")
            else:
                print_warn("LLM API 配置无效或未填写，请检查 config/api_keys_template.txt")
                print_info("你可以稍后重新运行向导来添加。")

        # 可选：硅基动力（兜底LLM）
        print()
        print_info("💡 可选：硅基动力（兜底 LLM，主 LLM 失败时自动切换）")
        if ask_yes_no("  是否配置硅基动力 API Key（免费，可选）？"):
            show_llm_tutorial('siliconflow')
            print("\n  📝 获取 Key 后，填入 config/api_keys_template.txt")
            print("     找到 siliconflow_api_key: 那一行并填写")
            input("\n  按回车键继续（假设你已填写）...")

            keys = read_api_from_template()
            sf_key = keys.get('siliconflow_api_key', '')
            sf_url = keys.get('siliconflow_base_url', 'https://api.siliconflow.cn/v1')

            if validate_api_key(sf_key):
                # 确保 llm 配置存在
                if 'llm' not in config:
                    config['llm'] = {'enabled': True, 'provider': ''}
                config['llm']['siliconflow_api_key'] = sf_key
                config['llm']['siliconflow_base_url'] = sf_url if sf_url and '替换' not in sf_url else 'https://api.siliconflow.cn/v1'
                print_success("硅基动力 API 配置完成！")
            else:
                print_warn("硅基动力 API 无效或未填写")
    else:
        print_info("跳过 LLM 配置，随时可以重新运行本向导来添加。")
        print_info("没有 LLM，系统会使用基础 OCR 识别，不会进行智能分析。\n")

    # ============================================================
    # 第4步：配置 IMA 同步
    # ============================================================
    print_step(4, "配置 IMA 同步（可选）")
    print()
    print("  IMA 是一个笔记服务，可以自动同步你生成的文档。")
    print("  配置后，处理完的图片会自动同步到 IMA 笔记。\n")

    if ask_yes_no("  是否现在配置 IMA 同步？（需要打开 IMA 获取 Key）"):
        print("\n  📖 IMA API Key 获取教程：")
        print("  1. 打开 IMA 设置 → API")
        print("  2. 创建新的 API Key")
        print("  3. 复制 Key\n")
        print("  " + "-"*50)
        print("  📝 接下来：")
        print("    1. 获取 Key 后，请填入 config/api_keys_template.txt")
        print("    2. 填写到 ima_api_key: 那一行")
        print("    3. 填写完成后保存文件，然后按回车继续")
        print("  " + "-"*50 + "\n")

        input("  按回车键继续（假设你已填写 config/api_keys_template.txt）...")

        keys = read_api_from_template()
        ima_api_key = keys.get('ima_api_key', '')

        # P1-2: 使用增强的密钥校验
        if validate_api_key(ima_api_key):
            ima_client_id = keys.get('ima_client_id', '')
            config['ima'] = {
                'enabled': True,
                'client_id': ima_client_id,
                'api_key': ima_api_key
            }
            print_success("IMA 同步配置完成！")
        else:
            print_warn("IMA 配置无效或未填写，请检查 config/api_keys_template.txt")
            print_info("你可以稍后重新运行向导来添加。")
    else:
        print_info("跳过 IMA 配置，随时可以重新运行本向导来添加。")

    # ============================================================
    # 保存配置（P0-1: 增量更新 - 合并后写回）
    # ============================================================
    print("\n" + "="*50)
    print("  保存配置")
    print("="*50)

    save_config(config)

    # ============================================================
    # 第5步：提示用户放入待处理图片
    # ============================================================
    print_step(5, "放入待处理图片")
    print()
    print("  📸 在以下文件夹放入要处理的图片：\n")
    print(f"     {os.path.join(work_dir, '待处理图片')}\n")
    print("  ✅ 支持子文件夹（会自动递归处理）")
    print("  ✅ 支持批量处理（可以放很多张图片）\n")
    print("  示例结构：")
    print("  D:\\WorkBuddy-Projects\\图片知识库\\待处理图片\\")
    print("  ├── 小红书截图1.png")
    print("  ├── 微信读书\\")
    print("  │   └── 读书笔记1.png")
    print("  └── 旅游攻略\\")
    print("      └── 景点介绍.png\n")

    # ============================================================
    # 第6步：提示用户开始处理
    # ============================================================
    print_step(6, "开始处理")
    print()
    print("  🎉 恭喜！配置已完成，现在可以开始使用了：\n")
    print("  【开始处理】在 WorkBuddy 对话框输入：")
    print("     「处理新图片」\n")
    print("  然后等待处理完成即可！\n")
    print("  💡 温馨提示：")
    print("     • 随时可以重新运行本向导：python setup_wizard.py")
    print("     • 有问题请联系开发者\n")

    if ask_yes_no("\n是否现在就把图片放到「待处理图片」文件夹？"):
        print(f"\n  📸 请手动把图片复制到：{os.path.join(work_dir, '待处理图片')}")
        print("  完成后，对 WorkBuddy 说：「处理新图片」")

    print("\n" + "="*50)
    print("  配置向导运行完成！")
    print("="*50 + "\n")


if __name__ == "__main__":
    # 解析命令行参数
    import sys
    work_folder_arg = None
    non_interactive = False
    for i, arg in enumerate(sys.argv):
        if arg == '--work-folder' and i + 1 < len(sys.argv):
            work_folder_arg = sys.argv[i+1]
        if arg == '--non-interactive':
            non_interactive = True

    # 先检查依赖
    check_dependencies()

    if non_interactive and work_folder_arg:
        # 非交互模式：只创建文件夹结构，跳过所有交互
        print("\n" + "="*50)
        print("  非交互模式：创建基础配置")
        print("="*50 + "\n")

        work_dir = work_folder_arg
        os.makedirs(work_dir, exist_ok=True)

        # 创建子文件夹
        folders = ["待处理图片", "已处理图片", "处理结果", "config", "logs"]
        for folder in folders:
            full_path = os.path.join(work_dir, folder)
            if not os.path.exists(full_path):
                os.makedirs(full_path, exist_ok=True)
                print(f"  ✅ 已创建文件夹：{full_path}")
            else:
                print(f"  ℹ️ 文件夹已存在：{full_path}")

        # 复制模板文件
        script_template = os.path.join(get_script_dir(), "config", "api_keys_template.txt")
        work_template = os.path.join(work_dir, "config", "api_keys_template.txt")
        if os.path.exists(script_template) and not os.path.exists(work_template):
            os.makedirs(os.path.dirname(work_template), exist_ok=True)
            shutil.copy2(script_template, work_template)
            print(f"  ✅ 已复制配置模板到：{work_template}")

        print("\n  ✅ 基础配置完成！")
        print("  如需配置 API，请编辑 config/api_keys_template.txt")
        print("  或重新运行：python setup_wizard.py\n")
    else:
        # 交互模式：运行完整向导
        config_path = get_config_path()
        if os.path.exists(config_path):
            print("\n  检测到已有配置文件。")
            if ask_yes_no("是否重新运行向导来更新配置？"):
                wizard()
            else:
                print("  使用现有配置。你可以直接运行：python auto_process_all_v9_4.py")
        else:
            wizard()
