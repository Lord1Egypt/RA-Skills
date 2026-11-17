#!/usr/bin/env python3
"""Rendering for Prove It Works (markdown and JSON). Secrets are already redacted upstream."""

from common import no_em_dash

CAUSE_LABEL = {
    1: "tests fail", 2: "build fails", 3: "type check fails", 4: "lint fails",
    5: "tests did not really run", 6: "tests weakened", 7: "outside the task's scope",
    8: "project rule broken", 9: "debug leftover", 10: "secret or env file", 11: "dependency or lockfile change",
    12: "existing migration edited", 13: "stub or placeholder", 14: "type or lint escape",
    15: "task item missing", 16: "exported API changed", 17: "large or generated file",
}
KIND_NAME = {"test": "tests", "build": "build", "typecheck": "typecheck", "lint": "lint", "rule": "rule"}


def _cell(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def _result(c):
    st = c["status"]
    cnt = c.get("counts") or {}
    bits = []
    if c.get("masked"):
        bits.append("exit code masked")
    if c.get("preexisting"):
        bits.append("errors only on lines the change did not touch")
    if c["kind"] == "test" and cnt.get("real_total") is not None and st in ("PASS", "FAIL"):
        if cnt.get("failed"):
            bits.append("%d of %d failed" % (cnt["failed"], cnt["real_total"]))
        else:
            bits.append("%d tests" % cnt["real_total"])
        if cnt.get("skipped_n"):
            bits.append("%d skipped" % cnt["skipped_n"])
    return st + (" (%s)" % ", ".join(bits) if bits else "")


def render_finding(f, n):
    L = ["### %s%s" % (("%d. " % n) if n else "", f["title"])]
    L.append("- **Finding:** %s" % f["finding"])
    ev = f["evidence"]
    if len(ev) <= 1:
        L.append("- **Evidence:** %s" % (ev[0] if ev else "(none)"))
    else:
        L.append("- **Evidence:**")
        for e in ev[:8]:
            L.append("  - `%s`" % e.replace("`", "'") if e.startswith("> ") else "  - %s" % e)
    L.append("- **Impact:** %s" % f["impact"])
    if len(f["fix"]) == 1:
        L.append("- **Fix:** %s" % f["fix"][0])
    else:
        L.append("- **Fix:**")
        for k, x in enumerate(f["fix"], 1):
            L.append("  %d. %s" % (k, x))
    L.append("- Cause%s: %s." % ("" if len(f["causes"]) == 1 else "s", ", ".join("%d (%s)" % (c, CAUSE_LABEL.get(c, "?")) for c in f["causes"])))
    L.append("")
    return "\n".join(L)


MAX_FULL = 25
MAX_REPORT = 40000


def render_md(res):
    L = [res["verdict"], ""]
    ch = res["change"]
    nfiles = len(ch["files"])
    t = res["timings"]
    L.append("Change: %s (%d file%s). Task: %s. Took %.1fs (checks %.1fs)." % (
        ch["how"], nfiles, "" if nfiles == 1 else "s", res.get("task_source") or "not given", t["total_s"], t["checks_s"]))
    L.append("")
    cov = res.get("coverage") or {}
    if cov.get("notes") and res["status"] != "PROVEN":
        L.append("**Not covered:** " + "; ".join(cov["notes"][:6]) + ".")
        L.append("")
    checks = res["checks"]
    L.append("## Checks (%d)" % len(checks))
    L.append("")
    if checks:
        L.append("| # | Check | Command | Result | Exit | Time |")
        L.append("|---|---|---|---|---|---|")
        for i, c in enumerate(checks, 1):
            name = KIND_NAME.get(c["kind"], c["kind"])
            if c.get("where") and c["where"] != ".":
                name += " (%s)" % c["where"]
            res_txt = _result(c)
            if c["status"] == "NOT RUN" and c.get("reason"):
                res_txt += ": " + c["reason"]
            if c.get("required_by"):
                res_txt += " [required by %s]" % ", ".join(c["required_by"])
            L.append("| %d | %s | `%s` | %s | %s | %s |" % (
                i, _cell(name), _cell(c["display"]), _cell(res_txt),
                "-" if c["exit"] is None else c["exit"], "-" if c["exit"] is None else "%.1fs" % c["seconds"]))
        L.append("")
        for c in checks:
            if c["status"] == "NOT RUN" or not c["tail"]:
                continue
            n = 20 if c["status"] in ("FAIL", "TIMEOUT", "NO TESTS") and not c.get("preexisting") else 4
            if c.get("excerpt"):
                L.append("**Failures: %s `%s`**" % (KIND_NAME.get(c["kind"], c["kind"]), c["display"]))
                L.append("```")
                L += [l[:300] for l in c["excerpt"]]
                L.append("```")
                n = 10
            L.append("**Output: %s `%s`** (last %d lines)" % (KIND_NAME.get(c["kind"], c["kind"]), c["display"], min(n, len(c["tail"]))))
            L.append("```")
            L += [l[:300] for l in c["tail"][-n:]]
            L.append("```")
            L.append("")
    else:
        L.append("No test, build, typecheck or lint command was found.")
        L.append("")
    fs = res["findings"]
    failing = [f for f in fs if f["key"].startswith("check:") and not f["key"].startswith("check:notests")]
    probs = [f for f in fs if f not in failing]
    i = 0
    if failing:
        L.append("## Failing checks (%d)" % len(failing))
        L.append("")
        for f in failing:
            i += 1
            L.append(render_finding(f, i))
    if probs:
        L.append("## Problems in the change (%d)" % len(probs))
        L.append("")
        shown, per_group, rest = 0, {}, []
        for f in probs:
            g = f.get("group")
            per_group[g] = per_group.get(g, 0) + 1
            if shown >= MAX_FULL or (f.get("group_count", 1) > 5 and per_group[g] > 3):
                rest.append(f)
                continue
            i += 1
            shown += 1
            L.append(render_finding(f, i))
        if rest:
            L.append("**And %d more problem%s of the kinds above** (full list: --json):" % (len(rest), "" if len(rest) == 1 else "s"))
            for f in rest[:40]:
                L.append("- %s (cause %s)" % (f["title"], "/".join(str(c) for c in f["causes"])))
            if len(rest) > 40:
                L.append("- ... %d more" % (len(rest) - 40))
            L.append("")
    chk = res["check_these"]
    if chk:
        L.append("## Check these (Claude: open each one and decide) (%d)" % len(chk))
        L.append("")
        for f in chk[:30]:
            L.append("- **%s.** %s Evidence: %s. Cause %s." % (
                f["title"], f["finding"], "; ".join(f["evidence"][:2]), "/".join(str(c) for c in f["causes"])))
        if len(chk) > 30:
            L.append("- and %d more (full list: --json)" % (len(chk) - 30))
        L.append("")
    rl = res["rules"]
    if rl["files"]:
        L.append("## Project rules (%s)" % ", ".join(rl["files"]))
        L.append("")
        if rl["checked"]:
            L.append("Checked automatically (%d): %s." % (len(rl["checked"]), "; ".join(
                "%s %s" % (r["source"], _rule_short(r)) for r in rl["checked"][:12])))
            L.append("")
        if rl["read"]:
            L.append("Rules Claude must check by reading (%d):" % len(rl["read"]))
            for r in rl["read"][:25]:
                txt = r["text"] if len(r["text"]) <= 170 else r["text"][:167] + "..."
                L.append("- %s: %s" % (r["source"], txt))
            if len(rl["read"]) > 25:
                L.append("- and %d more (run rules.py)" % (len(rl["read"]) - 25))
            L.append("")
    if res["notes"]:
        L.append("## Notes")
        L.append("")
        for n in res["notes"]:
            L.append("- %s" % n)
        L.append("")
    L.append("## What this can't see")
    L.append("")
    for c in res["cant_see"]:
        L.append("- %s" % c)
    L.append("")
    st = res["status"]
    if st == "PROVEN":
        L.append("Before you say done: quote the first line and the checks table, then do the review pass "
                 "(references/review-checklist.md) for what the scripts can't judge.")
    elif st == "CHECKS PASS":
        L.append("Before you say done: quote the first line, including what it says was not covered. The checks pass, but the proof "
                 "is incomplete; do the review pass and say plainly what is unverified.")
    elif st == "NOT VERIFIED":
        L.append("Before you say done: you can't claim it works. Quote the first line, tell the person which checks could not run "
                 "and the exact command that would let them run (install, tool), and ask once. Never call a NOT RUN check passed.")
    else:
        L.append("Before you say done: you can't. Say \"not done yet\" with the first line above, fix each failing check "
                 "and problem, then run the proof again. Never call a NOT RUN check passed.")
    L.append("")
    text = "\n".join(L)
    if len(text) > MAX_REPORT:
        res.setdefault("coverage", {})["truncated"] = True
        text = text[:MAX_REPORT].rsplit("\n", 1)[0] + "\n\n(report cut at %d characters; run with --json for everything)\n" % MAX_REPORT
    return no_em_dash(text)


def _rule_short(r):
    k = r["kind"]
    if k == "pm":
        return "use %s" % (r.get("pm") or "not " + "/".join(r.get("forbid") or []))
    if k == "forbid-path":
        return "do not edit %s" % r["pattern"]
    if k == "forbid-import":
        return "no import of %s" % r["pattern"]
    if k == "grep":
        return "no %s" % (r.get("literal") or r["pattern"])
    if k == "require-cmd":
        return "run %s" % r["pattern"]
    if k == "naming":
        return "%s file names" % r["style"]
    return k


def to_json(res):
    checks = []
    for c in res["checks"]:
        checks.append({k: c.get(k) for k in ("kind", "display", "source", "where", "status", "reason", "exit",
                                              "seconds", "counts", "failed_tests", "required_by", "excerpt", "tail",
                                              "inferred", "masked", "preexisting")})
    out = dict(res)
    out["checks"] = checks
    out["verdict"] = no_em_dash(res["verdict"])
    return out
