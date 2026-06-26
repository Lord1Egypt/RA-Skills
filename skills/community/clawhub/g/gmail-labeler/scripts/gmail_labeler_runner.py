#!/usr/bin/env python3
"""Config-driven Gmail labeler runner.

Goals:
- keep the shared skill publishable
- support a local overlay with private accounts/routing
- classify sender as person vs company first
- support dry-run, label-only, and full-action modes
- be safe and idempotent by default

This runner prefers gog for Gmail access. It can also consume a JSON fixture file
for local dry testing.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parseaddr
from pathlib import Path
from typing import Any

LLM_ALLOWED_KEYS = {"category", "actionable", "confidence", "archive", "star", "important", "notify", "reason"}


SYSTEM_LABELS = {"INBOX", "STARRED", "IMPORTANT", "CATEGORY_PROMOTIONS", "CATEGORY_UPDATES"}
LABEL_ALIASES = {
    "Press Release": "Press Releases",
    "Press Releases": "Press Releases",
    "Finance": "Financeiro",
    "Financial": "Financeiro",
    "Fincaceiro": "Financeiro",
    "Finaceiro": "Financeiro",
    "Notifications": "Notification",
    "Updates": "Notification",
}


def canonicalize_label(label: str) -> str:
    return LABEL_ALIASES.get(str(label).strip(), str(label).strip())


def canonicalize_labels(labels: list[str]) -> list[str]:
    seen=[]
    for x in labels:
        c=canonicalize_label(str(x))
        if c and c not in seen:
            seen.append(c)
    return seen


@dataclass
class Decision:
    filter_id: str
    kind: str
    confidence: float
    sender_type: str
    urgent: bool
    reasons: list[str]
    actions: dict[str, Any]


def deep_merge(base: Any, overlay: Any) -> Any:
    if isinstance(base, dict) and isinstance(overlay, dict):
        result = deepcopy(base)
        for key, value in overlay.items():
            if key in result:
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = deepcopy(value)
        return result
    if isinstance(base, list) and isinstance(overlay, list):
        return deepcopy(base) + deepcopy(overlay)
    return deepcopy(overlay)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def root_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def default_logs_dir() -> Path:
    return Path('/home/ubuntu/.openclaw/gmail-labeler-logs')


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def purge_old_logs(log_dir: Path, retention_days: int) -> list[str]:
    removed: list[str] = []
    cutoff = now_utc() - timedelta(days=retention_days)
    if not log_dir.exists():
        return removed
    for child in log_dir.glob('*.jsonl'):
        try:
            mtime = datetime.fromtimestamp(child.stat().st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                child.unlink()
                removed.append(str(child))
        except FileNotFoundError:
            pass
    return removed


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    ensure_dir(path.parent)
    with path.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + '\n')


def load_config(local_path: str | None) -> dict[str, Any]:
    defaults = load_json(root_dir() / "references" / "default-config.json")
    if not local_path:
        config = defaults
    else:
        config = deep_merge(defaults, load_json(Path(local_path).expanduser()))
    config.setdefault('logging', {})
    config['logging'].setdefault('dir', str(default_logs_dir()))
    config['logging'].setdefault('retentionDays', 30)
    return config


def normalize_sender(message: dict[str, Any]) -> tuple[str, str]:
    sender_raw = str(message.get("from", "") or "")
    display_name, addr = parseaddr(sender_raw)
    return display_name.strip(), addr.lower().strip()


def headers_map(message: dict[str, Any]) -> dict[str, str]:
    raw = message.get("headers") or {}
    if isinstance(raw, dict):
        return {str(k): str(v) for k, v in raw.items()}
    return {}


def body_text(message: dict[str, Any]) -> str:
    parts = [
        str(message.get("subject", "") or ""),
        str(message.get("snippet", "") or ""),
        str(message.get("body", "") or ""),
    ]
    return "\n".join(parts)


def domain_of(addr: str) -> str:
    return addr.split("@", 1)[1] if "@" in addr else ""


def is_known_person(addr: str, config: dict[str, Any]) -> bool:
    people = set(x.lower() for x in config.get("people", {}).get("knownPeople", []))
    domains = set(x.lower() for x in config.get("people", {}).get("knownPersonDomains", []))
    return addr in people or domain_of(addr) in domains


def is_vip(addr: str, config: dict[str, Any]) -> bool:
    vip = set(x.lower() for x in config.get("people", {}).get("vipSenders", []))
    vip_domains = set(x.lower() for x in config.get("people", {}).get("vipDomains", []))
    return addr in vip or domain_of(addr) in vip_domains


def classify_sender_type(message: dict[str, Any], config: dict[str, Any]) -> tuple[str, list[str]]:
    display_name, addr = normalize_sender(message)
    headers = headers_map(message)
    text = body_text(message).lower()
    reasons: list[str] = []

    if is_known_person(addr, config):
        return "person", ["known person allowlist"]

    if is_vip(addr, config):
        return "person", ["VIP sender"]

    local_part = addr.split("@", 1)[0] if "@" in addr else addr
    company_local_parts = [x.lower() for x in config.get("senderHeuristics", {}).get("companyLocalParts", [])]
    if any(token in local_part for token in company_local_parts):
        reasons.append("role-based/company local part")

    header_hints = config.get("senderHeuristics", {}).get("companyHeaderHints", [])
    if any(h in headers for h in header_hints):
        reasons.append("automation header hint")

    if re.search(r"unsubscribe|view in browser|manage preferences", text):
        reasons.append("marketing footer")

    if display_name and re.search(r"support|billing|team|newsletter|updates|notification", display_name.lower()):
        reasons.append("role-based display name")

    if reasons:
        return "company", reasons

    if display_name and " " in display_name and addr and not re.search(r"no-?reply|support|billing|team", addr):
        return "person", ["human-style display name"]

    return "person_or_unknown", ["no strong sender signal"]


def contains_any(text: str, needles: list[str]) -> tuple[bool, list[str]]:
    hits = [n for n in needles if n.lower() in text.lower()]
    return bool(hits), hits


def eval_node(message: dict[str, Any], node: dict[str, Any]) -> tuple[bool, list[str]]:
    subject = str(message.get("subject", "") or "")
    body = str(message.get("body", "") or "")
    snippet = str(message.get("snippet", "") or "")
    sender = str(message.get("from", "") or "")
    headers = headers_map(message)
    body_plus = "\n".join([subject, snippet, body])

    if "all" in node:
        reasons: list[str] = []
        for child in node["all"]:
            ok, child_reasons = eval_node(message, child)
            if not ok:
                return False, []
            reasons.extend(child_reasons)
        return True, reasons

    if "any" in node:
        reasons: list[str] = []
        for child in node["any"]:
            ok, child_reasons = eval_node(message, child)
            if ok:
                reasons.extend(child_reasons)
        return (len(reasons) > 0), reasons

    if "none" in node:
        matched: list[str] = []
        for child in node["none"]:
            ok, child_reasons = eval_node(message, child)
            if ok:
                matched.extend(child_reasons)
        return (len(matched) == 0), []

    if "subjectIncludes" in node:
        ok, hits = contains_any(subject, node["subjectIncludes"])
        return ok, [f"subject includes: {h}" for h in hits]

    if "subjectStartsWith" in node:
        hits = [x for x in node["subjectStartsWith"] if subject.startswith(x)]
        return bool(hits), [f"subject starts with: {h}" for h in hits]

    if "bodyIncludes" in node:
        ok, hits = contains_any(body_plus, node["bodyIncludes"])
        return ok, [f"body includes: {h}" for h in hits]

    if "fromIncludes" in node:
        ok, hits = contains_any(sender, node["fromIncludes"])
        return ok, [f"from includes: {h}" for h in hits]

    if "headersPresent" in node:
        present = [h for h in node["headersPresent"] if h in headers]
        return len(present) == len(node["headersPresent"]), [f"header present: {h}" for h in present]

    return False, []


def score_confidence(rule_reasons: list[str], sender_reasons: list[str], filt: dict[str, Any]) -> float:
    base = float(filt.get("baseConfidence", 0.55))
    score = base + min(0.25, 0.05 * len(rule_reasons)) + min(0.10, 0.03 * len(sender_reasons))
    return round(min(0.99, score), 2)


def is_urgent(decision_filter_id: str, message: dict[str, Any], config: dict[str, Any]) -> bool:
    urgent_filters = set(config.get("notifications", {}).get("urgentFilters", []))
    if decision_filter_id in urgent_filters:
        return True
    urgent_terms = [x.lower() for x in config.get("notifications", {}).get("urgentTerms", [])]
    text = body_text(message).lower()
    return any(term in text for term in urgent_terms)


def eligible_sender_type(actual: str, expected: str) -> bool:
    if expected == "person_or_unknown":
        return actual in {"person", "person_or_unknown"}
    return actual == expected


def never_archive(message: dict[str, Any], config: dict[str, Any]) -> bool:
    _, addr = normalize_sender(message)
    domains = set(x.lower() for x in config.get("people", {}).get("neverArchiveDomains", []))
    senders = set(x.lower() for x in config.get("people", {}).get("neverArchiveSenders", []))
    return addr in senders or domain_of(addr) in domains or is_vip(addr, config)


def select_filter(message: dict[str, Any], config: dict[str, Any]) -> Decision | None:
    sender_type, sender_reasons = classify_sender_type(message, config)
    filters = sorted(config.get("defaultFilters", []) + config.get("customFilters", []), key=lambda f: int(f.get("priority", 0)), reverse=True)
    for filt in filters:
        if not eligible_sender_type(sender_type, filt.get("senderType", "person_or_unknown")):
            continue
        ok, rule_reasons = eval_node(message, filt.get("match", {}))
        if not ok:
            continue
        confidence = score_confidence(rule_reasons, sender_reasons, filt)
        min_conf = float(filt.get("minConfidence", config.get("classification", {}).get("defaultMinConfidence", 0.65)))
        if confidence < min_conf:
            continue
        return Decision(
            filter_id=str(filt.get("id")),
            kind=str(filt.get("kind")),
            confidence=confidence,
            sender_type=sender_type,
            urgent=is_urgent(str(filt.get("id")), message, config),
            reasons=sender_reasons + rule_reasons,
            actions=deepcopy(filt.get("actions", {})),
        )
    if sender_type == "company":
        return Decision(
            filter_id="notifications",
            kind="non_actionable",
            confidence=0.6,
            sender_type=sender_type,
            urgent=False,
            reasons=sender_reasons + ["fallback: unmatched company sender"],
            actions={"addLabels": ["Notification", "CATEGORY_UPDATES"], "removeLabels": ["INBOX"]},
        )
    return None


def load_fixture_messages(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return []
    fixture_path = Path(path).expanduser()
    if not fixture_path.exists() or fixture_path.stat().st_size == 0:
        return []
    payload = load_json(fixture_path)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("messages"), list):
        return payload["messages"]
    return []


def ensure_actions(message: dict[str, Any], decision: Decision, config: dict[str, Any]) -> dict[str, Any]:
    processed_label = config.get("processedLabel", "Auto/Triaged")
    add_labels = canonicalize_labels(list(decision.actions.get("addLabels", [])))
    remove_labels = canonicalize_labels(list(decision.actions.get("removeLabels", [])))
    keep_in_inbox = bool(decision.actions.get("keepInInbox", False))

    if processed_label and processed_label not in add_labels:
        add_labels.append(processed_label)

    if never_archive(message, config):
        remove_labels = [x for x in remove_labels if x != "INBOX"]
        keep_in_inbox = True

    if decision.kind == "non_actionable":
        if "INBOX" not in remove_labels:
            remove_labels.append("INBOX")
        keep_in_inbox = False

    if decision.kind == "actionable" and "INBOX" in remove_labels:
        remove_labels.remove("INBOX")

    return {
        "addLabels": sorted(set(add_labels)),
        "removeLabels": sorted(set(remove_labels)),
        "keepInInbox": keep_in_inbox,
        "notify": bool(decision.actions.get("notify", False)),
    }


def build_notification(message: dict[str, Any], decision: Decision, config: dict[str, Any]) -> dict[str, Any] | None:
    notif = config.get("notifications", {})
    if not notif.get("enabled") or not decision.actions.get("notify", False):
        return None
    route = notif.get("urgentRoute") if decision.urgent else notif.get("defaultRoute")
    if not route:
        return None
    return {
        "route": route,
        "title": f"[{decision.filter_id}] {message.get('subject', '')}",
        "message": {
            "from": message.get("from"),
            "subject": message.get("subject"),
            "filter": decision.filter_id,
            "urgent": decision.urgent,
            "reasons": decision.reasons[:6],
        },
    }


def gog_cmd(account: str, args: list[str]) -> list[str]:
    # Match Secretaria's pattern: explicit --account on every call.
    return ["gog", *args, "--account", account]


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def fetch_messages_with_gog(account: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    search = config.get("search", {})
    processed_label = str(config.get("processedLabel", "Auto/Triaged")).strip()
    query = search.get("query", "in:inbox newer_than:2d")
    if processed_label and 'label:"Auto/Triaged"' not in query and f'label:"{processed_label}"' not in query and '-label:' not in query:
        query = f'{query} -label:"{processed_label}"'
    max_items = int(search.get("max", 100))
    cmd = gog_cmd(account, ["gmail", "messages", "search", query, "--max", str(max_items), "--json"])
    proc = run_cmd(cmd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "gog search failed")
    payload = json.loads(proc.stdout)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("messages"), list):
        return payload["messages"]
    return []


def extract_existing_labels(message: dict[str, Any]) -> set[str]:
    labels = message.get("labels") or message.get("labelIds") or []
    return {canonicalize_label(str(x)) for x in labels}


def ensure_labels_exist(account: str, labels: list[str]) -> list[dict[str, Any]]:
    executed: list[dict[str, Any]] = []
    if not labels:
        return executed
    proc = run_cmd(gog_cmd(account, ['gmail', 'labels', 'list', '--json', '--no-input']))
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'failed to list gmail labels')
    payload = json.loads(proc.stdout)
    existing = set()
    items = payload.get('labels', payload if isinstance(payload, list) else [])
    for item in items:
        name = str(item.get('name', ''))
        if name:
            existing.add(name)
    for label in labels:
        if label in SYSTEM_LABELS or label in existing:
            continue
        cproc = run_cmd(gog_cmd(account, ['gmail', 'labels', 'create', label, '--json', '--no-input']))
        if cproc.returncode == 0:
            executed.append({'op': 'createLabel', 'label': label, 'account': account})
            existing.add(label)
    return executed


def _modify_target(account: str, target_kind: str, target_id: str, add_labels: list[str], remove_labels: list[str]) -> subprocess.CompletedProcess[str]:
    args = ['gmail', target_kind, 'modify', target_id]
    if add_labels:
        args.extend(['--add', ','.join(add_labels)])
    if remove_labels:
        args.extend(['--remove', ','.join(remove_labels)])
    args.extend(['--json', '--no-input'])
    return run_cmd(gog_cmd(account, args))


def apply_actions(account: str, message: dict[str, Any], actions: dict[str, Any], mode: str) -> dict[str, Any]:
    result = {"mode": mode, "executed": []}
    if mode == "dry-run":
        return result
    message_id = str(message.get("id") or "")
    thread_id = str(message.get('threadId') or '')
    if not message_id:
        result["error"] = "missing message id"
        return result

    add_labels = canonicalize_labels(list(actions.get('addLabels', [])))
    remove_labels = canonicalize_labels(list(actions.get('removeLabels', [])))
    result['executed'].extend(ensure_labels_exist(account, add_labels))

    if mode in {"label-only", "full"}:
        proc = None
        used_target = None
        if thread_id:
            proc = _modify_target(account, 'thread', thread_id, add_labels, remove_labels if mode == 'full' else [])
            used_target = ('thread', thread_id)
        else:
            proc = _modify_target(account, 'messages', message_id, add_labels, remove_labels if mode == 'full' else [])
            used_target = ('messages', message_id)
        if proc.returncode != 0 and '404' in ((proc.stderr or '') + (proc.stdout or '')):
            proc = _modify_target(account, 'messages', message_id, add_labels, remove_labels if mode == 'full' else [])
            used_target = ('messages', message_id)
        if proc.returncode != 0:
            result['error'] = proc.stderr.strip() or proc.stdout.strip() or 'failed to modify labels'
            return result
        for label in add_labels:
            result['executed'].append({"op": "addLabel", "label": label, "targetKind": used_target[0], "threadId": thread_id, "messageId": message_id, "account": account})
        if mode == 'full':
            for label in remove_labels:
                result['executed'].append({"op": "removeLabel", "label": label, "targetKind": used_target[0], "threadId": thread_id, "messageId": message_id, "account": account})
    return result


def summarize(plans: list[dict[str, Any]]) -> dict[str, Any]:
    by_filter: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for item in plans:
        by_filter[item["filterId"]] = by_filter.get(item["filterId"], 0) + 1
        src = str(item.get("decisionSource", "heuristic"))
        by_source[src] = by_source.get(src, 0) + 1
    return {"totalPlanned": len(plans), "byFilter": by_filter, "bySource": by_source}


def log_path_for_day(log_dir: Path, stamp: datetime | None = None) -> Path:
    stamp = stamp or now_utc()
    return log_dir / f"{stamp.date().isoformat()}.jsonl"


def llm_review_needed(decision: Decision | None, config: dict[str, Any]) -> bool:
    if not decision:
        return False
    review = config.get('llmReview', {})
    if not review.get('enabled', False):
        return False
    c = float(decision.confidence)
    return float(review.get('minConfidence', 0.68)) <= c <= float(review.get('maxConfidence', 0.86))


def run_ain_review(message: dict[str, Any], heuristic: Decision, config: dict[str, Any]) -> dict[str, Any] | None:
    review = config.get('llmReview', {})
    body = body_text(message)[: int(review.get('maxBodyChars', 2500))]
    allowed = review.get('allowedCategories', [])
    prompt = {
        'from': message.get('from'),
        'subject': message.get('subject'),
        'body_excerpt': body,
        'heuristic_sender_type': heuristic.sender_type,
        'heuristic_category': heuristic.filter_id,
        'heuristic_kind': heuristic.kind,
        'heuristic_confidence': heuristic.confidence,
        'allowed_categories': allowed,
    }
    system = (
        'You are an email classifier. Choose exactly one category from allowed_categories and never invent a new value. '
        'Return JSON only with keys: category, actionable, confidence, archive, star, important, notify, reason. '
        'category must be exactly one string from allowed_categories. '
        'confidence must be a number between 0 and 1. '
        'archive, star, important, notify, actionable must be booleans. '
        'If unsure, choose "none". '
        'Do not output markdown, prose, or extra keys.'
    )
    model_chain = [str(review.get('model', 'amazon-bedrock/moonshotai.kimi-k2.5'))] + [str(x) for x in review.get('fallbackModels', [])]
    provider = str(review.get('provider', '')).strip()
    last_err = None
    for model_id in model_chain:
        cmd = [
            'ain', 'run', json.dumps(prompt, ensure_ascii=False),
            '--jsonl',
            '--schema', str(root_dir() / 'references' / 'ain-email-review.schema.json'),
            '--system', system,
            '--model', model_id,
            '--timeout', str(review.get('timeoutMs', 30000)),
            '--max-tokens', str(review.get('maxTokens', 300)),
            '--temperature', str(review.get('temperature', 0.1)),
        ]
        if provider:
            cmd.extend(['--provider', provider])
        proc = run_cmd(cmd)
        if proc.returncode != 0:
            last_err = proc.stderr.strip() or proc.stdout.strip() or f'ain review failed for {model_id}'
            continue
        raw = proc.stdout.strip()
        if not raw:
            last_err = f'ain returned empty output for {model_id}'
            continue
        data = json.loads(raw)
        if isinstance(data, dict) and 'output' in data and isinstance(data['output'], dict):
            data = data['output']
        if not isinstance(data, dict):
            last_err = f'ain returned non-object JSON for {model_id}'
            continue
        clean = {k: v for k, v in data.items() if k in LLM_ALLOWED_KEYS}
        if clean.get('category') not in allowed:
            last_err = f'ain review returned disallowed category for {model_id}'
            continue
        clean['_model'] = model_id
        return clean
    raise RuntimeError(str(last_err or 'all ain review models failed'))


def decision_from_llm(message: dict[str, Any], heuristic: Decision, llm: dict[str, Any], config: dict[str, Any]) -> Decision:
    category = str(llm.get('category') or heuristic.filter_id)
    if category == 'none':
        return Decision(filter_id='none', kind='none', confidence=float(llm.get('confidence', heuristic.confidence)), sender_type=heuristic.sender_type, urgent=False, reasons=heuristic.reasons + [f"llm: {llm.get('reason','no category')}"], actions={})
    filters = config.get('defaultFilters', []) + config.get('customFilters', [])
    base = next((f for f in filters if str(f.get('id')) == category), None)
    if not base:
        return heuristic
    actions = deepcopy(base.get('actions', {}))
    if bool(llm.get('archive', False)) and 'INBOX' not in actions.get('removeLabels', []):
        actions.setdefault('removeLabels', []).append('INBOX')
    if bool(llm.get('star', False)) and 'STARRED' not in actions.get('addLabels', []):
        actions.setdefault('addLabels', []).append('STARRED')
    if bool(llm.get('important', False)) and 'IMPORTANT' not in actions.get('addLabels', []):
        actions.setdefault('addLabels', []).append('IMPORTANT')
    if bool(llm.get('notify', False)):
        actions['notify'] = True
    if not bool(llm.get('archive', False)) and 'INBOX' in actions.get('removeLabels', []):
        actions['removeLabels'] = [x for x in actions.get('removeLabels', []) if x != 'INBOX']
        actions['keepInInbox'] = True
    return Decision(
        filter_id=category,
        kind=str(base.get('kind', heuristic.kind)),
        confidence=float(llm.get('confidence', heuristic.confidence)),
        sender_type=heuristic.sender_type,
        urgent=is_urgent(category, message, config),
        reasons=heuristic.reasons + [f"llm: {llm.get('reason','reviewed')}"],
        actions=actions,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="")
    parser.add_argument("--messages-json", default="")
    parser.add_argument("--account", action="append", default=[])
    parser.add_argument("--mode", choices=["dry-run", "label-only", "full"], default="")
    args = parser.parse_args()

    config = load_config(args.config or None)
    mode = args.mode or str(config.get("mode", "dry-run"))
    accounts = args.account or config.get("accounts", [])
    fixture_messages = load_fixture_messages(args.messages_json or None)

    log_dir = Path(str(config.get('logging', {}).get('dir', default_logs_dir()))).expanduser()
    ensure_dir(log_dir)
    purged = purge_old_logs(log_dir, int(config.get('logging', {}).get('retentionDays', 30)))
    today_log = log_path_for_day(log_dir)

    all_plans: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for account in accounts:
        try:
            if fixture_messages:
                messages = [m for m in fixture_messages if str(m.get('account', account)) == account]
            else:
                messages = fetch_messages_with_gog(account, config)
            seen_message_ids: set[str] = set()
            for message in messages:
                mid = str(message.get("id") or "")
                if not mid or mid in seen_message_ids:
                    continue
                seen_message_ids.add(mid)
                existing = extract_existing_labels(message)
                processed_label = str(config.get("processedLabel", "Auto/Triaged"))
                if processed_label and processed_label in existing:
                    continue
                decision = select_filter(message, config)
                if not decision:
                    continue
                decision_source = 'heuristic'
                llm_review = None
                if llm_review_needed(decision, config):
                    try:
                        llm_review = run_ain_review(message, decision, config)
                        decision = decision_from_llm(message, decision, llm_review, config)
                        if decision.filter_id == 'none':
                            append_jsonl(today_log, {
                                'timestamp': now_utc().isoformat(),
                                'type': 'decision-skipped',
                                'account': account,
                                'messageId': message.get('id'),
                                'from': message.get('from'),
                                'subject': message.get('subject'),
                                'decisionSource': 'heuristic+llm',
                                'llmReview': llm_review,
                            })
                            continue
                        decision_source = 'heuristic+llm'
                    except Exception as exc:
                        append_jsonl(today_log, {
                            'timestamp': now_utc().isoformat(),
                            'type': 'llm-review-error',
                            'account': account,
                            'messageId': message.get('id'),
                            'error': str(exc),
                        })
                actions = ensure_actions(message, decision, config)
                note = build_notification(message, decision, config)
                execution = apply_actions(account, message, actions, mode)
                plan_row = {
                    "account": account,
                    "messageId": message.get("id"),
                    "from": message.get("from"),
                    "subject": message.get("subject"),
                    "senderType": decision.sender_type,
                    "filterId": decision.filter_id,
                    "kind": decision.kind,
                    "confidence": decision.confidence,
                    "urgent": decision.urgent,
                    "reasons": decision.reasons[:8],
                    "actions": actions,
                    "notification": note,
                    "execution": execution,
                    "decisionSource": decision_source,
                    "llmReview": llm_review,
                }
                all_plans.append(plan_row)
                append_jsonl(today_log, {
                    "timestamp": now_utc().isoformat(),
                    "type": "decision",
                    **plan_row,
                })
        except Exception as exc:
            err_row = {"account": account, "error": str(exc)}
            errors.append(err_row)
            append_jsonl(today_log, {
                "timestamp": now_utc().isoformat(),
                "type": "error",
                **err_row,
            })

    print(json.dumps({
        "mode": mode,
        "accounts": accounts,
        "summary": summarize(all_plans),
        "planned": all_plans,
        "errors": errors,
        "logging": {
            "dir": str(log_dir),
            "file": str(today_log),
            "purged": purged,
        }
    }, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
