"""Render one weekly digest email from a finished discover round.

Inputs in the run's workspace, written by the agent: `digest-picks.yaml`
({roles: [{id, why, gaps}], unread}) and `digest-sources.yaml`
({checked: [site], unchecked: [{site, reason}]}). Titles, companies and links come
from `shortlist.yaml`, never from the agent's own text.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

import journal

MAX_ROLES = 5
SUBJECT_TAG = "[job-hunt weekly]"

TEXT = {
    "zh": {
        "subject": "{tag} {date} — {n} 个新岗位",
        "intro": "本周新的合适岗位（{n} 个）：",
        "empty": "本周没有新的合适岗位。",
        "link": "链接", "why": "为什么适合", "gaps": "差距",
        "checked": "本周查看的来源：{sites}",
        "unchecked": "未能查看：{site}（{reason}），下周会再试。",
        "unread": "另有 {n} 个新岗位没能读到完整招聘页，留到下周。",
        "unread_only": "有 {n} 个新岗位没能读到完整招聘页，留到下周。",
        "questions": "需要你确认：",
        "question": "{id}. 把「{avoid}」加入排除条件吗？{about}这也会影响以后的 discover 搜索。回复「是 {id}」确认。",
        "about": "（来自你对「{role}」的反馈）",
        "reply": ("回复这封邮件即可：「取消推送」停止推送；「暂停 N 周」暂停；"
                  "「第 N 个不相关，因为……」告诉我哪里不合适。"),
        "none": "无", "sep": "：", "place": "（{}）",
    },
    "en": {
        "subject": "{tag} {date} — {n} new role(s)",
        "intro": "New roles that fit this week ({n}):",
        "empty": "No new matching roles this week.",
        "link": "Link", "why": "Why it fits", "gaps": "Gaps",
        "checked": "Sources checked this week: {sites}",
        "unchecked": "Could not check: {site} ({reason}); it will be tried again next week.",
        "unread": "{n} more new role(s) could not be read in full; they wait for next week.",
        "unread_only": "{n} new role could not be read in full; it waits for next week.",
        "questions": "Please confirm:",
        "question": "{id}. Add \"{avoid}\" to your exclusions?{about} This also applies to later discover "
                    "searches. Reply \"yes {id}\" to confirm.",
        "about": " (from your feedback on \"{role}\")",
        "reply": ("Reply to this email: \"unsubscribe\" stops the digest; \"pause N weeks\" pauses it; "
                  "\"#N not relevant because …\" tells me what did not fit."),
        "none": "none", "sep": ": ", "place": " ({})",
    },
}


def role_label(row: dict) -> str:
    return f"{row.get('title', '').strip()} — {row.get('company', '').strip()}"


def load_inputs(workspace) -> tuple[dict, dict, dict]:
    """(picks, sources, shortlist rows by id) from the workspace."""
    workspace = pathlib.Path(workspace)
    picks = journal.load_yaml(workspace / "digest-picks.yaml")
    sources = journal.load_yaml(workspace / "digest-sources.yaml")
    shortlist = journal.load_yaml(workspace / "shortlist.yaml")
    rows = {r.get("id"): r for r in shortlist.get("rows") or [] if isinstance(r, dict)}
    return picks, sources, rows


def inputs_hash(workspace) -> str:
    workspace = pathlib.Path(workspace)
    digest = hashlib.sha256()
    for name in ("digest-picks.yaml", "digest-sources.yaml", "shortlist.yaml"):
        path = workspace / name
        digest.update(path.read_bytes() if path.exists() else b"")
    return digest.hexdigest()


def compose(settings: dict, workspace, today) -> dict:
    """Write digest-email.json and digest-email.txt; return the email."""
    workspace = pathlib.Path(workspace)
    text = TEXT.get(settings.get("language") or "en", TEXT["en"])
    picks, sources, rows = load_inputs(workspace)
    chosen = [(rows[p["id"]], p) for p in picks.get("roles") or [] if p.get("id") in rows]
    lines = [text["intro"].format(n=len(chosen)) if chosen else text["empty"], ""]
    for n, (row, pick) in enumerate(chosen, 1):
        place = text["place"].format(row.get("location")) if row.get("location") else ""
        sep = text["sep"]
        lines += [f"{n}. {role_label(row)}{place}",
                  f"   {text['link']}{sep}{row.get('url', '')}",
                  f"   {text['why']}{sep}{str(pick.get('why', '')).strip()}",
                  f"   {text['gaps']}{sep}{str(pick.get('gaps', '')).strip() or text['none']}", ""]
    unread = int(picks.get("unread") or 0)
    if unread:
        key = "unread" if chosen else "unread_only"
        lines += [text[key].format(n=unread), ""]
    checked = [str(s) for s in sources.get("checked") or []]
    lines.append(text["checked"].format(sites=", ".join(checked) or text["none"]))
    for item in sources.get("unchecked") or []:
        lines.append(text["unchecked"].format(site=item.get("site"), reason=item.get("reason")))
    lines.append("")
    questions = [q for q in settings.get("pending_questions") or [] if int(q.get("asked", 0)) < 2]
    if questions:
        lines.append(text["questions"])
        for q in questions:
            about = text["about"].format(role=q["role"]) if q.get("role") else ""
            lines.append(text["question"].format(id=q["id"], avoid=q["avoid"], about=about))
        lines.append("")
    lines.append(text["reply"])
    body = "\n".join(lines).rstrip() + "\n"
    mail = {"to": [settings.get("recipient")],
            "subject": text["subject"].format(tag=SUBJECT_TAG, date=today.isoformat(), n=len(chosen)),
            "body": body, "role_ids": [row["id"] for row, _ in chosen],
            "role_labels": [role_label(row) for row, _ in chosen],
            "question_ids": [q["id"] for q in questions], "inputs_sha256": inputs_hash(workspace)}
    (workspace / "digest-email.json").write_text(json.dumps(mail, ensure_ascii=False, indent=2) + "\n",
                                                 encoding="utf-8")
    (workspace / "digest-email.txt").write_text(body, encoding="utf-8")
    return mail
