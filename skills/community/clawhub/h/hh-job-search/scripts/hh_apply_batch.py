#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from hh_browser_cli import BrowserCli, BrowserCliError

APPLIED_PATTERNS = [r"Вы\s*откликнулись", r"Резюме доставлено"]
QUESTION_PATTERNS = [r"вопрос", r"сопроводительное", r"textarea", r"ответ"]


def js(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def choose_resume_title(vacancy_title: str) -> str:
    t = vacancy_title.lower()
    if any(x in t for x in ["ml", "mlo", "machine learning", "инженер"]):
        return "ML-инженер"
    return "Data Scientist"


def page_probe_js() -> str:
    applied_union = "|".join(APPLIED_PATTERNS)
    return rf'''
() => {{
  const text = document.body.innerText || '';
  const title = (document.querySelector('h1') || {{innerText: ''}}).innerText || document.title;
  const visible = (el) => !!el && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0;
  const buttons = [...document.querySelectorAll('button,a,[role="button"]')].filter(visible).map(el => (el.innerText || '').trim()).filter(Boolean);
  return {{
    title,
    alreadyApplied: /{applied_union}/i.test(text),
    hasRespondButton: buttons.some(t => /Откликнуться/i.test(t)),
    text: text.slice(0, 10000)
  }};
}}
'''.strip()


def click_respond_js() -> str:
    return r'''
() => {
  const visible = (el) => !!el && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0;
  const buttons = [...document.querySelectorAll('button,a,[role="button"]')]
    .filter(el => visible(el) && /Откликнуться/i.test(el.innerText || ''))
    .sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
  if (!buttons.length) return {ok:false, status:'respond-button-not-found'};
  buttons[0].click();
  return {ok:true, status:'clicked-respond'};
}
'''.strip()


def modal_probe_js(resume_title: str) -> str:
    question_union = "|".join(QUESTION_PATTERNS)
    return f'''
() => {{
  const wanted = {js(resume_title)};
  const text = document.body.innerText || '';
  const visible = (el) => !!el && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0;
  const modalTexts = [...document.querySelectorAll('dialog, [role="dialog"], [aria-modal="true"]')].filter(visible).map(el => (el.innerText || '').trim());
  const modalText = modalTexts.join("\n");
  const resumeButton = [...document.querySelectorAll('button,[role="button"]')].find(el => visible(el) && (el.innerText || '').includes(wanted));
  const applyButton = [...document.querySelectorAll('button,[role="button"]')].find(el => visible(el) && /^Откликнуться$/i.test((el.innerText || '').trim()));
  const textarea = [...document.querySelectorAll('textarea,input')].find(el => visible(el));
  return {{
    wanted,
    hasWantedResume: !!resumeButton,
    hasApplyButton: !!applyButton,
    hasTextarea: !!textarea,
    modalText,
    needsReview: /{question_union}/i.test(modalText) || !!textarea,
  }};
}}
'''.strip()


def click_apply_js(resume_title: str) -> str:
    return f'''
() => {{
  const wanted = {js(resume_title)};
  const visible = (el) => !!el && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0;
  const resumeButton = [...document.querySelectorAll('button,[role="button"]')].find(el => visible(el) && (el.innerText || '').includes(wanted));
  if (resumeButton) resumeButton.click();
  const applyButton = [...document.querySelectorAll('button,[role="button"]')].find(el => visible(el) && /^Откликнуться$/i.test((el.innerText || '').trim()));
  if (!applyButton) return {{ok:false, status:'apply-button-not-found', wanted}};
  applyButton.click();
  return {{ok:true, status:'clicked-apply', wanted}};
}}
'''.strip()


def verify_applied_js() -> str:
    applied_union = "|".join(APPLIED_PATTERNS)
    return rf'''
() => {{
  const text = document.body.innerText || '';
  return {{
    applied: /{applied_union}/i.test(text),
    snippets: (text.match(/.{{0,40}}(Вы\s*откликнулись|Резюме доставлено|Произошла ошибка).{{0,80}}/gi) || []).slice(0, 8)
  }};
}}
'''.strip()


def read_resume_cards_js() -> str:
    return r'''
() => {
  const norm = (s) => (s || '').replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim();
  const lines = (document.body.innerText || '').split('\n').map(norm).filter(Boolean);
  const cards = [];
  for (let i = 0; i < lines.length - 2; i++) {
    const title = lines[i];
    const next = lines[i + 1] || '';
    if (!title || title.length > 120) continue;
    if (!next.includes('Уровень дохода')) continue;
    const chunk = lines.slice(i, i + 12);
    const statusLine = chunk.find(line => line.startsWith('Поднять')) || null;
    if (!statusLine) continue;
    if (cards.find(c => c.title === title)) continue;
    cards.push({
      title,
      order: cards.length,
      statusLine,
      cooldown: !!(statusLine && statusLine.startsWith('Поднять в ') && !statusLine.includes('поиске')),
      available: !!(statusLine && statusLine.includes('Поднять в поиске')),
    });
  }
  return cards;
}
'''.strip()


def click_first_available_raise_js() -> str:
    return r'''
() => {
  const norm = (s) => (s || '').replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim();
  const controls = [...document.querySelectorAll('button,a,[role="button"]')]
    .filter(el => norm(el.innerText || el.textContent || '').includes('Поднять в поиске'));
  const el = controls[0];
  if (!el) return {ok:false, status:'raise-button-not-found', count:controls.length};
  controls[0].click();
  return {ok:true, status:'clicked', count:controls.length};
}
'''.strip()


def raise_available_resumes(browser: BrowserCli, target_id: str, origin: str, wait_ms: int) -> list[dict[str, Any]]:
    browser.navigate_js(f'{origin}/applicant/resumes', target_id)
    browser.wait_time(2200, target_id)
    cards = browser.evaluate(read_resume_cards_js(), target_id, retries=2).result or []
    results: list[dict[str, Any]] = []
    for card in cards:
        item: dict[str, Any] = {'title': card.get('title'), 'status_before': card.get('statusLine')}
        if card.get('cooldown'):
            item['status'] = 'cooldown'
            results.append(item)
            continue
        if not card.get('available'):
            item['status'] = 'raise-button-not-found'
            results.append(item)
            continue
        click = browser.evaluate(click_first_available_raise_js(), target_id, retries=1).result or {}
        browser.wait_time(wait_ms, target_id)
        refreshed = browser.evaluate(read_resume_cards_js(), target_id, retries=2).result or []
        current = next((c for c in refreshed if c.get('title') == card.get('title')), None)
        item['click'] = click
        item['status_after'] = (current or {}).get('statusLine')
        item['status'] = 'raised' if (current or {}).get('cooldown') else (click.get('status') or 'clicked')
        results.append(item)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply to HH vacancies via OpenClaw browser CLI")
    parser.add_argument("urls", nargs="+", help="HH vacancy URLs")
    parser.add_argument("--profile", default="chrome-relay")
    parser.add_argument("--wait-ms", type=int, default=1200)
    parser.add_argument("--skip-raise-after-apply", action="store_true", help="Do not refresh applicant resumes and raise available resumes after a successful apply")
    args = parser.parse_args()

    browser = BrowserCli(profile=args.profile)
    try:
        browser.ensure_ready()
        target_id = browser.current_target()
        current = browser.current_page(target_id).result or {}
        origin = str(current.get("origin") or "https://hh.ru")
        results: list[dict[str, Any]] = []
        for url in args.urls:
            normalized = re.sub(r"^https?://[^/]+", origin, url)
            browser.navigate_js(normalized, target_id)
            browser.wait_time(2200, target_id)
            probe = browser.evaluate(page_probe_js(), target_id).result or {}
            vacancy_title = str(probe.get("title") or "")
            chosen_resume = choose_resume_title(vacancy_title)
            item: dict[str, Any] = {"url": normalized, "title": vacancy_title, "chosen_resume": chosen_resume}
            if probe.get("alreadyApplied"):
                item["status"] = "already-applied"
                results.append(item)
                continue
            if not probe.get("hasRespondButton"):
                item["status"] = "no-respond-button"
                results.append(item)
                continue
            item["respond_click"] = browser.evaluate(click_respond_js(), target_id).result or {}
            browser.wait_time(args.wait_ms, target_id)
            modal = browser.evaluate(modal_probe_js(chosen_resume), target_id).result or {}
            item["modal"] = modal
            if modal.get("needsReview"):
                item["status"] = "requires-review"
                results.append(item)
                continue
            item["apply_click"] = browser.evaluate(click_apply_js(chosen_resume), target_id).result or {}
            browser.wait_time(args.wait_ms, target_id)
            verify = browser.evaluate(verify_applied_js(), target_id).result or {}
            item["verify"] = verify
            item["status"] = "applied" if verify.get("applied") else "apply-unconfirmed"
            if item["status"] == "applied" and not args.skip_raise_after_apply:
                item["post_apply_raise"] = raise_available_resumes(browser, target_id, origin, args.wait_ms)
                browser.navigate_js(normalized, target_id)
                browser.wait_time(args.wait_ms, target_id)
            results.append(item)
        print(json.dumps({"ok": True, "profile": args.profile, "results": results}, ensure_ascii=False, indent=2))
        return 0
    except BrowserCliError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
