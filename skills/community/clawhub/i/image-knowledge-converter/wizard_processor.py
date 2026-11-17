#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片知识库整理工具 - 配置向导处理器
AI 引导用户填写配置模板后，自动读取模板生成最终配置文件。

安全设计：用户的 API 密钥只写入模板文件，不经过对话传递。
"""

import os
import sys
import yaml
from pathlib import Path


def get_work_folder():
    """动态获取工作文件夹（优先级：命令行参数 > 环境变量 > 脚本目录 > 当前目录）"""
    # 1. 命令行参数已通过 main() 的 sys.argv[1] 传入，此处不重复处理
    # 2. 检查环境变量
    env_folder = os.environ.get('WIZARD_WORK_FOLDER', '')
    if env_folder and os.path.isdir(env_folder):
        return env_folder
    # 3. 尝试使用脚本所在目录（解压后的 skill 目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, 'config')
    if os.path.isdir(config_dir):
        return script_dir
    # 4. 兜底：使用当前工作目录
    return os.getcwd()


def get_template_path(work_folder):
    return os.path.join(work_folder, "config", "api_keys_template.txt")


def get_output_path(work_folder):
    return os.path.join(work_folder, "config", "api_keys.yaml")


def parse_template(template_path):
    """解析模板文件，提取各服务的 API 密钥"""
    if not os.path.exists(template_path):
        print(f"  ❌ 模板文件不存在：{template_path}")
        print("  💡 请先在配置向导中让 AI 生成模板文件")
        return None

    result = {
        'ocr': {
            'tencent': {'enabled': False, 'secret_id': '', 'secret_key': ''},
            'baidu': {'enabled': False, 'api_key': '', 'secret_key': ''},
            'tesseract': {'enabled': False, 'path': 'tesseract', 'lang': 'chi_sim+eng'}
        },
        'llm': {
            'enabled': False,
            'provider': '混元',
            'hunyuan_api_key': '',
            'kimi_api_key': '',
            'doubao_api_key': '',
            'siliconflow_api_key': '',
            'siliconflow_base_url': 'https://api.siliconflow.cn/v1'
        },
        'ima': {
            'enabled': False,
            'client_id': '',
            'api_key': ''
        }
    }

    ocr_mode = None  # 'cloud', 'local', 'hybrid'
    current_section = None

    with open(template_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 检测 OCR 模式标记（支持注释和无注释格式）
        # 注释格式: # OCR_MODE: cloud
        # 无注释格式: OCR_MODE: cloud
        # 注意：用户选中的项没有 # 前缀，所以要跳过注释行
        if 'ocr_mode' in line.lower() and not line.strip().startswith('#'):
            ocr_mode = line.split(':', 1)[1].strip().lower().split('#')[0].strip()
            i += 1
            continue

        if line.startswith('# llm_enabled:'):
            val = line.split(':', 1)[1].strip().lower()
            result['llm']['enabled'] = (val in ('true', 'yes', '1'))
            i += 1
            continue

        # LLM 也支持无注释格式：llm_enabled: true/false
        if line.startswith('llm_enabled:'):
            val = line.split(':', 1)[1].strip().lower()
            result['llm']['enabled'] = (val in ('true', 'yes', '1'))
            i += 1
            continue

        if line.startswith('# llm_provider:'):
            result['llm']['provider'] = line.split(':', 1)[1].strip()
            i += 1
            continue

        # LLM provider 也支持无注释格式
        if line.startswith('llm_provider:'):
            result['llm']['provider'] = line.split(':', 1)[1].strip()
            i += 1
            continue

        if line.startswith('# ima_enabled:'):
            val = line.split(':', 1)[1].strip().lower()
            result['ima']['enabled'] = (val in ('true', 'yes', '1'))
            i += 1
            continue

        # IMA 也支持无注释格式：ima_enabled: true/false
        if line.startswith('ima_enabled:'):
            val = line.split(':', 1)[1].strip().lower()
            result['ima']['enabled'] = (val in ('true', 'yes', '1'))
            i += 1
            continue

        # 解析各字段（同时支持冒号和等号格式）
        # 模板用冒号格式，优先用冒号分隔
        # 格式1: key: value   (YAML格式，模板使用)
        # 格式2: key = value  (INI格式)
        if ':' in line:
            # 用冒号分隔（模板格式）
            key, _, value = line.partition(':')
        elif '=' in line:
            # 用等号分隔（INI格式备选）
            key, _, value = line.partition('=')
        else:
            i += 1
            continue
        key = key.strip()
        value = value.strip().strip('"\'')

        # OCR
        if key == 'tencent_secret_id':
            result['ocr']['tencent']['secret_id'] = value
        elif key == 'tencent_secret_key':
            result['ocr']['tencent']['secret_key'] = value
        elif key == 'baidu_api_key':
            result['ocr']['baidu']['api_key'] = value
        elif key == 'baidu_secret_key':
            result['ocr']['baidu']['secret_key'] = value
        elif key == 'use_tesseract':
            if value.lower() in ('true', '1', 'yes'):
                result['ocr']['tesseract']['enabled'] = True
        # LLM
        elif key == 'llm_enabled':
            result['llm']['enabled'] = (value.lower() in ('true', '1', 'yes'))
        elif key == 'llm_provider':
            result['llm']['provider'] = value
        elif key == 'hunyuan_api_key':
            result['llm']['hunyuan_api_key'] = value
        elif key == 'kimi_api_key':
            result['llm']['kimi_api_key'] = value
        elif key == 'doubao_api_key':
            result['llm']['doubao_api_key'] = value
        elif key == 'siliconflow_api_key':
            result['llm']['siliconflow_api_key'] = value
        elif key == 'siliconflow_base_url':
            result['llm']['siliconflow_base_url'] = value
        # IMA
        elif key == 'ima_client_id':
            result['ima']['client_id'] = value
        elif key == 'ima_api_key':
            result['ima']['api_key'] = value

        i += 1

    # 根据 OCR 模式设置启用状态
    if ocr_mode == 'cloud':
        result['ocr']['tencent']['enabled'] = True
        result['ocr']['baidu']['enabled'] = True
        result['ocr']['tesseract']['enabled'] = False
    elif ocr_mode == 'local':
        result['ocr']['tencent']['enabled'] = False
        result['ocr']['baidu']['enabled'] = False
        result['ocr']['tesseract']['enabled'] = True
    elif ocr_mode == 'hybrid':
        result['ocr']['tencent']['enabled'] = True
        result['ocr']['baidu']['enabled'] = True
        result['ocr']['tesseract']['enabled'] = True

    return result


def generate_yaml(config, output_path):
    """生成 api_keys.yaml 配置文件"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False,
                   sort_keys=False)

    print(f"  ✅ 配置文件已生成：{output_path}")


def validate_config(config):
    """验证配置，提示缺失项"""
    issues = []
    ocr_enabled = (config['ocr']['tencent']['enabled'] or
                   config['ocr']['baidu']['enabled'] or
                   config['ocr']['tesseract']['enabled'])

    if not ocr_enabled:
        issues.append("❌ 未启用任何 OCR 服务！请至少选择一种。")

    if config['ocr']['tencent']['enabled']:
        if not config['ocr']['tencent']['secret_id']:
            issues.append("⚠️  腾讯云 SecretId 为空")
        if not config['ocr']['tencent']['secret_key']:
            issues.append("⚠️  腾讯云 SecretKey 为空")

    if config['ocr']['baidu']['enabled']:
        if not config['ocr']['baidu']['api_key']:
            issues.append("⚠️  百度云 API Key 为空")
        if not config['ocr']['baidu']['secret_key']:
            issues.append("⚠️  百度云 Secret Key 为空")

    if config['ocr']['tesseract']['enabled']:
        print("  📌 将使用本地 Tesseract OCR（免费离线）")

    if config['llm']['enabled']:
        provider = config['llm']['provider']
        api_key = ''
        api_key_name = ''
        if provider == '混元' or provider == 'hunyuan':
            # 混元使用腾讯云OCR的SecretId/SecretKey
            if config['ocr']['tencent']['enabled']:
                secret_id = config['ocr']['tencent']['secret_id']
                secret_key = config['ocr']['tencent']['secret_key']
                if secret_id and secret_key:
                    api_key = secret_id  # 只要有值就认为已配置
                    api_key_name = '腾讯云 SecretId/SecretKey'
            if not api_key:
                issues.append(f"⚠️  LLM [混元] 需要腾讯云 SecretId/SecretKey（请确保 OCR 配置已填写）")
        elif provider == 'Kimi' or provider == 'kimi':
            api_key = config['llm']['kimi_api_key']
            api_key_name = 'Kimi API Key'
        elif provider == 'Doubao' or provider == 'doubao':
            api_key = config['llm']['doubao_api_key']
            api_key_name = 'Doubao API Key'
        elif provider == '硅基动力' or provider == 'siliconflow':
            api_key = config['llm']['siliconflow_api_key']
            api_key_name = 'SiliconFlow API Key'

        if api_key_name and not api_key:
            issues.append(f"⚠️  LLM [{provider}] 的 {api_key_name} 为空")

    if config['ima']['enabled']:
        if not config['ima']['api_key']:
            issues.append("⚠️  IMA API Key 为空")

    return issues


def process_wizard_config(work_folder):
    """处理配置向导生成的文件"""
    template_path = get_template_path(work_folder)
    output_path = get_output_path(work_folder)

    print(f"\n🔄 正在处理配置文件...")
    print(f"   模板：{template_path}")

    # 解析模板
    config = parse_template(template_path)
    if config is None:
        return False

    # 验证配置
    issues = validate_config(config)

    if issues:
        print("\n⚠️  配置验证结果：")
        for issue in issues:
            print(f"   {issue}")
        print("\n💡 提示：请重新编辑模板文件，然后再次运行向导")
    else:
        print("\n✅ 配置验证通过！")

    # 生成配置文件
    generate_yaml(config, output_path)

    # 打印配置摘要
    print("\n📋 配置摘要：")
    ocr_modes = []
    if config['ocr']['tencent']['enabled']:
        ocr_modes.append("腾讯云")
    if config['ocr']['baidu']['enabled']:
        ocr_modes.append("百度云")
    if config['ocr']['tesseract']['enabled']:
        ocr_modes.append("本地Tesseract")

    print(f"   OCR：{' + '.join(ocr_modes) if ocr_modes else '未配置'}")
    print(f"   LLM：{'已启用 (' + config['llm']['provider'] + ')' if config['llm']['enabled'] else '未启用'}")
    print(f"   IMA：{'已启用' if config['ima']['enabled'] else '未启用'}")

    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description='图片知识库配置向导处理器')
    parser.add_argument('work_dir_pos', nargs='?', default=None,
                        help='工作文件夹路径（位置参数）')
    parser.add_argument('--work-dir', dest='work_dir', default=None,
                        help='工作文件夹路径（命名参数，与 SKILL.md 一致）')
    args = parser.parse_args()

    # 优先级：--work-dir > 位置参数 > 自动检测
    work_folder = args.work_dir or args.work_dir_pos or get_work_folder()

    success = process_wizard_config(work_folder)

    if success:
        print("\n🎉 配置完成！可以开始处理图片了。")
        sys.exit(0)
    else:
        print("\n⚠️  配置已生成但有缺失项，请检查后重新运行向导。")
        sys.exit(0)  # 仍然返回成功，让向导可以继续


if __name__ == "__main__":
    main()
