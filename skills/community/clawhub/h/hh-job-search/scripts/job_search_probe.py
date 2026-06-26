#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from hh_browser_cli import BrowserCli, BrowserCliError

HH_RESUMES_URL = "https://hh.ru/applicant/resumes"


def read_resume_cards_js(limit_titles: list[str] | None = None) -> str:
    titles_json = json.dumps(limit_titles or [], ensure_ascii=False)
    return rf"""
() => {{
  const onlyWanted = new Set({titles_json});
  const norm = (s) => (s || '').replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim();
  const lines = (document.body.innerText || '').split('\n').map(norm).filter(Boolean);
  const cards = [];
  for (let i = 0; i < lines.length - 2; i++) {{
    const title = lines[i];
    const next = lines[i + 1] || '';
    if (!title || title.length > 120) continue;
    if (!next.includes('Уровень дохода')) continue;
    if (onlyWanted.size && !onlyWanted.has(title)) continue;
    const chunk = lines.slice(i, i + 12);
    const statusLine = chunk.find(line => line.startsWith('Поднять')) || null;
    if (!statusLine) continue;
    const already = cards.find(c => c.title === title);
    if (already) continue;
    cards.push({{
      title,
      order: cards.length,
      statusLine,
      cooldown: !!(statusLine && statusLine.startsWith('Поднять в ') && !statusLine.includes('поиске')),
      available: !!(statusLine && statusLine.includes('Поднять в поиске')),
      chunk,
    }});
  }}
  return cards;
}}
""".strip()


def load_json(path: str):
    text = Path(path).read_text(encoding='utf-8').strip()
    if not text:
        return []
    return json.loads(text)


def delivered_keys(delivery_path: str | None) -> set[str]:
    if not delivery_path:
        return set()
    p = Path(delivery_path)
    if not p.exists():
        return set()
    data = load_json(str(p))
    items = data.get('delivered_vacancies') if isinstance(data, dict) else []
    keys = set()
    for item in items or []:
        company = (item.get('company') or '').strip().lower()
        title = (item.get('title') or '').strip().lower()
        url = (item.get('url') or '').strip().lower()
        if url:
            keys.add('url:' + url)
        if company or title:
            keys.add('ct:' + company + '::' + title)
    return keys


def vacancy_key(v: dict) -> tuple[str, str]:
    url = (v.get('source_url') or v.get('url') or '').strip().lower()
    company = (v.get('company') or '').strip().lower()
    title = (v.get('title') or '').strip().lower()
    return ('url:' + url if url else '', 'ct:' + company + '::' + title)


def shortlist_delta(raw_path: str, delivery_path: str | None, min_score: int = 70) -> list[dict]:
    rows = load_json(raw_path)
    seen = delivered_keys(delivery_path)
    keep = []
    for v in rows:
        score = v.get('fit_score') or 0
        label = v.get('fit_label')
        if score < min_score and label not in {'strong', 'strong-match'}:
            continue
        if label in {'possible', 'possible-match'} and score < 80:
            continue
        k1, k2 = vacancy_key(v)
        if (k1 and k1 in seen) or k2 in seen:
            continue
        keep.append({
            'title': v.get('title'),
            'company': v.get('company'),
            'url': v.get('source_url') or v.get('url'),
            'fit_score': score,
            'fit_label': label,
        })
    return keep


def main() -> int:
    ap = argparse.ArgumentParser(description='Quick status/probe for HH resumes and fresh vacancy delta')
    ap.add_argument('--profile', default='chrome-relay')
    ap.add_argument('--raw-json')
    ap.add_argument('--delivery-json')
    ap.add_argument('--min-score', type=int, default=70)
    ap.add_argument('--titles', nargs='*')
    args = ap.parse_args()

    result = {'ok': True, 'resumes': None, 'delta': None}

    try:
        browser = BrowserCli(profile=args.profile)
        browser.ensure_ready()
        target_id = browser.current_target()
        browser.navigate_js(HH_RESUMES_URL, target_id)
        browser.wait_time(2200, target_id)
        result['resumes'] = browser.evaluate(read_resume_cards_js(args.titles), target_id, retries=2).result or []
    except BrowserCliError as e:
        result['ok'] = False
        result['resume_error'] = str(e)

    if args.raw_json:
        result['delta'] = shortlist_delta(args.raw_json, args.delivery_json, args.min_score)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
