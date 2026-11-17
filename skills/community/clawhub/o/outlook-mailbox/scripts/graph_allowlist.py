#!/usr/bin/env python3
"""Fail-closed gate for Microsoft Graph mail calls made by an agent's scripts.

Usage:
  python3 graph_allowlist.py --policy policy.json [--cycle cycle.json] METHOD URL
Exit codes: 0 = allowed, 2 = denied, 3 = unusable input (also a denial).
Anything not explicitly allowed below is denied. Stdlib only.
Every read of message data needs a $select inside policy.select, except:
  - delta continuation links (they cannot carry $select): allowed only if the
    stored origin is an initial delta request that passes this gate today;
  - attachment metadata: $select limited to ATTACHMENT_META;
  - attachment bytes ($value): only with allow_attachment_content: true.
POST createReply / PATCH return the full draft: callers keep its id only.
"""
import json
import re
import sys
from urllib.parse import urlsplit, parse_qsl

ALLOW, DENY, BAD = 0, 2, 3
BASE = ("https", "graph.microsoft.com", "/v1.0/")
ATTACHMENT_META = {"id", "name", "contentType", "size", "isInline", "lastModifiedDateTime"}
ID_RE = re.compile(r"^[A-Za-z0-9_=-]{8,1024}$")
SEG_RE = re.compile(r"^([A-Za-z.]+)(?:\('([^'()]*)'\)|\(\))?$")
SMTP_RE = re.compile(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$")
GUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


class Bad(Exception):
    pass


def _str_list(obj, key, required):
    val = obj.get(key)
    if val is None and not required:
        return []
    if not isinstance(val, list) or (required and not val) or not all(isinstance(v, str) and v.strip() for v in val):
        raise Bad(f"{key}: must be a non-empty list of non-empty strings" if required else f"{key}: must be a list of strings")
    return [v.strip() for v in val]


def load_policy(raw):
    if not isinstance(raw, dict):
        raise Bad("policy: must be a JSON object")
    boxes = {m.lower() for m in _str_list(raw, "mailboxes", True)}
    for m in boxes:
        if not (SMTP_RE.match(m) or GUID_RE.match(m)):
            raise Bad(f"policy.mailboxes: not an SMTP address or object id: {m!r}")
    folders = {f.lower() for f in _str_list(raw, "folders", True)}
    select = set(_str_list(raw, "select", True))
    content = raw.get("allow_attachment_content", False)
    if not isinstance(content, bool):
        raise Bad("policy.allow_attachment_content: must be true or false")
    return {"mailboxes": boxes, "folders": folders, "select": select, "content": content}


def load_cycle(raw):
    if raw is None:
        return {"drafts": {}, "links": {}}
    if not isinstance(raw, dict):
        raise Bad("cycle: must be a JSON object")
    drafts = raw.get("draft_ids", {})
    if not isinstance(drafts, dict):
        raise Bad("cycle.draft_ids: must be an object {mailbox: [ids]}")
    out = {}
    for box, ids in drafts.items():
        if not isinstance(box, str) or not isinstance(ids, list) or not all(isinstance(i, str) and ID_RE.match(i) for i in ids):
            raise Bad("cycle.draft_ids: each value must be a list of message ids")
        out[box.strip().lower()] = set(ids)
    links = raw.get("issued_links", [])
    if not isinstance(links, list):
        raise Bad("cycle.issued_links: must be a list")
    issued = {}
    for item in links:
        if (not isinstance(item, dict) or set(item) != {"link", "origin"}
                or not all(isinstance(item[k], str) and item[k].strip() for k in ("link", "origin"))):
            raise Bad('cycle.issued_links: each entry must be {"link": <Graph-issued URL>, "origin": <initial delta URL>}')
        issued[item["link"]] = item["origin"]
    return {"drafts": out, "links": issued}


def parse_path(path):
    """"users/x/mailFolders('inbox')/messages/microsoft.graph.delta()" -> ['users','x','mailFolders','inbox','messages','delta']"""
    if "%" in path.replace("%40", ""):
        raise PermissionError("percent-encoding other than %40 in path")
    path = path.replace("%40", "@")
    if "\\" in path or "//" in path or any(ord(c) < 33 or ord(c) == 127 for c in path):
        raise PermissionError("malformed path")
    out = []
    for seg in path.split("/"):
        if seg in ("", ".", ".."):
            raise PermissionError("empty or dot segment")
        m = SEG_RE.match(seg)
        if m:
            name = m.group(1)
            if name.lower().startswith("microsoft.graph."):
                name = name[len("microsoft.graph."):]
            out.append(name)
            if m.group(2) is not None:
                if not m.group(2):
                    raise PermissionError("empty key")
                out.append(m.group(2))
        elif "(" in seg or ")" in seg or "'" in seg:
            raise PermissionError("unexpected key syntax")
        else:
            out.append(seg)
    return out


def check(method, url, policy, cycle):
    method = method.upper()
    if not isinstance(url, str) or len(url) > 8192:
        return DENY, "url missing or too long"
    sp = urlsplit(url)
    if (sp.scheme, sp.netloc.lower()) != BASE[:2] or sp.fragment or not sp.path.startswith(BASE[2]):
        return DENY, "only https://graph.microsoft.com/v1.0/ is allowed"
    try:
        segs = parse_path(sp.path[len(BASE[2]):])
    except PermissionError as exc:
        return DENY, str(exc)
    query = parse_qsl(sp.query, keep_blank_values=True, strict_parsing=False) if sp.query else []
    keys = [k for k, _ in query]
    if len(keys) != len(set(keys)):
        return DENY, "duplicate query parameter"
    q = dict(query)
    if len(segs) < 3 or segs[0].lower() != "users":
        return DENY, "only /users/{mailbox}/... is allowed"
    box = segs[1].lower()
    if box not in policy["mailboxes"]:
        return DENY, "mailbox not in allowlist"
    rest = segs[2:]
    low = [s.lower() for s in rest]

    def select_ok(allowed):
        if "$select" not in q:
            return False
        fields = [f.strip() for f in q["$select"].split(",")]
        return all(fields) and all(f in allowed for f in fields)

    # delta: GET /users/{b}/mailFolders/{f}/messages/delta
    if len(rest) == 4 and low[0] == "mailfolders" and low[2] == "messages" and low[3] == "delta":
        if method != "GET":
            return DENY, "delta is GET only"
        tokens = {"$deltatoken", "$skiptoken"} & set(q)
        if tokens:
            if set(q) != tokens or len(tokens) != 1:
                return DENY, "continuation link must carry its token and nothing else"
            origin = cycle["links"].get(url)
            # A deltaLink/nextLink cannot carry $select: it inherits the fields of the initial
            # request that started the chain. Re-check that origin against the CURRENT policy,
            # so a link born from a wider $select (or an older, wider policy) is refused.
            # An unknown link has no origin: check(None) denies (url must be a string).
            if check("GET", origin, policy, {"drafts": {}, "links": {}}) != (ALLOW, "delta initial"):
                return DENY, "continuation link not issued by Graph from a compliant initial delta"
            return ALLOW, "delta continuation"
        if low[1] not in policy["folders"]:
            return DENY, "folder not in allowlist"
        if set(q) - {"$select", "changeType"} or not select_ok(policy["select"]):
            return DENY, "initial delta needs $select within policy, only changeType besides"
        return ALLOW, "delta initial"
    if len(rest) >= 2 and low[0] == "messages" and ID_RE.match(rest[1]):
        mid, tail = rest[1], [t.lower() for t in rest[2:]]
        if not tail:
            if method == "GET":
                if set(q) != {"$select"} or not select_ok(policy["select"]):
                    return DENY, "message read needs $select within policy, nothing else"
                return ALLOW, "message read"
            if method == "PATCH":
                if q:
                    return DENY, "PATCH takes no query"
                if mid not in cycle["drafts"].get(box, set()):
                    return DENY, "PATCH only on a draft id returned by createReply this cycle and re-read isDraft:true"
                return ALLOW, "draft patch"
            return DENY, f"{method} on a message is never allowed"
        if tail == ["createreply"] and method == "POST" and not q:
            return ALLOW, "createReply"
        if tail == ["attachments"] and method == "GET":
            if set(q) != {"$select"} or not select_ok(ATTACHMENT_META):
                return DENY, "attachment list needs $select of metadata fields only"
            return ALLOW, "attachment metadata"
        if len(tail) == 3 and tail[0] == "attachments" and ID_RE.match(rest[3]) and tail[2] == "$value":
            if method == "GET" and not q and policy["content"]:
                return ALLOW, "attachment content"
            return DENY, "attachment content disabled by policy"
    return DENY, "call not in the closed list"


def main(argv):
    args, policy_path, cycle_path = [], None, None
    it = iter(argv)
    for a in it:
        if a == "--policy":
            policy_path = next(it, None)
        elif a == "--cycle":
            cycle_path = next(it, None)
        else:
            args.append(a)
    if not policy_path or len(args) != 2:
        print("usage: graph_allowlist.py --policy P [--cycle C] METHOD URL", file=sys.stderr)
        return BAD
    try:
        with open(policy_path, encoding="utf-8") as fh:
            policy = load_policy(json.load(fh))
        cycle_raw = None
        if cycle_path:
            with open(cycle_path, encoding="utf-8") as fh:
                cycle_raw = json.load(fh)
        cycle = load_cycle(cycle_raw)
    except (OSError, ValueError, Bad) as exc:
        print(f"DENY unusable input: {exc}", file=sys.stderr)
        return BAD
    code, reason = check(args[0], args[1], policy, cycle)
    print(("ALLOW " if code == ALLOW else "DENY ") + reason, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
