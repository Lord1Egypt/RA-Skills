#!/usr/bin/env python3
"""
core/llm_router.py — Infoseek LLM 多模型路由（v2.0.0 新增）

4 provider 路由策略：
- ollama-local: 本地免费（priority=1）
- zhipu: 智谱 GLM（成本 0.001/1k，priority=2）
- openai: GPT 系列（成本 0.01/1k，priority=3）
- anthropic: Claude 系列（成本 0.015/1k，priority=4）

特性：
- 自动 fallback（首选失败 → 次选）
- 成本控制（prefer_cheap=True 强制最低成本路径）
- 配额感知（per_provider_quota 字典）
- mock 模式（无 API key 时返回模拟响应）
"""

import os
import time
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

# G8-apply: 公共入口类型契约守卫（纯 stdlib，scripts/entry_guard.py）
import sys as _eg_sys
from pathlib import Path as _eg_p
_eg_dir = str(_eg_p(__file__).resolve().parent.parent / 'scripts')
if _eg_dir not in _eg_sys.path:
    _eg_sys.path.insert(0, _eg_dir)
from entry_guard import (require_text, require_mapping, require_sequence, coerce_mapping_list)


@dataclass
class ProviderConfig:
    """LLM Provider 配置"""
    name: str
    cost_per_1k: float  # USD per 1K tokens
    priority: int  # 1=highest priority
    api_key_env: str  # 环境变量名
    endpoint: str
    mock_supported: bool = True
    model: Optional[str] = None  # 默认模型名（v3.0.0 GA 新增）
    openai_compatible: bool = False  # 是否兼容 OpenAI SDK（v3.0.0 GA 新增）
    anthropic_api: bool = False  # 是否走 Anthropic Messages API（v1.0.1 PATCH / G5 新增）
    max_retries: int = 2  # 重试次数（v3.0.0 GA 后续：scnet.cn 转发偶发超时）


# 4 个 provider 配置
PROVIDERS = [
    ProviderConfig(
        name='ollama-local',
        cost_per_1k=0.0,
        priority=1,
        api_key_env='OLLAMA_HOST',
        endpoint='http://localhost:11434',
        mock_supported=True,
    ),
    ProviderConfig(
        name='zhipu',
        cost_per_1k=0.001,
        priority=2,
        api_key_env='ZHIPU_API_KEY',
        endpoint='https://open.bigmodel.cn/api/paas/v4',
        mock_supported=True,
        model='glm-4-flash',  # v1.0.1 PATCH / G5: 默认模型（OpenAI 兼容端点）
        openai_compatible=True,  # v1.0.1 PATCH / G5: 智谱 GLM 支持 chat/completions
    ),
    ProviderConfig(
        name='openai',
        cost_per_1k=0.01,
        priority=3,
        api_key_env='OPENAI_API_KEY',
        endpoint='https://api.openai.com/v1',
        mock_supported=True,
        model='gpt-4o-mini',  # v1.0.1 PATCH / G5: 默认模型
        openai_compatible=True,  # v1.0.1 PATCH / G5: OpenAI 原生兼容
    ),
    ProviderConfig(
        name='anthropic',
        cost_per_1k=0.015,
        priority=4,
        api_key_env='ANTHROPIC_API_KEY',
        endpoint='https://api.anthropic.com/v1',
        mock_supported=True,
        model='claude-haiku-4-5-20251001',  # v1.0.1 PATCH / G5: 默认模型
        anthropic_api=True,  # v1.0.1 PATCH / G5: 走 Anthropic Messages API（非 OpenAI 兼容）
    ),
    ProviderConfig(
        name='deepseek',  # v3.0.0 GA: DeepSeek provider（兼容 OpenAI 接口）
        cost_per_1k=0.0002,  # deepseek-coder 实际价格（input 1 元/M token）
        priority=2,  # 与 zhipu 同级（成本最低之一）
        api_key_env='DEEPSEEK_API_KEY',
        endpoint='https://api.deepseek.com/v1',
        mock_supported=True,
        model='deepseek-chat',
        openai_compatible=True,  # 标记走 OpenAI 客户端
    ),
    ProviderConfig(
        name='kimi',  # v3.0.0 GA: Kimi/moonshot provider（兼容 OpenAI 接口）
        cost_per_1k=0.0012,  # moonshot-v1-8k 标准价格（12 元/M token ≈ $0.0012）
        priority=3,  # 与 openai 同级
        api_key_env='KIMI_API_KEY',  # 用 KIMI_API_KEY 兼容 MOONSHOT_API_KEY
        endpoint='https://api.scnet.cn/api/llm/v1',  # v3.0.0 GA Sprint 4 后续：国家超算中心代理
        mock_supported=True,
        model='Kimi-K2.6',  # 国家超算中心 K2.6 模型（注意大小写 + 点）
        openai_compatible=True,  # 标记走 OpenAI 客户端
        max_retries=3,  # 国家超算中心转发偶发超时，加重试
    ),
]


# Provider 可用性检测
def _is_provider_available(config: ProviderConfig) -> bool:
    """检测 provider 是否可用（有 API key 或本地服务）"""
    if config.name == 'ollama-local':
        # v3.0.0 GA: 仅在 mock 模式（无 deepseek/openai key）时启用
        deepseek_key = os.environ.get('DEEPSEEK_API_KEY')
        openai_key = os.environ.get('OPENAI_API_KEY')
        return not (deepseek_key or openai_key)  # 无更优 provider 时，ollama 兜底
    # v3.0.0 GA: Kimi 兼容 MOONSHOT_API_KEY 别名
    if config.name == 'kimi':
        return bool(os.environ.get('KIMI_API_KEY') or os.environ.get('MOONSHOT_API_KEY'))
    return bool(os.environ.get(config.api_key_env))


def list_available_providers(prefer_provider: Optional[str] = None) -> List[ProviderConfig]:
    """列出所有可用的 provider（按 priority 排序）

    v3.0.0 GA 新增: prefer_provider 优先
    """
    available = [p for p in PROVIDERS if _is_provider_available(p)]
    if prefer_provider:
        # 优先把指定 provider 排到最前
        available.sort(key=lambda p: (0 if p.name == prefer_provider else 1, p.priority))
    else:
        available.sort(key=lambda p: p.priority)
    return available


def select_provider(prefer_cheap: bool = True,
                    prefer_provider: Optional[str] = None) -> Optional[ProviderConfig]:
    """选择首选 provider

    参数:
        prefer_cheap: True=选最便宜的；False=按 priority 选
        prefer_provider: v3.0.0 GA 新增：直接指定 provider（'deepseek' / 'openai' / 等）

    返回:
        ProviderConfig 或 None（无可用）
    """
    available = list_available_providers(prefer_provider=prefer_provider)
    if not available:
        return None
    if prefer_provider:
        # 直接返回首个（已排序）
        return available[0]
    if prefer_cheap:
        return min(available, key=lambda p: (p.cost_per_1k, p.priority))
    return available[0]


def llm_call(prompt: str,
             max_tokens: int = 200,
             temperature: float = 0.3,
             prefer_cheap: bool = True,
             prefer_provider: Optional[str] = None,
             max_retries: int = 3) -> Dict[str, Any]:
    """LLM 调用（带自动 fallback）

    参数:
        prompt: 输入提示
        max_tokens: 最大生成 tokens
        temperature: 温度参数
        prefer_cheap: 优先低成本
        prefer_provider: v3.0.0 GA 新增：直接指定 provider（'deepseek' / 'openai' / 等）
        max_retries: 失败重试次数

    返回:
        {
            'content': 生成内容（mock 或真实）,
            'provider': 实际使用的 provider,
            'cost_estimate': 估算成本,
            'fallback_used': bool,
            'retries': 实际重试次数,
        }
    """
    primary = select_provider(prefer_cheap, prefer_provider=prefer_provider)
    if primary is None:
        return {
            'content': '',
            'provider': None,
            'cost_estimate': 0,
            'fallback_used': False,
            'retries': 0,
            'error': '无可用 provider',
        }

    available = list_available_providers(prefer_provider=prefer_provider)
    retries = 0
    last_error = None

    for attempt_idx, provider in enumerate(available[:max_retries]):
        retries = attempt_idx
        try:
            result = _call_provider(provider, prompt, max_tokens, temperature)
            result['retries'] = retries
            result['fallback_used'] = attempt_idx > 0
            # v1.0.1 B2: token 级用量记录（真实或估算 token → KeyManager 累计）
            try:
                from core.key_manager import KeyManager
                KeyManager.instance().record_usage(
                    provider.name,
                    input_tokens=result.get('input_tokens', 0),
                    output_tokens=result.get('output_tokens', 0))
            except Exception:
                pass
            return result
        except Exception as e:
            last_error = f"{type(e).__name__}: {str(e)[:100]}"
            continue

    return {
        'content': '',
        'provider': primary.name,
        'cost_estimate': 0,
        'fallback_used': True,
        'retries': retries,
        'error': f'所有 provider 调用失败: {last_error}',
    }


def _call_provider(provider: ProviderConfig, prompt: str,
                   max_tokens: int, temperature: float) -> Dict[str, Any]:
    """调用单个 provider

    v3.0.0 GA: 真实 API 调用（deepseek 走 OpenAI 兼容，openai 走 OpenAI SDK）
    无 API key 时降级 mock（保留向后兼容）
    v1.0.1 PATCH: key 经 KeyManager 归一化读取（支持多 key 池/熔断/配额），
    调用结果回注健康状态（成功重置 / 失败累计熔断）
    """
    try:
        from core.key_manager import KeyManager
        km = KeyManager.instance()
        api_key = km.get(provider.name)
    except Exception:
        km = None
        api_key = os.environ.get(provider.api_key_env)  # 兜底：退化原逻辑

    # 真实 API 调用（仅 deepseek 验证过）+ 通用化 OpenAI 兼容
    if api_key and provider.openai_compatible:
        result = _call_openai_compatible(provider, prompt, max_tokens, temperature, api_key)
        # 健康回注：成功/失败反馈 KeyManager（不影响主流程）
        if km is not None:
            try:
                if result.get('error'):
                    km.report_failure(provider.name)
                else:
                    km.report_success(provider.name)
            except Exception:
                pass
        return result

    # v1.0.1 PATCH / G5: Anthropic Messages API（x-api-key 头 + /v1/messages）
    if api_key and provider.anthropic_api:
        result = _call_anthropic(provider, prompt, max_tokens, temperature, api_key)
        if km is not None:
            try:
                if result.get('error'):
                    km.report_failure(provider.name)
                else:
                    km.report_success(provider.name)
            except Exception:
                pass
        return result

    # Mock 兜底
    content = _mock_generate(prompt, provider.name)
    input_tokens = len(prompt.split())
    output_tokens = max_tokens // 4
    cost = (input_tokens + output_tokens) / 1000 * provider.cost_per_1k

    return {
        'content': content,
        'provider': provider.name,
        'cost_estimate': round(cost, 6),
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'model': f'{provider.name}-default',
        'mock': True,
    }


def _call_openai_compatible(provider: ProviderConfig, prompt: str,
                            max_tokens: int, temperature: float,
                            api_key: str) -> Dict[str, Any]:
    """调用 OpenAI 兼容 API（deepseek / openai / kimi 共用）

    v3.0.0 GA 后续：增加 retry 逻辑（应对 scnet.cn 转发偶发超时）
    """
    import time
    max_retries = getattr(provider, 'max_retries', 2)
    retry_delays = [1, 2, 4]  # 指数退避

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            import urllib.request
            import json as json_mod

            url = f"{provider.endpoint.rstrip('/')}/chat/completions"
            # v3.0.0 GA 修复: 规范化 endpoint（避免双 /v1 或双 v1）
            base = provider.endpoint.rstrip('/').removesuffix('/v1')
            url = f"{base}/v1/chat/completions"
            model = provider.model or 'deepseek-chat'

            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a research assistant."},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False,
            }

            req = urllib.request.Request(
                url,
                data=json_mod.dumps(payload).encode('utf-8'),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json_mod.loads(resp.read().decode('utf-8'))

            content = data['choices'][0]['message']['content']
            usage = data.get('usage', {})
            input_tokens = usage.get('prompt_tokens', len(prompt.split()))
            output_tokens = usage.get('completion_tokens', max_tokens // 4)
            cost = (input_tokens + output_tokens) / 1000 * provider.cost_per_1k

            return {
                'content': content,
                'provider': provider.name,
                'cost_estimate': round(cost, 6),
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'model': model,
                'mock': False,
                'attempts': attempt + 1,
            }
        except Exception as e:
            last_error = f"{type(e).__name__}: {str(e)[:200]}"
            if attempt < max_retries:
                # 指数退避（针对 URLError/timeout）
                if 'URLError' in str(type(e)) or 'timeout' in str(e).lower():
                    time.sleep(retry_delays[min(attempt, len(retry_delays)-1)])
                    continue
            break

    # 全部重试失败：降级 mock
    err = last_error or 'unknown'
    content = _mock_generate(prompt, provider.name) + f" [API_ERR: {err}]"
    return {
        'content': content,
        'provider': provider.name,
        'cost_estimate': 0,
        'input_tokens': len(prompt.split()),
        'output_tokens': max_tokens // 4,
        'model': provider.model or 'mock',
        'mock': True,
        'error': err,
        'attempts': max_retries + 1,
    }


def _call_anthropic(provider: ProviderConfig, prompt: str,
                    max_tokens: int, temperature: float,
                    api_key: str) -> Dict[str, Any]:
    """v1.0.1 PATCH / G5: 调用 Anthropic Messages API。

    与 OpenAI 兼容端点不同：
    - header: x-api-key + anthropic-version
    - 端点: POST {endpoint}/v1/messages
    - body: {model, max_tokens, temperature, messages}
    - 返回: content[0].text
    """
    import time as _time
    import urllib.request
    import json as json_mod

    max_retries = getattr(provider, 'max_retries', 2)
    retry_delays = [1, 2, 4]
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            base = provider.endpoint.rstrip('/').removesuffix('/v1')
            url = f"{base}/v1/messages"
            model = provider.model or 'claude-haiku-4-5-20251001'
            payload = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
            req = urllib.request.Request(
                url,
                data=json_mod.dumps(payload).encode('utf-8'),
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                },
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json_mod.loads(resp.read().decode('utf-8'))
            content = data['content'][0]['text']
            usage = data.get('usage', {})
            input_tokens = usage.get('input_tokens', len(prompt.split()))
            output_tokens = usage.get('output_tokens', max_tokens // 4)
            cost = (input_tokens + output_tokens) / 1000 * provider.cost_per_1k
            return {
                'content': content, 'provider': provider.name,
                'cost_estimate': round(cost, 6),
                'input_tokens': input_tokens, 'output_tokens': output_tokens,
                'model': model, 'mock': False, 'attempts': attempt + 1,
            }
        except Exception as e:
            last_error = f"{type(e).__name__}: {str(e)[:200]}"
            if attempt < max_retries and ('URLError' in str(type(e)) or 'timeout' in str(e).lower()):
                _time.sleep(retry_delays[min(attempt, len(retry_delays) - 1)])
                continue
            break

    err = last_error or 'unknown'
    content = _mock_generate(prompt, provider.name) + f" [API_ERR: {err}]"
    return {
        'content': content, 'provider': provider.name, 'cost_estimate': 0,
        'input_tokens': len(prompt.split()), 'output_tokens': max_tokens // 4,
        'model': provider.model or 'mock', 'mock': True, 'error': err,
        'attempts': max_retries + 1,
    }


def _mock_generate(prompt: str, provider_name: str) -> str:
    """模拟 LLM 生成（无 API key 时使用）"""
    snippet = prompt[:60].replace('\n', ' ')
    return f'[{provider_name} mock response] 分析: {snippet}...'


def estimate_cost(prompt: str, max_tokens: int = 200,
                  prefer_cheap: bool = True) -> Dict[str, Any]:
    """估算调用成本（不实际执行）"""
    # G8-apply: 类型契约守卫（拒绝 None/非 str → 受控 TypeError，替代 None.split 崩溃）
    require_text(prompt, "prompt")
    provider = select_provider(prefer_cheap)
    if provider is None:
        return {'error': '无可用 provider'}

    input_tokens = len(prompt.split())
    output_tokens = max_tokens // 4
    cost = (input_tokens + output_tokens) / 1000 * provider.cost_per_1k

    return {
        'provider': provider.name,
        'cost_per_1k': provider.cost_per_1k,
        'estimated_cost': round(cost, 6),
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
    }


# ═══════════════════════════════════════════════════════════════
# CLI 测试
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('=== Provider 列表 ===')
    for p in PROVIDERS:
        available = _is_provider_available(p)
        print(f"  {p.name:15s} priority={p.priority} cost=${p.cost_per_1k}/1k  available={available}")

    print()
    print('=== 可用 provider（按 priority）===')
    for p in list_available_providers():
        print(f"  - {p.name}")

    print()
    print('=== select_provider 测试 ===')
    p1 = select_provider(prefer_cheap=True)
    print(f"  prefer_cheap=True → {p1.name if p1 else None}")
    p2 = select_provider(prefer_cheap=False)
    print(f"  prefer_cheap=False → {p2.name if p2 else None}")

    print()
    print('=== llm_call 测试 ===')
    result = llm_call('钢卷分切工艺的关键参数是什么？', max_tokens=100)
    print(f"  content: {result['content'][:80]}...")
    print(f"  provider: {result['provider']}")
    print(f"  cost: ${result['cost_estimate']}")
    print(f"  fallback_used: {result['fallback_used']}")