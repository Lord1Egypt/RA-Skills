#!/usr/bin/env python3
import html
import json
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'references' / 'background-template.html'

REQUIRED_FIELDS = ['display_name']

DEFAULT_BG_URL = 'https://pub-626ee41d8f1544638070799686c756bf.r2.dev/open-card-bg.png'


def shorten_tokens(s: str) -> str:
    # convert '10.7M tokens' -> '10.7M'
    return s.replace(' tokens', '').strip()


def _resolve_bg(raw: Optional[str]) -> str:
    """返回可直接用于 CSS url() 的背景图地址（URL 或本地 POSIX 路径）。"""
    if raw is None:
        return DEFAULT_BG_URL
    if raw.startswith(('http://', 'https://')):
        return raw
    return Path(raw).as_posix()


def _esc(value: str) -> str:
    """Escape user-provided text for safe HTML insertion."""
    return html.escape(value, quote=True)


def main():
    if len(sys.argv) < 3:
        print('usage: render-background-card.py <data.json> <output.html> [background_url_or_path]', file=sys.stderr)
        sys.exit(1)

    data_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    bg = _resolve_bg(sys.argv[3] if len(sys.argv) > 3 else None)

    data = json.loads(data_path.read_text(encoding='utf-8'))

    # Validate required fields
    missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
    if missing:
        print(f'warning: missing required fields: {missing}', file=sys.stderr)

    # Fallback: if AI didn't fill comment/review, use copy_inputs fallbacks
    copy_inputs = data.get('copy_inputs', {})
    if not data.get('openclaw_review'):
        data['openclaw_review'] = copy_inputs.get('openclaw_review_fallback', '')
    if not data.get('recent_focus'):
        data['recent_focus'] = copy_inputs.get('recent_focus_fallback', '')

    tpl = TEMPLATE.read_text(encoding='utf-8')

    # Escape all user-provided text fields; bg URL is not escaped (used in CSS url())
    replacements = {
        '{{display_name}}': _esc(data.get('display_name', 'Unknown')),
        '{{role_title}}': _esc(data.get('role_title', '')),
        '{{recent_focus}}': _esc(data.get('recent_focus', '')),
        '{{default_model}}': _esc(data.get('default_model', 'Unknown')),
        '{{token_30d_short}}': _esc(shorten_tokens(data.get('token_30d_display', '0 tokens'))),
        '{{skills_count}}': _esc(str(data.get('skills_count', 0))),
        '{{skill_chips}}': ''.join([f'<span class="chip">{_esc(s)}</span>' for s in data.get('skill_names', [])]),
        '{{platform_count}}': _esc(str(len(data.get('platforms', [])))),
        '{{born_label}}': _esc(data.get('born_label', 'Born')),
        '{{born_date}}': _esc(data.get('born_date', '')),
        '{{generated_at}}': _esc(data.get('generated_at', '')),
        '{{platform_chips}}': ''.join([f'<span class="chip">{_esc(p)}</span>' for p in data.get('platforms', [])]),
        '{{openclaw_review}}': _esc(data.get('openclaw_review', '')),
        '{{background_image}}': bg,
    }

    for k, v in replacements.items():
        tpl = tpl.replace(k, v)

    out_path.write_text(tpl, encoding='utf-8')
    print(out_path)


if __name__ == '__main__':
    main()
