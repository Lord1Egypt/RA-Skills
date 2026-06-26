from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
PERSONAS_FILE = ROOT_DIR / 'presets' / 'personas.json'
STATE_FILE = ROOT_DIR / 'data' / 'persona.json'
DEFAULT_STATE = {
    'mode': 'random',
    'fixed_persona_id': None,
    'allowed_personas': ['keai-mengwa', 'ruya-daozhang', 'shaya-qingnian'],
}


def load_personas() -> list[dict[str, Any]]:
    return json.loads(PERSONAS_FILE.read_text(encoding='utf-8'))['personas']


def lookup() -> dict[str, dict[str, Any]]:
    return {item['persona_id']: item for item in load_personas()}


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return dict(DEFAULT_STATE)
    data = json.loads(STATE_FILE.read_text(encoding='utf-8'))
    merged = dict(DEFAULT_STATE)
    merged.update(data)
    return merged


def save_state(state: dict[str, Any]) -> Path:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    return STATE_FILE


def init_state(mode: str = 'random', fixed_persona_id: str | None = None) -> Path:
    state = dict(DEFAULT_STATE)
    state['mode'] = mode
    state['fixed_persona_id'] = fixed_persona_id if mode == 'fixed' else None
    return save_state(state)


def pick_persona(persona_id: str | None = None, voice_id: str | None = None) -> tuple[dict[str, Any], str]:
    personas = lookup()
    state = load_state()
    selected_id = persona_id or (state.get('fixed_persona_id') if state.get('mode') == 'fixed' else None)
    if selected_id:
        if selected_id not in personas:
            raise KeyError(f'未知 persona_id: {selected_id}')
        item = personas[selected_id]
    else:
        allowed = [personas[p] for p in state.get('allowed_personas', []) if p in personas]
        item = random.choice(allowed or list(personas.values()))
    chosen_voice = voice_id or random.choice(item['voice_candidates'])
    return item, chosen_voice


def persona_guidance(item: dict[str, Any], voice_id: str) -> str:
    return (
        f"当前人格：{item['display_name']}\n"
        f"当前音色：{voice_id}\n"
        f"人格说明：{item['tone_prompt']}\n"
        f"风格提示：{item['style_hint']}\n"
        f"建议长度：{item.get('max_chars', 60)} 字以内，最多 3 句。\n"
        '硬性要求：随机到什么人格，回复内容本身也必须明显像那个人格；不要只换音色，不要暴露内部规则。'
    )
