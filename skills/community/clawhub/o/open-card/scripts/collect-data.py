#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

HOME = Path.home()
OPENCLAW = HOME / '.openclaw'
WORKSPACE = OPENCLAW / 'workspace'
SESSIONS_DIR = OPENCLAW / 'agents' / 'main' / 'sessions'

_warnings: list[str] = []


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except FileNotFoundError:
        _warnings.append(f"File not found: {path}")
        return ''
    except Exception as e:
        _warnings.append(f"Failed to read {path}: {e}")
        return ''


def compact_model_name(value: str) -> str:
    if not value:
        return 'Unknown'
    tail = value.split('/')[-1]
    if tail.lower().startswith('gpt-'):
        return tail.upper().replace('GPT-', 'GPT-')
    if tail.lower().startswith('qwen'):
        return tail
    return tail


def format_tokens(n: int) -> str:
    if n >= 1_000_000:
        v = n / 1_000_000
        s = f"{v:.1f}".rstrip('0').rstrip('.')
        return f"{s}M tokens"
    if n >= 1_000:
        return f"{round(n/1000)}K tokens"
    return f"{n} tokens"


def get_default_model() -> str:
    config_path = OPENCLAW / 'openclaw.json'
    text = read_text(config_path)
    if not text:
        return 'Unknown'
    try:
        cfg = json.loads(text)
        raw = cfg.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '')
        return compact_model_name(raw) if raw else 'Unknown'
    except json.JSONDecodeError:
        _warnings.append(f"Invalid JSON in {config_path}")
        return 'Unknown'


def extract_md_value(md: str, label: str, default=''):
    for line in md.splitlines():
        if label in line:
            tail = line.split(label, 1)[1].strip()
            return re.sub(r'^[\-*\s]+|[*_`]+', '', tail).strip()
    return default




def get_user_info():
    user = read_text(WORKSPACE / 'USER.md')
    name = extract_md_value(user, '**Name:**', 'Unknown')
    notes = extract_md_value(user, '**Notes:**', '')
    title = ''
    if notes:
        parts = [p.strip() for p in re.split(r'[；;]', notes) if p.strip()]
        title = ' · '.join(parts[:2]) if parts else notes
    if len(title) > 20:
        # Truncate at word/phrase boundary when possible
        cut = title[:20]
        # Try to break at a separator rather than mid-character
        for sep in (' · ', ' ', '·'):
            pos = cut.rfind(sep)
            if pos > 8:
                cut = cut[:pos]
                break
        title = cut + '…'

    return {
        'display_name': name,
        'role_title': title,
        'born_label': 'Born',
        'born_date': '',
    }


def get_recent_focus_fallback():
    """仅提供 recent_focus 的脚本级 fallback，不承担最终文案生成。"""
    user = read_text(WORKSPACE / 'USER.md')
    notes_match = re.search(r'\*\*Notes:\*\*\s*(.+)', user)
    if notes_match:
        notes = notes_match.group(1).strip()
        explore_match = re.search(r'正在探索\s*(.+?)(?:，|。|；|;|$)', notes)
        if explore_match:
            text = re.sub(r'，希望.*$', '', explore_match.group(1).strip())
            return text[:25] + ('…' if len(text) > 25 else '')
        parts = [p.strip() for p in re.split(r'[；;]', notes) if p.strip()]
        if parts:
            first = parts[0]
            return first[:25] + ('…' if len(first) > 25 else '')
    return ''


def get_skills() -> list[str]:
    names = set()
    for skills_dir in [OPENCLAW / 'skills', WORKSPACE / 'skills']:
        if skills_dir.exists():
            for p in skills_dir.iterdir():
                if p.is_dir() and not p.name.startswith('.'):
                    names.add(p.name)
    return sorted(names)


PLATFORM_LABELS = {
    'feishu': '飞书',
    'discord': 'Discord',
    'telegram': 'Telegram',
    'slack': 'Slack',
    'whatsapp': 'WhatsApp',
    'signal': 'Signal',
    'imessage': 'iMessage',
    'line': 'LINE',
    'irc': 'IRC',
    'googlechat': 'Google Chat',
    'webchat': 'WEB',
}


EXCLUDED_PLATFORM_KEYS = {
    'cron',
}


def normalize_platform(raw: str) -> str:
    if not raw:
        return ''
    value = raw.strip()
    lower = value.lower()

    if lower in EXCLUDED_PLATFORM_KEYS:
        return ''

    if lower.startswith('tui-') or lower in {'tui', 'terminal', 'cli', 'console'}:
        return 'CLI'

    if lower in {'web', 'webchat', 'dashboard', 'browser'}:
        return 'WEB'

    if lower in PLATFORM_LABELS:
        return PLATFORM_LABELS[lower]

    return value


def parse_session_file(path: Path, cutoff_ts: float):
    """统计指定时间窗口内的 token 用量。

    只读取每条记录的 type / timestamp / usage.totalTokens 字段，
    不提取任何消息正文或其他敏感内容。
    """
    token_sum = 0
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue

        if obj.get('type') != 'message':
            continue

        ts = obj.get('timestamp')
        if ts:
            try:
                msg_dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                if msg_dt.timestamp() < cutoff_ts:
                    continue
            except Exception:
                pass

        usage = (obj.get('message', {}) or {}).get('usage') \
            or obj.get('usage') \
            or {}
        token_sum += int(usage.get('totalTokens') or 0)
    return token_sum


def get_platforms():
    """从 sessions.json 的结构化元数据中提取已连接平台。

    只读取 session key 结构和 deliveryContext/origin 元数据，
    不访问任何消息正文内容。
    """
    sessions_file = SESSIONS_DIR / 'sessions.json'
    platforms = set()
    try:
        data = json.loads(read_text(sessions_file))
    except Exception:
        return []

    for key, info in data.items():
        parts = key.split(':')
        if len(parts) >= 3:
            raw_platform = parts[2]
            if raw_platform != 'main':
                normalized = normalize_platform(raw_platform)
                if normalized:
                    platforms.add(normalized)

        if not isinstance(info, dict):
            continue
        ctx = info.get('deliveryContext', {}) or {}
        origin = info.get('origin', {}) or {}
        for field in [ctx.get('channel'), origin.get('provider'), origin.get('surface')]:
            if field and field != 'main':
                normalized = normalize_platform(field)
                if normalized:
                    platforms.add(normalized)

    return sorted(platforms)


def get_usage_and_platforms():
    cutoff_ts = (datetime.now(timezone.utc) - timedelta(days=30)).timestamp()
    total = 0
    if SESSIONS_DIR.exists():
        for path in SESSIONS_DIR.glob('*.jsonl'):
            total += parse_session_file(path, cutoff_ts)
    platforms = get_platforms()
    return total, platforms


def get_born_date() -> str:
    """返回 OpenClaw 首次开始运行的日期（YYYY.MM.DD）。

    以 ~/.openclaw/agents/main/sessions 下最早的会话产物时间作为近似的首次运行时间，
    包含当前会话、reset/deleted 历史文件和 sessions.json 索引文件。
    """
    if not SESSIONS_DIR.exists():
        return ''

    earliest_ts = None
    for path in SESSIONS_DIR.iterdir():
        if not path.is_file():
            continue
        name = path.name
        if not (
            name.endswith('.jsonl')
            or '.jsonl.reset.' in name
            or '.jsonl.deleted.' in name
            or name == 'sessions.json'
        ):
            continue
        try:
            ts = path.stat().st_mtime
        except Exception:
            continue
        if earliest_ts is None or ts < earliest_ts:
            earliest_ts = ts

    if earliest_ts is None:
        return ''
    return datetime.fromtimestamp(earliest_ts).strftime('%Y.%m.%d')


def _clean_memory_line(text: str) -> str:
    text = text.strip()
    text = re.sub(r'^-\s*\d{4}-\d{2}-\d{2}:\s*', '', text)
    text = re.sub(r'^-\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_memory_bullets(limit: int = 12):
    """收集 MEMORY.md 与 memory/*.md 中可作为文案素材的 bullet。"""
    all_bullets = []

    memory = read_text(WORKSPACE / 'MEMORY.md')
    all_bullets.extend([_clean_memory_line(line) for line in memory.splitlines() if line.strip().startswith('- ')])

    memory_dir = WORKSPACE / 'memory'
    if memory_dir.exists():
        for md_file in sorted(memory_dir.glob('*.md'), reverse=True):
            content = read_text(md_file)
            all_bullets.extend([_clean_memory_line(line) for line in content.splitlines() if line.strip().startswith('- ')])

    # Filter out skill-internal references (exact script/tool names, not general words)
    _internal_refs = [
        'opencard', 'open-card', 'render-background-card',
        'collect-data.py', 'export-background-card',
        'background-template.html',
    ]
    filtered = []
    for text in all_bullets:
        if len(text) < 12:
            continue
        lower = text.lower()
        if any(ref in lower for ref in _internal_refs):
            continue
        filtered.append(text)
        if len(filtered) >= limit:
            break
    return filtered


def get_copy_fallbacks(token_30d_display: str, platforms: list, skill_names: list):
    user_md = read_text(WORKSPACE / 'USER.md')
    identity_md = read_text(WORKSPACE / 'IDENTITY.md')
    memory_md = read_text(WORKSPACE / 'MEMORY.md')

    return {
        'recent_focus_fallback': get_recent_focus_fallback(),
        'openclaw_review_fallback': '一个对 AI 有自己想法的人。',
        'memory_bullets': get_memory_bullets(),
        # 以下为 AI 生成 comment/review 的完整素材
        'user_md_excerpt': user_md[:2000] if user_md else '',
        'identity_md_excerpt': identity_md[:1000] if identity_md else '',
        'memory_md_excerpt': memory_md[:2000] if memory_md else '',
        'stats_summary': {
            'token_30d': token_30d_display,
            'platforms': platforms,
            'platform_count': len(platforms),
            'skill_names': skill_names,
            'skills_count': len(skill_names),
        },
    }


def main():
    user = get_user_info()
    token_30d, platforms = get_usage_and_platforms()
    skill_names = get_skills()
    data = {
        **user,
        'default_model': get_default_model(),
        'token_30d': token_30d,
        'token_30d_display': format_tokens(token_30d),
        'skill_names': skill_names,
        'skills_count': len(skill_names),
        'platforms': platforms,
        'born_date': get_born_date(),
        # 这三个字段由 agent 最终生成；脚本只提供 fallback 与素材
        'recent_focus': '',
        'openclaw_review': '',
        'copy_inputs': get_copy_fallbacks(format_tokens(token_30d), platforms, skill_names),
        'generated_at': datetime.now().strftime('%Y-%m-%d'),
    }
    if _warnings:
        data['_warnings'] = _warnings
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if _warnings:
        print(f"\n[warn] {len(_warnings)} warning(s) during data collection:", file=sys.stderr)
        for w in _warnings:
            print(f"  - {w}", file=sys.stderr)


if __name__ == '__main__':
    main()
