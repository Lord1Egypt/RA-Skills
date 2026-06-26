#!/usr/bin/env python3
"""
快速配置脚本
帮助用户快速配置各平台API Key
"""

import os
import sys
import yaml

# 支持直接运行此脚本
_project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from llm_key_pool.llm_client import TieredLLMClient


def create_config_template():
    """创建配置模板"""

    config_template = {
        'providers': {},
        'global': {
            'max_retries': 3,
            'retry_delay': 1,
            'error_threshold': 5,
            'cooldown_seconds': 300,
            'quota_check_enabled': True
        }
    }

    print("=" * 60)
    print("LLM Key Pool - 快速配置向导")
    print("=" * 60)
    print()

    # 小龙虾配置
    print("【1/4】配置小龙虾（XiaoLongXia）")
    xiaolongxia_enable = input("是否配置小龙虾？(y/n, 默认: n): ").strip().lower()
    if xiaolongxia_enable == 'y':
        api_key = input("请输入小龙虾API Key: ").strip()
        if api_key:
            config_template['providers']['xiaolongxia'] = {
                'tier': 'primary',
                'model': 'xiaolongxia-72b',
                'api_keys': [api_key],
                'base_url': 'https://api.xiaolongxia.com/v1'
            }
            print("✓ 小龙虾配置完成")
    print()

    # OpenCode配置
    print("【2/4】配置OpenCode")
    opencode_enable = input("是否配置OpenCode？(y/n, 默认: n): ").strip().lower()
    if opencode_enable == 'y':
        api_key = input("请输入OpenCode API Key: ").strip()
        if api_key:
            config_template['providers']['opencode'] = {
                'tier': 'fallback',
                'model': 'opencode-72b',
                'api_keys': [api_key],
                'base_url': 'https://api.opencode.com/v1'
            }
            print("✓ OpenCode配置完成")
    print()

    # Qwen配置
    print("【3/4】配置Qwen独立API")
    qwen_enable = input("是否配置Qwen？(y/n, 默认: n): ").strip().lower()
    if qwen_enable == 'y':
        api_key = input("请输入Qwen API Key: ").strip()
        model_choice = input("选择模型 (max/plus/turbo/long, 默认: max): ").strip().lower() or 'max'
        model_map = {
            'max': 'qwen-max',
            'plus': 'qwen-plus',
            'turbo': 'qwen-turbo',
            'long': 'qwen-long'
        }
        model = model_map.get(model_choice, 'qwen-max')

        if api_key:
            config_template['providers']['qwen'] = {
                'tier': 'fallback',
                'model': model,
                'api_keys': [api_key],
                'base_url': 'https://api.qwen.ai/v1'
            }
            print(f"✓ Qwen配置完成（模型: {model}）")
    print()

    # ClaudeCode配置
    print("【4/4】配置ClaudeCode")
    claudecode_enable = input("是否配置ClaudeCode？(y/n, 默认: n): ").strip().lower()
    if claudecode_enable == 'y':
        api_key = input("请输入ClaudeCode API Key (sk-ant-xxx): ").strip()
        if api_key and api_key.startswith('sk-ant-'):
            config_template['providers']['claudecode'] = {
                'tier': 'fallback',
                'model': 'claude-3-5-sonnet-20241022',
                'api_keys': [api_key],
                'base_url': 'https://api.anthropic.com/v1'
            }
            print("✓ ClaudeCode配置完成")
        elif api_key:
            print("⚠ 警告: API Key格式不正确，应以 'sk-ant-' 开头")
    print()

    # 保存配置
    if config_template['providers']:
        config_file = 'llm_config.yaml'
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config_template, f, default_flow_style=False, allow_unicode=True)

        print("=" * 60)
        print(f"✓ 配置已保存到 {config_file}")
        print("=" * 60)
        print()
        print("已配置的平台：")
        for provider_name, config in config_template['providers'].items():
            print(f"  - {provider_name} (层级: {config['tier']}, 模型: {config['model']})")
        print()
        print("下一步：")
        print("1. 测试配置：python scripts/llm_client.py --config ./llm_config.yaml --test")
        print("2. 开始使用：python scripts/llm_client.py --config ./llm_config.yaml --prompt '你好'")
    else:
        print("未配置任何平台，配置文件未创建。")


def show_get_api_key_guide():
    """显示获取API Key的指南"""

    print("=" * 60)
    print("获取API Key指南")
    print("=" * 60)
    print()

    print("【小龙虾（XiaoLongXia）】")
    print("1. 访问小龙虾官网")
    print("2. 注册账号并登录")
    print("3. 进入控制台或API管理页面")
    print("4. 创建新的API Key")
    print("5. 复制生成的API Key")
    print()

    print("【OpenCode】")
    print("1. 访问OpenCode官网")
    print("2. 注册开发者账号")
    print("3. 进入API密钥管理页面")
    print("4. 生成新的API Key")
    print("5. 保存API Key（仅显示一次）")
    print()

    print("【Qwen独立API】")
    print("1. 访问通义千问官网（https://qwen.ai）")
    print("2. 注册/登录阿里云账号")
    print("3. 进入API密钥管理")
    print("4. 创建AccessKey")
    print("5. 复制生成的AccessKey")
    print()

    print("【ClaudeCode】")
    print("1. 访问Anthropic控制台（https://console.anthropic.com）")
    print("2. 登录账号（如果没有则注册）")
    print("3. 进入API Keys页面")
    print("4. 点击'Create Key'")
    print("5. 复制生成的API Key（仅显示一次！）")
    print()


def test_config():
    """测试配置"""

    config_file = 'llm_config.yaml'

    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        print("请先运行配置向导创建配置文件")
        return

    print(f"正在测试配置: {config_file}")
    print()

    from llm_key_pool.llm_client import TieredLLMClient

    try:
        client = TieredLLMClient(config_file)
        print("✓ 配置文件格式正确")
        print()

        status = client.get_status()
        print("配置的平台：")
        for tier_name, pools in status['tiers'].items():
            for pool in pools:
                print(f"  - {pool['provider']} (层级: {tier_name}, 模型: {pool['model']})")
        print()

        print("正在测试连接...")
        result, usage_info = client.call_llm(
            prompt="你好",
            temperature=0.7,
            max_tokens=50
        )

        print(f"✓ 连接成功！")
        print(f"  平台: {usage_info['provider']}")
        print(f"  层级: {usage_info['tier']}")
        print(f"  模型: {usage_info['model']}")
        print(f"  响应: {result}")
        print()

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


def main():
    """主函数"""

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  LLM Key Pool - 平台配置助手                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    print("请选择操作：")
    print("1. 快速配置向导（推荐）")
    print("2. 查看获取API Key指南")
    print("3. 测试现有配置")
    print("4. 退出")
    print()

    choice = input("请输入选项 (1/2/3/4): ").strip()

    if choice == '1':
        create_config_template()
    elif choice == '2':
        show_get_api_key_guide()
    elif choice == '3':
        test_config()
    elif choice == '4':
        print("再见！")
    else:
        print("无效选项，请重新运行")


if __name__ == '__main__':
    main()
