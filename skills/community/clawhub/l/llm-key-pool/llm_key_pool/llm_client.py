"""
统一LLM客户端 - 分层轮询版本
支持多平台OpenAI兼容接口，实现分层轮询、跨层切换和自动故障转移
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

import requests

# 修复Windows控制台中文乱码问题
if sys.platform.startswith('win'):
    import locale
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 支持直接 python 运行（开发模式）
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from llm_key_pool.config_loader import ConfigLoader, ConfigValidationError
from llm_key_pool.key_pool import TieredKeyPool


class TieredLLMClient:
    """分层LLM客户端"""

    def __init__(self, config_path: str):
        """
        初始化LLM客户端

        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load()
        self.global_config = self.config_loader.get_global_config()

        # 按层级组织Key池
        self.tier_pools = {
            'primary': [],
            'daily': [],
            'fallback': []
        }

        # 初始化Key池
        for provider_name in self.config_loader.get_provider_names():
            provider_config = self.config_loader.get_provider_config(provider_name)
            tier = provider_config['tier']

            key_pool = TieredKeyPool(
                provider_name=provider_name,
                tier=tier,
                api_keys=provider_config['api_keys'],
                model=provider_config['model'],
                config=self.global_config
            )

            self.tier_pools[tier].append(key_pool)

        # 当前层级索引
        self.current_tier_index = 0
        self.tier_order = ['primary', 'daily', 'fallback']

    def call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Tuple[str, Dict]:
        """
        调用LLM服务（分层轮询策略）

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大Token数

        Returns:
            (响应文本, 使用信息字典)

        Raises:
            Exception: 所有平台的Key都不可用
        """
        # 构建消息
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # 重试逻辑
        max_retries = self.global_config.get('max_retries', 3)
        retry_delay = self.global_config.get('retry_delay', 1)

        # 按层级轮询
        for attempt in range(max_retries):
            # 尝试从当前层级获取可用的Key
            result = self._try_call_from_tiers(messages, temperature, max_tokens)
            if result:
                return result

            # 如果当前层级都不可用，切换到下一层
            if self.current_tier_index < len(self.tier_order) - 1:
                old_tier = self.tier_order[self.current_tier_index]
                self.current_tier_index += 1
                new_tier = self.tier_order[self.current_tier_index]
                print(f"[SWITCH] 从 {old_tier} 切换到 {new_tier}")
                continue
            else:
                # 所有层级都不可用，重置层级索引
                print("[INFO] 所有层级Key池都不可用，等待冷却后重试...")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    self.current_tier_index = 0
                    continue
                else:
                    raise Exception("调用失败，所有平台的API Key都不可用，请检查配置或等待冷却")

    def _try_call_from_tiers(
        self,
        messages: List[Dict],
        temperature: float,
        max_tokens: int
    ) -> Optional[Tuple[str, Dict]]:
        """
        尝试从当前层级及其后续层级调用

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大Token数

        Returns:
            (响应文本, 使用信息) 或 None
        """
        # 从当前层级开始，依次尝试每个层级
        for tier_idx in range(self.current_tier_index, len(self.tier_order)):
            tier_name = self.tier_order[tier_idx]
            key_pools = self.tier_pools[tier_name]

            # 尝试当前层级的每个Key池
            for key_pool in key_pools:
                if key_pool.has_available_key():
                    try:
                        result = self._call_with_pool(
                            key_pool,
                            messages,
                            temperature,
                            max_tokens
                        )
                        if result:
                            return result
                    except Exception as e:
                        print(f"[WARN] 平台 {key_pool.provider_name} 调用失败: {e}")
                        continue

        return None

    def _call_with_pool(
        self,
        key_pool: TieredKeyPool,
        messages: List[Dict],
        temperature: float,
        max_tokens: int
    ) -> Tuple[str, Dict]:
        """
        使用指定Key池调用API

        Args:
            key_pool: Key池
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大Token数

        Returns:
            (响应文本, 使用信息)

        Raises:
            Exception: 调用失败
        """
        try:
            # 获取API Key
            api_key, key_index = key_pool.get_next_key()
            api_key_preview = api_key[:8] + '...' if len(api_key) > 8 else api_key

            # 显示当前使用的Key信息
            tier_name = key_pool.tier
            print(f"[INFO] 使用平台: {key_pool.provider_name}, 层级: {tier_name}, 模型: {key_pool.model}, Key: {api_key_preview} (索引: {key_index})")

            # 获取平台配置
            provider_config = self.config_loader.get_provider_config(key_pool.provider_name)
            base_url = provider_config['base_url']

            # 统一使用OpenAI兼容接口格式
            # 特殊处理ClaudeCode的API格式
            if key_pool.provider_name == 'claudecode':
                response = self._call_anthropic_format(
                    base_url=base_url,
                    api_key=api_key,
                    model=key_pool.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            else:
                response = self._call_openai_compatible(
                    base_url=base_url,
                    api_key=api_key,
                    model=key_pool.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

            # 提取响应头
            headers = response.headers if hasattr(response, 'headers') else {}

            # 标记Key使用成功
            key_pool.mark_key_success(key_index, dict(headers))

            # 提取响应内容
            content = self._extract_response_content(response)

            # 返回结果和使用信息
            usage_info = {
                'provider': key_pool.provider_name,
                'tier': tier_name,
                'model': key_pool.model,
                'key_index': key_index,
                'temperature': temperature,
                'max_tokens': max_tokens
            }

            return content, usage_info

        except Exception as e:
            error_msg = str(e)
            error_type = self._extract_error_type(error_msg)

            print(f"[ERROR] 调用失败: {error_msg}")

            # 标记Key使用失败
            if 'key_index' in locals():
                key_pool.mark_key_error(key_index, error_type, error_msg)

            raise

    def _call_openai_compatible(
        self,
        base_url: str,
        api_key: str,
        model: str,
        messages: List[Dict],
        temperature: float,
        max_tokens: int
    ):
        """
        调用OpenAI兼容接口

        Args:
            base_url: API基础URL
            api_key: API Key
            model: 模型名称
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大Token数

        Returns:
            响应对象
        """
        url = f"{base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response

    def _call_anthropic_format(
        self,
        base_url: str,
        api_key: str,
        model: str,
        messages: List[Dict],
        temperature: float,
        max_tokens: int
    ):
        """
        调用Anthropic格式接口（ClaudeCode专用）

        Args:
            base_url: API基础URL
            api_key: API Key
            model: 模型名称
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大Token数

        Returns:
            响应对象
        """
        url = f"{base_url}/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }

        # Anthropic需要将system prompt单独提取
        system_prompt = None
        filtered_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                system_prompt = msg['content']
            else:
                # 将role转换为Anthropic格式
                role = 'user' if msg['role'] == 'user' else 'assistant'
                filtered_messages.append({"role": role, "content": msg['content']})

        data = {
            "model": model,
            "messages": filtered_messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        if system_prompt:
            data["system"] = system_prompt

        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response

    def _extract_response_content(self, response) -> str:
        """
        从响应中提取内容

        Args:
            response: 响应对象

        Returns:
            响应文本
        """
        try:
            data = response.json()

            # OpenAI兼容格式
            if 'choices' in data:
                return data['choices'][0]['message']['content']
            # Anthropic格式
            elif 'content' in data:
                return data['content'][0]['text']
            else:
                raise Exception(f"未知的响应格式: {data}")
        except (KeyError, IndexError) as e:
            raise Exception(f"解析响应失败: {str(e)}, 响应内容: {response.text}")

    def _extract_error_type(self, error_msg: str) -> str:
        """
        从错误消息中提取错误类型

        Args:
            error_msg: 错误消息

        Returns:
            错误类型（401, 429, 500等）
        """
        if '401' in error_msg or 'Unauthorized' in error_msg:
            return '401'
        elif '429' in error_msg or 'Too Many Requests' in error_msg:
            return '429'
        elif '500' in error_msg or 'Internal Server Error' in error_msg:
            return '500'
        elif '503' in error_msg or 'Service Unavailable' in error_msg:
            return '503'
        else:
            return 'unknown'

    def get_status(self) -> Dict:
        """
        获取所有平台的Key池状态

        Returns:
            状态信息字典
        """
        status = {
            'tiers': {}
        }

        for tier_name, key_pools in self.tier_pools.items():
            status['tiers'][tier_name] = [pool.get_status() for pool in key_pools]

        return status

    def test_config(self) -> bool:
        """
        测试配置是否正确

        Returns:
            是否测试通过
        """
        print("[INFO] 开始测试配置...")

        all_passed = True
        for tier_name, key_pools in self.tier_pools.items():
            print(f"[INFO] 测试层级: {tier_name}")

            for key_pool in key_pools:
                try:
                    result, usage_info = self.call_llm(
                        prompt="Hello",
                        system_prompt=None,
                        temperature=0.5,
                        max_tokens=10
                    )

                    print(f"[INFO] 平台 {key_pool.provider_name} 测试成功")
                    print(f"[INFO] 响应: {result[:50]}...")

                except Exception as e:
                    print(f"[ERROR] 平台 {key_pool.provider_name} 测试失败: {str(e)}")
                    all_passed = False

        if all_passed:
            print("[INFO] 所有平台测试通过")
        else:
            print("[WARNING] 部分平台测试失败")

        return all_passed


def main():
    """命令行入口"""
    # 默认配置路径：优先Skill目录，然后当前目录
    default_config = './llm_config.yaml'
    skill_config_path = os.path.expanduser('~/.claude/skills/llm-key-pool/llm_config.yaml')
    if os.path.exists(skill_config_path):
        default_config = skill_config_path

    parser = argparse.ArgumentParser(description='LLM Key Pool - 分层轮询多平台API Key管理')
    parser.add_argument('--config', type=str, default=default_config, help='配置文件路径 (默认: ~/.claude/skills/llm-key-pool/llm_config.yaml)')
    parser.add_argument('--prompt', type=str, help='用户提示词')
    parser.add_argument('--system-prompt', type=str, help='系统提示词')
    parser.add_argument('--temperature', type=float, default=0.7, help='温度参数')
    parser.add_argument('--max-tokens', type=int, default=2000, help='最大Token数')
    parser.add_argument('--test', action='store_true', help='测试配置')
    parser.add_argument('--status', action='store_true', help='查看Key池状态')

    args = parser.parse_args()

    try:
        # 初始化客户端
        client = TieredLLMClient(args.config)

        # 查看状态
        if args.status:
            status = client.get_status()
            print(json.dumps(status, indent=2, ensure_ascii=False))
            return 0

        # 测试配置
        if args.test:
            if client.test_config():
                print("[SUCCESS] 配置测试通过")
                return 0
            else:
                print("[FAILED] 配置测试失败")
                return 1

        # 调用LLM
        if not args.prompt:
            parser.print_help()
            print("\n[ERROR] 缺少必需参数: --prompt")
            return 1

        result, usage_info = client.call_llm(
            prompt=args.prompt,
            system_prompt=args.system_prompt,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )

        print("\n=== 响应内容 ===")
        print(f"平台: {usage_info['provider']}")
        print(f"层级: {usage_info['tier']}")
        print(f"模型: {usage_info['model']}")
        print(f"温度: {usage_info['temperature']}")
        print(f"最大Token数: {usage_info['max_tokens']}")
        print("-" * 50)
        print(result)
        print("\n=== 调用完成 ===")

        return 0

    except FileNotFoundError as e:
        print(f"[ERROR] {str(e)}")
        return 1
    except ConfigValidationError as e:
        print(f"[ERROR] 配置验证失败: {str(e)}")
        return 1
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
