#!/usr/bin/env python3
"""
OpenClaw Model Card - 模型配置可视化与自动质检
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from typing import Dict, List

# 默认搜索路径（按顺序）
DEFAULT_CONFIG_PATHS = [
    '/opt/openclaw-data/conf/openclaw.json',
    os.path.expanduser('~/.openclaw/openclaw.json'),
    './openclaw.json',
]


def _expand_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def load_config(config_path: str = '') -> Dict:
    """加载 openclaw.json，优先级：--config > OPENCLAW_CONFIG > 默认路径"""
    candidates: List[str] = []

    if config_path:
        candidates.append(_expand_path(config_path))

    env_path = os.environ.get('OPENCLAW_CONFIG', '').strip()
    if env_path:
        candidates.append(_expand_path(env_path))

    candidates.extend(_expand_path(p) for p in DEFAULT_CONFIG_PATHS)

    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error: invalid JSON in {p}: {e}", file=sys.stderr)
                sys.exit(2)

    print(
        "Error: openclaw.json not found. Use --config or OPENCLAW_CONFIG.",
        file=sys.stderr,
    )
    sys.exit(1)


def fmt_ctx(n: int) -> str:
    if n >= 1000000:
        return f"{n // 1000000}M"
    if n >= 1000:
        return f"{n // 1000}k"
    return str(n)


def check_config(config: Dict) -> int:
    """逻辑驱动的通用自动质检"""
    warnings, errors = [], []
    all_models = set()
    all_aliases = {}

    providers = config.get('models', {}).get('providers', {})
    for pname, pinfo in providers.items():
        for model in pinfo.get('models', []):
            mid = model.get('id')
            full_id = f"{pname}/{mid}"
            all_models.add(full_id)

            ctx = model.get('contextWindow', 0)
            if ctx <= 0:
                errors.append(f"❌ {full_id}: contextWindow missing or zero")
            elif ctx < 1000:
                warnings.append(f"⚠️ {full_id}: contextWindow {ctx} suspiciously small")

            if not model.get('input'):
                warnings.append(f"⚠️ {full_id}: input types missing")

    defaults = config.get('agents', {}).get('defaults', {})
    def_models = defaults.get('models', {})
    for key, val in def_models.items():
        if key not in all_models:
            errors.append(f"❌ Default config references undefined model: `{key}`")
        alias = val.get('alias')
        if alias:
            if alias in all_aliases:
                errors.append(
                    f"❌ Alias conflict: `{alias}` used for `{all_aliases[alias]}` and `{key}`"
                )
            all_aliases[alias] = key

    for k in ['model', 'imageModel']:
        cfg = defaults.get(k, {})
        pri = cfg.get('primary')
        if pri and pri not in all_models:
            errors.append(f"❌ {k}.primary `{pri}` not found")
        for fb in cfg.get('fallbacks', []):
            if fb not in all_models:
                warnings.append(f"⚠️ {k}.fallback `{fb}` not found")

    print("\n🔍 Logic Check Report")
    if not errors and not warnings:
        print("✅ No logical inconsistencies found.")
        return 0
    for e in errors:
        print(e)
    for w in warnings:
        print(w)
    return len(errors)


def generate_markdown(config: Dict) -> str:
    """生成 Markdown 表格格式"""
    defaults_models = config.get('agents', {}).get('defaults', {}).get('models', {})
    defaults = config.get('agents', {}).get('defaults', {})
    lines = ['## 📋 OpenClaw Model List', '']

    for pname, pinfo in config.get('models', {}).get('providers', {}).items():
        models = pinfo.get('models', [])
        lines.append(f'### {pname} ({len(models)})')
        lines.append('| Model ID | Alias | Context | Type |')
        lines.append('| :--- | :--- | ---: | :---: |')
        for m in models:
            mid = m.get('id', '-')
            ctx = fmt_ctx(m.get('contextWindow', 0))
            tag = '**Multimodal**' if 'image' in m.get('input', []) else 'Text'
            alias = '-'
            for k, v in defaults_models.items():
                if k == f'{pname}/{mid}':
                    alias = v.get('alias', '') or '-'
                    break
            lines.append(f'| {mid} | `{alias}` | {ctx} | {tag} |')
        lines.append('')

    mcfg, icfg = defaults.get('model', {}), defaults.get('imageModel', {})
    lines.append('---')
    lines.append(f'**🎯 Default:** `{mcfg.get("primary", "")}`')
    lines.append(f'**🔄 Fallbacks:** {", ".join(mcfg.get("fallbacks", [])) or "-"}')
    lines.append(f'**🖼️ Image:** `{icfg.get("primary", "")}`')
    lines.append(
        f'**🖼️ Image Fallbacks:** {", ".join(icfg.get("fallbacks", [])) or "-"}'
    )
    return '\n'.join(lines)


def render_image(markdown: str, output_path: str) -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md2img = os.path.join(script_dir, 'md2img.js')
    output_path = _expand_path(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with tempfile.TemporaryDirectory(prefix='model-card-') as td:
        md_file = os.path.join(td, 'model-list.md')
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        proc = subprocess.run(
            ['node', md2img, md_file, output_path],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.stdout:
            print(proc.stdout.strip())
        if proc.returncode != 0:
            if proc.stderr:
                print(proc.stderr.strip(), file=sys.stderr)
            return proc.returncode

    print(f"Success: {output_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate OpenClaw model list and check consistency.'
    )
    parser.add_argument('--config', help='Path to openclaw.json')
    parser.add_argument(
        '--image',
        nargs='?',
        const='model-card.png',
        help='Render markdown to image (optional output path, default: ./model-card.png)',
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config or '')

    if args.image is not None:
        md_content = generate_markdown(config)
        return render_image(md_content, args.image)

    # CLI Output
    defaults = config.get('agents', {}).get('defaults', {})
    defaults_models = defaults.get('models', {})
    for pname, pinfo in config.get('models', {}).get('providers', {}).items():
        print(f"📦 {pname}")
        for m in pinfo.get('models', []):
            mid = m.get('id', '-')
            full_id = f"{pname}/{mid}"
            ctx = fmt_ctx(m.get('contextWindow', 0))
            alias = ''
            if full_id in defaults_models:
                alias = defaults_models[full_id].get('alias', '') or ''
            alias_str = f" [{alias}]" if alias else ""
            print(f"  - {mid} ({ctx}){alias_str}")

    mcfg = defaults.get('model', {})
    icfg = defaults.get('imageModel', {})
    print(f"\n🎯 Primary: {mcfg.get('primary', '-')}")
    fb = mcfg.get('fallbacks', [])
    if fb:
        print(f"🔄 Fallbacks: {' → '.join(fb)}")
    print(f"🖼️  Image Primary: {icfg.get('primary', '-')}")
    ifb = icfg.get('fallbacks', [])
    if ifb:
        print(f"🔄 Image Fallbacks: {' → '.join(ifb)}")

    return check_config(config)


if __name__ == '__main__':
    raise SystemExit(main())
