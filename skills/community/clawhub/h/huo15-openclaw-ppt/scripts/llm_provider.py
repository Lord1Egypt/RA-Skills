#!/usr/bin/env python3
"""
llm_provider.py — v5.0 多 LLM Provider 抽象（对标 ChatPPT / 国内合规）

参考 huo15_woocommerce_odoo 的 5 provider 模式 + huo15-openclaw-openai-knowledge-base
的 OpenClaw 平台中转。一个 unified `call_llm()` 接口 → 6 个后端：

  anthropic   Claude 直连（默认）— claude-sonnet-4-5 / opus-4-7 / haiku-4-5
  openai      OpenAI 兼容（OpenAI / Azure / 任何兼容服务）
  deepseek    DeepSeek（OpenAI 兼容，URL https://api.deepseek.com）
  qwen        通义千问（dashscope OpenAI 兼容模式）
  doubao      字节豆包（火山引擎 ark.cn-beijing.volces.com）
  openclaw    OpenClaw runtime 中转（读 ~/.openclaw/models.json，参考 kb-llm.py）

环境变量配置（任选一种）：
  PPT_LLM_PROVIDER=anthropic|openai|deepseek|qwen|doubao|openclaw
  PPT_LLM_MODEL=...                  覆盖默认模型
  PPT_LLM_API_KEY=...                provider 的 API key
  PPT_LLM_BASE_URL=https://...       自定义 base URL（OpenAI 兼容服务用）

  # 各 provider 的快捷 env：
  ANTHROPIC_API_KEY                  anthropic
  OPENAI_API_KEY                     openai
  DEEPSEEK_API_KEY                   deepseek
  DASHSCOPE_API_KEY                  qwen（阿里云 dashscope）
  ARK_API_KEY                        doubao（火山引擎）

用法：
    from llm_provider import call_llm

    text = call_llm(
        system="你是 PPT 设计 AI...",
        user="给我做一份发布会演讲",
        max_tokens=4096,
        cache=True,  # 仅 anthropic 支持 prompt caching
    )

兼容性：
  - 现有 prompt_to_deck.call_claude 内部改用 llm_provider.call_llm
  - 现有脚本调用 call_claude 不变（向后兼容）
"""

from __future__ import annotations
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional


PROVIDER_DEFAULTS = {
    'anthropic': {
        'base_url': 'https://api.anthropic.com',
        'model_balanced': 'claude-sonnet-4-5',
        'model_fast': 'claude-haiku-4-5-20251001',
        'model_deep': 'claude-opus-4-7',
        'env_key': 'ANTHROPIC_API_KEY',
    },
    'openai': {
        'base_url': 'https://api.openai.com/v1',
        'model_balanced': 'gpt-4o',
        'model_fast': 'gpt-4o-mini',
        'model_deep': 'o1',
        'env_key': 'OPENAI_API_KEY',
    },
    'deepseek': {
        'base_url': 'https://api.deepseek.com/v1',
        'model_balanced': 'deepseek-chat',
        'model_fast': 'deepseek-chat',
        'model_deep': 'deepseek-reasoner',
        'env_key': 'DEEPSEEK_API_KEY',
    },
    'qwen': {
        'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'model_balanced': 'qwen-plus',
        'model_fast': 'qwen-turbo',
        'model_deep': 'qwen-max',
        'env_key': 'DASHSCOPE_API_KEY',
    },
    'doubao': {
        'base_url': 'https://ark.cn-beijing.volces.com/api/v3',
        'model_balanced': 'doubao-pro-32k',
        'model_fast': 'doubao-lite-32k',
        'model_deep': 'doubao-pro-256k',
        'env_key': 'ARK_API_KEY',
    },
    'openclaw': {
        # 走 OpenClaw runtime，从 ~/.openclaw/models.json 读
        'base_url': None,
        'env_key': None,
    },
}


def get_provider() -> str:
    """从环境变量决定 provider，默认 anthropic"""
    p = os.environ.get('PPT_LLM_PROVIDER', '').lower()
    if p in PROVIDER_DEFAULTS:
        return p
    # 自动检测：哪个 env key 存在就用哪个
    for prov, cfg in PROVIDER_DEFAULTS.items():
        env = cfg.get('env_key')
        if env and os.environ.get(env):
            return prov
    return 'anthropic'


def resolve_model(provider: str, tier: str = 'balanced') -> str:
    """从 PPT_LLM_MODEL 或 provider 默认解析模型"""
    model = os.environ.get('PPT_LLM_MODEL')
    if model:
        return model
    cfg = PROVIDER_DEFAULTS.get(provider, {})
    return cfg.get(f'model_{tier}', cfg.get('model_balanced', 'gpt-4o'))


def resolve_api_key(provider: str) -> str | None:
    """先看 PPT_LLM_API_KEY 再看 provider 专用 env"""
    key = os.environ.get('PPT_LLM_API_KEY')
    if key:
        return key
    env_name = PROVIDER_DEFAULTS.get(provider, {}).get('env_key')
    return os.environ.get(env_name) if env_name else None


def resolve_base_url(provider: str) -> str | None:
    """支持 PPT_LLM_BASE_URL 覆盖"""
    url = os.environ.get('PPT_LLM_BASE_URL')
    if url:
        return url
    return PROVIDER_DEFAULTS.get(provider, {}).get('base_url')


# ============================================================
# Anthropic（带 prompt caching）
# ============================================================

def _call_anthropic(system: str, user: str, model: str,
                    max_tokens: int, api_key: str,
                    cache: bool = True) -> dict:
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("pip install anthropic")
    client = anthropic.Anthropic(api_key=api_key)
    system_blocks = [{"type": "text", "text": system}]
    if cache:
        system_blocks[0]["cache_control"] = {"type": "ephemeral"}
    response = client.messages.create(
        model=model, max_tokens=max_tokens,
        system=system_blocks,
        messages=[{"role": "user", "content": user}],
    )
    usage = response.usage
    info = {
        'text': response.content[0].text.strip(),
        'input_tokens': usage.input_tokens,
        'output_tokens': usage.output_tokens,
        'cache_read': getattr(usage, 'cache_read_input_tokens', 0) or 0,
    }
    return info


# ============================================================
# OpenAI 兼容（OpenAI / DeepSeek / Qwen / Doubao 共用）
# ============================================================

def _call_openai_compat(system: str, user: str, model: str,
                        max_tokens: int, api_key: str,
                        base_url: str) -> dict:
    body = json.dumps({
        'model': model,
        'max_tokens': max_tokens,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user},
        ],
    }).encode('utf-8')
    req = urllib.request.Request(
        f'{base_url.rstrip("/")}/chat/completions',
        data=body, method='POST',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f"HTTP {e.code}: {body_text[:500]}")

    text = data['choices'][0]['message']['content'].strip()
    usage = data.get('usage', {})
    return {
        'text': text,
        'input_tokens': usage.get('prompt_tokens', 0),
        'output_tokens': usage.get('completion_tokens', 0),
        'cache_read': 0,
    }


# ============================================================
# OpenClaw runtime（读 ~/.openclaw/models.json）
# ============================================================

def _call_openclaw(system: str, user: str, model: str,
                   max_tokens: int) -> dict:
    """从 ~/.openclaw/models.json 读 provider 配置（参考 kb-llm.py）"""
    cfg_path = Path.home() / '.openclaw' / 'models.json'
    if not cfg_path.exists():
        raise RuntimeError(
            "缺 ~/.openclaw/models.json\n"
            "OpenClaw runtime LLM 配置文件，让 OpenClaw 平台代为提供 LLM"
        )
    cfg = json.loads(cfg_path.read_text())
    providers = cfg.get('providers', {})
    if not providers:
        raise RuntimeError("~/.openclaw/models.json 没有 providers 配置")

    # 优先 minimax-cn → minimax → 任何
    for pname in ('minimax-cn', 'minimax'):
        if pname in providers:
            prov = providers[pname]
            break
    else:
        pname = next(iter(providers.keys()))
        prov = providers[pname]

    base_url = prov.get('baseUrl', '')
    api_key = prov.get('apiKey') or prov.get('key', '')
    api_type = prov.get('api', '')

    # OpenClaw 的 model 通常 'minimax/MiniMax-M2.7' 这种 prefix 形式
    actual_model = model or prov.get('defaultModel') or 'auto'

    if api_type == 'anthropic-messages':
        # 用 Anthropic-style 调用
        body = json.dumps({
            'model': actual_model,
            'max_tokens': max_tokens,
            'system': system,
            'messages': [{'role': 'user', 'content': user}],
        }).encode('utf-8')
        req = urllib.request.Request(
            f'{base_url}/v1/messages', data=body, method='POST',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01',
            })
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        return {
            'text': data['content'][0]['text'].strip(),
            'input_tokens': data.get('usage', {}).get('input_tokens', 0),
            'output_tokens': data.get('usage', {}).get('output_tokens', 0),
            'cache_read': 0,
        }
    else:
        # 走 OpenAI 兼容
        return _call_openai_compat(
            system, user, actual_model, max_tokens, api_key, base_url)


# ============================================================
# 统一入口
# ============================================================

def call_llm(*, system: str, user: str,
             provider: str | None = None,
             tier: str = 'balanced',
             model: str | None = None,
             max_tokens: int = 4096,
             cache: bool = True,
             verbose: bool = True) -> dict:
    """
    返回 {'text': str, 'input_tokens': int, 'output_tokens': int, 'cache_read': int}
    """
    provider = provider or get_provider()
    model = model or resolve_model(provider, tier)

    if verbose:
        print(f"  🤖 LLM provider={provider} model={model}", file=sys.stderr)

    if provider == 'openclaw':
        result = _call_openclaw(system, user, model, max_tokens)
    elif provider == 'anthropic':
        api_key = resolve_api_key(provider)
        if not api_key:
            raise RuntimeError(f"缺 ANTHROPIC_API_KEY")
        result = _call_anthropic(system, user, model, max_tokens, api_key, cache)
    else:
        # OpenAI 兼容（openai / deepseek / qwen / doubao）
        api_key = resolve_api_key(provider)
        base_url = resolve_base_url(provider)
        if not api_key:
            env = PROVIDER_DEFAULTS[provider].get('env_key', '?')
            raise RuntimeError(f"缺 {env}")
        result = _call_openai_compat(system, user, model, max_tokens,
                                     api_key, base_url)

    if verbose:
        print(f"  📊 token: input={result['input_tokens']} "
              f"output={result['output_tokens']}"
              f"{' cache=' + str(result['cache_read']) if result['cache_read'] else ''}",
              file=sys.stderr)

    return result


def is_enabled(provider: str | None = None) -> tuple[bool, str]:
    """检查 provider 是否可用"""
    provider = provider or get_provider()
    if provider == 'openclaw':
        cfg = Path.home() / '.openclaw' / 'models.json'
        if not cfg.exists():
            return False, "OpenClaw 没 ~/.openclaw/models.json"
        return True, ''
    if provider == 'anthropic':
        try:
            import anthropic  # noqa
        except ImportError:
            return False, "缺 anthropic SDK：pip install anthropic"
    if not resolve_api_key(provider):
        env = PROVIDER_DEFAULTS[provider].get('env_key', 'PPT_LLM_API_KEY')
        return False, f"缺 {env}"
    return True, ''


# ============================================================
# CLI（测试用）
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='火一五 PPT v5.0 LLM provider 测试')
    parser.add_argument('--provider', help='强制 provider')
    parser.add_argument('--tier', default='balanced',
                        choices=['fast', 'balanced', 'deep'])
    parser.add_argument('--model', help='强制 model')
    parser.add_argument('--system', default='你是简洁的 AI 助手。',
                        help='system prompt')
    parser.add_argument('--user', default='用一句话介绍火一五公司。',
                        help='user prompt')
    parser.add_argument('--max-tokens', type=int, default=200)
    parser.add_argument('--list-providers', action='store_true')
    args = parser.parse_args()

    if args.list_providers:
        print("\n  可用 provider 与默认模型：")
        for p, cfg in PROVIDER_DEFAULTS.items():
            avail, reason = is_enabled(p)
            icon = '✅' if avail else '❌'
            models = f"{cfg.get('model_fast', '?')} / {cfg.get('model_balanced', '?')} / {cfg.get('model_deep', '?')}"
            print(f"  {icon} {p:10}  fast/balanced/deep: {models}")
            if not avail:
                print(f"     ↪ {reason}")
        return

    result = call_llm(system=args.system, user=args.user,
                      provider=args.provider, tier=args.tier,
                      model=args.model, max_tokens=args.max_tokens)
    print()
    print(result['text'])


if __name__ == '__main__':
    main()
