#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def resume_line(card: dict) -> str:
    title = card.get('title') or 'Без названия'
    status = card.get('status') or card.get('statusLine') or 'неизвестно'
    if card.get('available'):
        verdict = 'можно поднять сейчас'
    elif card.get('cooldown'):
        verdict = status
    else:
        verdict = status
    return f"- {title}: {verdict}"


def vacancy_line(idx: int, item: dict) -> str:
    title = item.get('title') or 'Без названия'
    company = item.get('company') or 'Без компании'
    score = item.get('fit_score')
    label = item.get('fit_label') or 'unknown'
    url = item.get('url') or item.get('source_url') or 'нет ссылки'
    return f"{idx}. {title} — {company} · {score}/100 · {label}\n   {url}"


def main() -> int:
    ap = argparse.ArgumentParser(description='Render Telegram-friendly HH resume + vacancy probe summary')
    ap.add_argument('probe_json')
    ap.add_argument('--title', default='Job-search status update')
    args = ap.parse_args()

    data = load(args.probe_json)
    parts = [args.title]

    resumes = data.get('resumes') or []
    parts.append('\nHH резюме:')
    if resumes:
        parts.extend(resume_line(card) for card in resumes)
    elif data.get('resume_error'):
        parts.append(f"- ошибка: {data['resume_error']}")
    else:
        parts.append('- карточки резюме не найдены')

    delta = data.get('delta') or []
    parts.append('\nНовые релевантные вакансии:')
    if delta:
        parts.extend(vacancy_line(i, item) for i, item in enumerate(delta[:5], 1))
        if len(delta) > 5:
            parts.append(f"… и ещё {len(delta) - 5}")
    else:
        parts.append('- новых релевантных вакансий нет')

    print('\n'.join(parts).strip())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
