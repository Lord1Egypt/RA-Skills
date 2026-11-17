"""Classify the user's replies to a weekly digest, and apply them.

The script decides, not the agent: a cancel must not depend on how a model reads
a sentence. Quoted text is removed first (the digest's own instructions contain
the cancel words), then keyword rules apply. Any cancel wins over everything else.
"""
from __future__ import annotations

import datetime
import email.utils
import re
import shutil

import digest
import journal
from digest_compose import SUBJECT_TAG
import paths

_QUOTE_START = re.compile(
    r"^(?:.+\bwrote:|.+写道[:：]|.+\bschreef\b.*:|.+\ba écrit\s*:|.+\bschrieb\b.*:|"
    r"-----\s*Original Message\s*-----|From: .+|发件人[:：].+|Van: .+)\s*$", re.I)
# "cancel" alone is a common English word ("Cancel Corp", "don't cancel"), so it counts
# only as a command: at the start of a line, or "cancel it/this/the digest/…".
_CANCEL = re.compile(r"取消推送|取消订阅|退订|停止推送|不要再发|unsubscribe|stop sending|stop these emails|"
                     r"\bafmelden\b|\bopzeggen\b|\buitschrijven\b|"
                     r"^\s*(?:please\s+)?cancel\b|\bcancel\s+(?:it|this|that|these|the\s+(?:digest|emails?|"
                     r"subscription)|my\s+subscription)\b", re.I | re.M)
_NEGATED = re.compile(r"(?:\b(?:don'?t|do\s+not|never|no\s+need\s+to|not)\s+(?:\w+\s+)?|"
                      r"(?:别|不要|不用|请勿|勿|niet|geen)\s*)$", re.I)
_BARE_HEADER = re.compile(r"^(?:wrote|schreef|schrieb|a écrit|写道)\s*[:：]$", re.I)
_CN_NUM = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
_PAUSE_N = re.compile(r"暂停\s*(\d+|[一二两三四五六七八九十])\s*(?:个)?(?:周|星期|礼拜)|"
                      r"pause\s*(?:for\s*)?(\d+)\s*weeks?|pauzeer\s*(\d+)\s*wee?ke?n?|pauze\s*(\d+)\s*wee?ke?n?", re.I)
_PAUSE = re.compile(r"暂停|\bpause\b|\bpauzeer\b|\bpauze\b", re.I)
_YES = re.compile(r"^\s*(?:是的?|好的?|确认|对|yes|ja|y)(?:\s+([A-Za-z]))?\s*[.!。！]?\s*$", re.I)
_FEEDBACK = re.compile(r"第\s*(\d+)\s*个|#\s*(\d+)|\b(?:no\.?|number|nr\.?)\s*(\d+)", re.I)
_BECAUSE = re.compile(r"(?:因为|由于|because|omdat)\s*(.+)$", re.I)
DEFAULT_PAUSE_WEEKS = 4


def _own_lines() -> tuple:
    """The digest's own instruction sentences, whitespace removed: never the user's words."""
    import digest_compose
    return tuple("".join(t["reply"].split()) for t in digest_compose.TEXT.values())


OWN_FRAGMENT_MIN = 8
_BARE_COMMAND = re.compile(r"^(?:please\s+)?(?:unsubscribe|cancel|stop sending|取消推送|取消订阅|退订|停止推送|"
                           r"不要再发了?|afmelden|opzeggen|(?:暂停|pause|pauzeer)(?:\s*\w+\s*(?:周|weeks?|weken?))?)"
                           r"(?:\s+(?:please|thanks?|吧|了))?$", re.I)


def _is_own_text(line: str, own: tuple) -> bool:
    """The line is our instruction sentence, or a wrapped piece of it long enough to be ours."""
    flat = "".join(line.split())
    if not flat:
        return False
    bare = re.sub(r"[\W_]+", " ", line).strip()
    if _BARE_COMMAND.match(bare):
        return False  # "unsubscribe" on its own is the user's command, even though our text contains it
    return any(o in flat or (len(flat) >= OWN_FRAGMENT_MIN and flat in o) for o in own)


def strip_quoted(body: str) -> str:
    kept, own = [], _own_lines()
    for line in str(body or "").splitlines():
        stripped = line.strip()
        # A quote header names a date or an address; "As I wrote:" is the user's own line.
        if _QUOTE_START.match(stripped) and (re.search(r"\d|@", stripped) or stripped.startswith("-----")):
            break
        if _BARE_HEADER.match(stripped):  # a header wrapped onto its own line
            break
        if line.lstrip().startswith(">"):
            continue
        if _is_own_text(line, own):
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def classify(body: str) -> dict:
    text = strip_quoted(body)
    pause = None
    match = _PAUSE_N.search(text)
    if match:
        raw = next(g for g in match.groups() if g)
        pause = int(raw) if raw.isdigit() else _CN_NUM[raw]
    elif _PAUSE.search(text):
        pause = DEFAULT_PAUSE_WEEKS
    first = next((line for line in text.splitlines() if line.strip()), "")
    yes_match = _YES.match(first)
    yes = [(yes_match.group(1) or "*").upper()] if yes_match else []
    feedback = []
    for line in text.splitlines():
        found = _FEEDBACK.search(line)
        if not found:
            continue
        index = int(next(g for g in found.groups() if g))
        because = _BECAUSE.search(line)
        if because:
            reason = because.group(1)
        else:
            reason = line[found.end():]
        reason = reason.strip(" \t,，。.!！:：;；")
        feedback.append({"index": index, "text": line.strip(), "reason": reason})
    cancel = any(not _NEGATED.search(text[:m.start()][-30:]) for m in _CANCEL.finditer(text))
    return {"cancel": cancel, "pause_weeks": pause, "yes": yes,
            "feedback": feedback}


def apply_avoid(name: str, text: str, words: str, today: datetime.date):
    """Add `text` to search-preferences.yaml `avoid`, after a dated backup."""
    import yaml
    path = paths.search_prefs(name)
    if not path.exists():
        raise ValueError(f"{path} does not exist; run discover's preference questions first")
    prefs = journal.load_yaml(path)
    avoid = prefs.get("avoid") or []
    if not isinstance(avoid, list):
        raise ValueError(f"`avoid` in {path} is not a list; change it by hand")
    backup = path.with_name(f"{path.name}.bak-{today.isoformat()}")
    n = 1
    while backup.exists():
        n += 1
        backup = path.with_name(f"{path.name}.bak-{today.isoformat()}-{n}")
    shutil.copy2(path, backup)
    if text not in avoid:
        avoid.append(text)
    prefs["avoid"], prefs["updated"] = avoid, today.isoformat()
    path.write_text(yaml.safe_dump(prefs, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def _next_id(questions: list) -> str:
    used = {q.get("id") for q in questions}
    return next(chr(c) for c in range(ord("A"), ord("Z") + 1) if chr(c) not in used)


def apply_messages(name: str, messages: list, today: datetime.date, run=None) -> dict:
    """Apply replies from the recipient in digest threads. Returns the run's next action."""
    settings = digest.load_settings(name)
    recipient = str(settings.get("recipient") or "").strip().casefold()
    threads = set(settings.get("threads") or [])
    processed = list(settings.get("processed_messages") or [])
    questions = [q for q in settings.get("pending_questions") or [] if int(q.get("asked", 0)) < 2]
    sent_digests = settings.get("sent_digests") or {}
    sent_subjects = settings.get("sent_subjects") or {}
    applied, ignored = [], []
    cancel_words = pause = None
    for message in messages or []:
        mid = str(message.get("id") or "")
        sender = email.utils.parseaddr(str(message.get("from") or ""))[1].casefold()
        if mid and mid in processed:
            ignored.append({"id": mid, "reason": "already applied"})
            continue
        if not recipient or sender != recipient:
            ignored.append({"id": mid, "reason": f"sender {sender or '?'} is not the recipient"})
            continue
        subject = str(message.get("subject") or "")
        if message.get("thread_id") not in threads and SUBJECT_TAG not in subject:
            ignored.append({"id": mid, "reason": "not a reply to a digest"})
            continue
        if mid:
            processed.append(mid)
        found = classify(message.get("body"))
        words = strip_quoted(message.get("body"))[:500]
        if found["cancel"]:
            cancel_words = words
            applied.append({"id": mid, "effect": "cancel"})
            continue
        if found["pause_weeks"]:
            pause = (found["pause_weeks"], words)
            applied.append({"id": mid, "effect": f"pause {found['pause_weeks']} weeks"})
        for item in found["feedback"]:
            roles = sent_digests.get(message.get("thread_id")) or next(
                (labels for subj, labels in sent_subjects.items() if subj and subj in subject), [])
            role = roles[item["index"] - 1] if 0 < item["index"] <= len(roles) else None
            if not item["reason"]:
                ignored.append({"id": mid, "reason": f"feedback on #{item['index']} gives no reason"})
                continue
            questions.append({"id": _next_id(questions), "avoid": item["reason"], "role": role,
                              "words": item["text"], "date": today.isoformat(), "asked": 0})
            applied.append({"id": mid, "effect": f"question about #{item['index']}"})
        for target in found["yes"]:
            open_qs = list(questions)
            if target == "*":
                chosen = open_qs if len(open_qs) == 1 else []
                if len(open_qs) > 1:
                    ignored.append({"id": mid, "reason": "yes, but which question? reply 是 A / yes A"})
            else:
                chosen = [q for q in open_qs if q["id"] == target]
            for q in chosen:
                apply_avoid(name, q["avoid"], words, today)
                questions.remove(q)
                applied.append({"id": mid, "effect": f"avoid {q['avoid']!r}"})
    settings = digest.load_settings(name)
    settings["processed_messages"] = processed[-200:]
    settings["pending_questions"] = questions
    digest.save_settings(name, settings)
    if cancel_words is not None:
        digest.cancel(name, cancel_words, today)
        if run is not None:
            digest.uninstall(name, run=run)
        else:
            digest.uninstall(name)
        return {"action": "cancel", "applied": applied, "ignored": ignored}
    if pause:
        digest.pause(name, pause[0], pause[1], today)
        return {"action": "pause", "applied": applied, "ignored": ignored}
    return {"action": "continue", "applied": applied, "ignored": ignored}
