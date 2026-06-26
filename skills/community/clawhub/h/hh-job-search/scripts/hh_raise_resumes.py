#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

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
      chunk,
      statusLine,
      cooldown: !!(statusLine && statusLine.startsWith('Поднять в ') && !statusLine.includes('поиске')),
      available: !!(statusLine && statusLine.includes('Поднять в поиске')),
    }});
  }}
  return cards;
}}
""".strip()


def click_first_available_raise_js() -> str:
    return r'''
() => {
  const norm = (s) => (s || '').replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim();
  const controls = [...document.querySelectorAll('button,a,[role="button"]')]
    .filter(el => norm(el.innerText || el.textContent || '').includes('Поднять в поиске'));
  const el = controls[0];
  if (!el) return {ok:false, status:'raise-button-not-found', count:controls.length};
  const before = norm(el.innerText || el.textContent || '');
  el.click();
  return {ok:true, status:'clicked', before, count:controls.length};
}
'''.strip()


def modal_status_js() -> str:
    return """
() => {
  const text = document.body.innerText || '';
  const visible = (el) => !!el && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0;
  const closeBtn = [...document.querySelectorAll('button,[role=\"button\"]')].find(el =>
    visible(el) && (((el.getAttribute('aria-label') || '').includes('Закрыть')) || ['Закрыть', 'Отмена'].includes((el.innerText || '').trim()))
  );
  const outcome = {
    success: text.includes('Готово, вы подняли резюме'),
    cooldown: text.includes('Поднять снова можно через 4 часа'),
  };
  if (closeBtn && (outcome.success || outcome.cooldown)) closeBtn.click();
  return outcome;
}
""".strip()


def main() -> int:
    parser = argparse.ArgumentParser(description='Raise HH resumes via OpenClaw browser CLI')
    parser.add_argument('--profile', default='chrome-relay')
    parser.add_argument('--title', action='append', dest='titles', help='Resume title to raise (repeatable)')
    parser.add_argument('--all-default', action='store_true', help='Compatibility flag; ignored when titles are not passed')
    parser.add_argument('--wait-ms', type=int, default=1200)
    args = parser.parse_args()

    limit_titles = args.titles or None

    browser = BrowserCli(profile=args.profile)
    try:
        browser.ensure_ready()
        target_id = browser.current_target()
        browser.navigate_js(HH_RESUMES_URL, target_id)
        browser.wait_time(2200, target_id)

        cards = browser.evaluate(read_resume_cards_js(limit_titles), target_id, retries=2).result or []
        results: list[dict[str, Any]] = []

        for card in cards:
            item: dict[str, Any] = {'title': card.get('title'), 'card': card}
            if card.get('cooldown'):
                item['status'] = 'cooldown'
                results.append(item)
                continue
            if not card.get('available'):
                item['status'] = 'raise-button-not-found'
                results.append(item)
                continue
            click = browser.evaluate(click_first_available_raise_js(), target_id, retries=1).result or {}
            browser.wait_time(args.wait_ms, target_id)
            modal = browser.evaluate(modal_status_js(), target_id, retries=2).result or {}
            item['click'] = click
            item['modal'] = modal
            item['status'] = 'raised' if modal.get('success') else ('cooldown' if modal.get('cooldown') else click.get('status') or 'clicked')
            results.append(item)

        print(json.dumps({'ok': True, 'profile': args.profile, 'results': results}, ensure_ascii=False, indent=2))
        return 0
    except BrowserCliError as e:
        print(json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
