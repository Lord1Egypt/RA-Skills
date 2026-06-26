#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def load_rows(path: str) -> list[dict]:
    text = Path(path).read_text(encoding='utf-8').strip()
    if not text:
        return []
    if text.startswith('['):
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    rows: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def salary_text(v: dict) -> str:
    if v.get('salary') and v.get('salary') != 'not listed':
        return str(v['salary'])
    low = v.get('salary_min')
    high = v.get('salary_max')
    cur = v.get('salary_currency') or ''
    if low is None and high is None:
        return 'не указана'
    if low and high and low != high:
        return f"{low:,}-{high:,} {cur}".replace(',', ' ')
    val = high or low
    return f"{val:,} {cur}".replace(',', ' ')


def match_label(v: dict) -> str:
    mapping = {
        'strong-match': 'strong',
        'possible-match': 'possible',
        'skip': 'skip',
        'strong': 'strong',
        'possible': 'possible',
        None: 'unknown',
    }
    return mapping.get(v.get('fit_label'), str(v.get('fit_label')))


def verdict(v: dict) -> str:
    reasons = v.get('fit_reasons') or ([] if not v.get('notes') else [v.get('notes')])
    base = ', '.join(reasons[:2]) if reasons else 'короткая ручная проверка нужна'
    risks = '; '.join((v.get('red_flags') or [])[:2])
    return f"{base}." + (f" Риск: {risks}." if risks else '')


def render_card(v: dict, idx: int) -> str:
    fit_reasons = v.get('fit_reasons') or ([] if not v.get('notes') else [v.get('notes')])
    red_flags = v.get('red_flags') or []
    parts = [
        f"{idx}. {v.get('title') or 'Без названия'} — {v.get('company') or 'Без компании'}",
        f"   Источник: {v.get('source') or 'unknown'}",
        f"   Ссылка: {v.get('source_url') or v.get('url') or 'нет'}",
        f"   Формат: {v.get('remote_mode') or v.get('location') or 'unknown'}",
        f"   Зарплата: {salary_text(v)}",
        f"   Роль/уровень: {v.get('seniority') or 'не указан'}",
        f"   Match: {(v.get('fit_score') if v.get('fit_score') is not None else '?')}/100 · {match_label(v)}",
    ]
    if fit_reasons:
        parts.append('   Почему подходит: ' + '; '.join(fit_reasons[:3]))
    if red_flags:
        parts.append('   Что может мешать: ' + '; '.join(red_flags[:2]))
    parts.append('   Вердикт: ' + verdict(v))
    return '\n'.join(parts)


def render(vacancies: Iterable[dict], title: str) -> str:
    rows = list(vacancies)
    if not rows:
        return f'{title}\n\nНовых релевантных вакансий нет.'
    body = '\n\n'.join(render_card(v, i) for i, v in enumerate(rows, 1))
    return f'{title}\n\n{body}'


def main() -> int:
    parser = argparse.ArgumentParser(description='Render compact Telegram-friendly job report from vacancies JSON/JSONL')
    parser.add_argument('input', help='vacancies json/jsonl path')
    parser.add_argument('--out', help='output text file path')
    parser.add_argument('--min-score', type=int, default=70)
    parser.add_argument('--title', default='Свежий shortlist по job-search')
    args = parser.parse_args()

    vacancies = [
        v for v in load_rows(args.input)
        if (v.get('fit_score') or 0) >= args.min_score or v.get('fit_label') in {'strong-match', 'strong'}
    ]
    text = render(vacancies, args.title)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding='utf-8')
    print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
