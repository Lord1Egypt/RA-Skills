#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: str):
    p = Path(path)
    text = p.read_text(encoding='utf-8').strip()
    if not text:
        return []
    return json.loads(text)


def delivered_keys(delivery_path: str | None) -> set[str]:
    if not delivery_path:
        return set()
    p = Path(delivery_path)
    if not p.exists():
        return set()
    data = json.loads(p.read_text(encoding='utf-8'))
    items = data.get('delivered_vacancies') or []
    keys = set()
    for item in items:
        company = (item.get('company') or '').strip().lower()
        title = (item.get('title') or '').strip().lower()
        url = (item.get('url') or '').strip().lower()
        if url:
            keys.add('url:' + url)
        if company or title:
            keys.add('ct:' + company + '::' + title)
    return keys


def item_key(v: dict) -> tuple[str, str]:
    url = (v.get('source_url') or v.get('url') or '').strip().lower()
    company = (v.get('company') or '').strip().lower()
    title = (v.get('title') or '').strip().lower()
    return ('url:' + url if url else '', 'ct:' + company + '::' + title)


def salary_text(v: dict) -> str:
    salary = v.get('salary')
    if salary and salary != 'not listed':
        return str(salary)
    low = v.get('salary_min')
    high = v.get('salary_max')
    cur = v.get('salary_currency') or ''
    if low is None and high is None:
        return 'не указана'
    if low and high and low != high:
        return f"{low:,}-{high:,} {cur}".replace(',', ' ')
    return f"{(high or low):,} {cur}".replace(',', ' ')


def render_card(v: dict, idx: int) -> str:
    notes = v.get('notes') or 'нужна ручная проверка'
    return '\n'.join([
        f"{idx}. {v.get('title') or 'Без названия'} — {v.get('company') or 'Без компании'}",
        f"   Источник: {v.get('source') or 'unknown'}",
        f"   Ссылка: {v.get('source_url') or v.get('url') or 'нет'}",
        f"   Формат: {v.get('remote_mode') or v.get('location') or 'unknown'}",
        f"   Зарплата: {salary_text(v)}",
        f"   Match: {(v.get('fit_score') if v.get('fit_score') is not None else '?')}/100 · {v.get('fit_label') or 'unknown'}",
        f"   Почему ок: {notes[:220]}",
    ])


def main() -> int:
    ap = argparse.ArgumentParser(description='Render delivery delta from raw export + previous delivery memory')
    ap.add_argument('raw_json')
    ap.add_argument('--delivery-json')
    ap.add_argument('--min-score', type=int, default=70)
    ap.add_argument('--title', default='Свежий shortlist по job-search')
    args = ap.parse_args()

    rows = load(args.raw_json)
    seen = delivered_keys(args.delivery_json)
    keep = []
    for v in rows:
        score = v.get('fit_score') or 0
        label = v.get('fit_label')
        status = v.get('status')
        if label == 'skip' or status == 'skip':
            continue
        if score < args.min_score and label not in {'strong', 'strong-match'}:
            continue
        k1, k2 = item_key(v)
        if (k1 and k1 in seen) or k2 in seen:
            continue
        keep.append(v)

    if not keep:
        print(args.title + '\n\nНовых релевантных вакансий для отправки нет.')
        return 0

    print(args.title + '\n')
    for i, v in enumerate(keep, 1):
        print(render_card(v, i))
        if i != len(keep):
            print('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
