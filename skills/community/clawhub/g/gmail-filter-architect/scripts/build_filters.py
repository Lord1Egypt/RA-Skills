#!/usr/bin/env python3
"""Build a complete Gmail filter set from a profile (profiles/*.json).

Usage:
    python3 build_filters.py <profile.json> <out_dir> [--gmailctl]

Outputs:
    batchA.xml      label-only filters. Safe to import with "Also apply filter to matching conversations"
                    checked, so existing mail gets categorised too.
    batchB.xml      star / archive filters. Import WITHOUT applying to existing mail, otherwise old mail
                    gets mass-starred or archived.
    tests.json      every filter's Gmail search query, for checking misfires against real mail before import.
    gmailctl.jsonnet  (with --gmailctl) the same rules as a gmailctl config, for API-based import with diff.

Design rules (see SKILL.md):
    * Every archiving filter carries the same protection group. Gmail has no "move back to inbox" action
      and every matching filter runs, so one archiving filter is enough to hide an important mail.
    * CJK keywords go in subject: only. Gmail matches CJK as substrings, body matching misfires a lot.
    * No "unsubscribe", no is:/label:/in: (they never match incoming mail).
    * One user label per filter; each query stays under ~1,400 characters.
"""
import datetime
import html
import json
import os
import sys

MAX_QUERY = 1400


def grp(prefix, items):
    """from:{a b c}  or  -from:{a b c}"""
    return f"{prefix}{{{' '.join(items)}}}" if items else ""


def subj(items):
    return f"subject:({' OR '.join(items)})" if items else ""


def build_design(p):
    """Return (batch_a, batch_b): lists of dicts with id, desc, label, query and action flags."""
    L = p["labels"]
    protect = " ".join(x for x in (
        "-" + subj(p["protect"]["subjects"]) if p["protect"]["subjects"] else "",
        grp("-from:", p["protect"]["senders"])) if x)
    arch = dict(archive=True, read=True, never_important=True)
    fin_ex = p["fin"].get("exclude_compact") or p["fin"]["txn_senders"]
    A, B = [], []

    b = p["bill"]
    A.append(dict(id="A1-bill", desc="bills, receipts, renewal notices (stay in inbox)", label=L["bill"], never_spam=True,
                  query=f"{{{grp('from:', b['senders'])} {subj(b['subjects'])}}} {grp('-from:', b.get('exclude_senders', []))}"))
    A.append(dict(id="A2-infra", desc="infrastructure notices (stay in inbox)", label=L["infra"], never_spam=True,
                  query=grp("from:", p["infra"]["senders"])))
    A.append(dict(id="A3-apple", desc="Apple / App Store (stay in inbox, important)", label=L["apple"], never_spam=True,
                  important=True, query=grp("from:", p["apple"]["senders"])))
    A.append(dict(id="A4-fin", desc="finance transactional mail (stay in inbox)", label=L["fin"], never_spam=True,
                  query=grp("from:", p["fin"]["txn_senders"])))
    A.append(dict(id="A5-otp", desc="verification codes (stay in inbox)", label=L["otp"], never_spam=True,
                  query=subj(p["otp"]["subjects"])))
    if p.get("biz", {}).get("query"):
        A.append(dict(id="A6-biz", desc="own business", label=L["biz"], never_spam=True,
                      query=f"({p['biz']['query']}) {grp('-from:', p['biz'].get('exclude_senders', []))}"))

    u = p["urgent"]
    ex = grp("-from:", u.get("exclude_senders", []))
    B.append(dict(id="B1-urgent-sec", desc="security / login alerts -> star + important", label=L["urgent"], star=True,
                  important=True, never_spam=True, query=f"{subj(u['security_subjects'])} {ex}"))
    B.append(dict(id="B2-urgent-risk", desc="failed payments, suspension, abuse, review rejections -> star + important",
                  label=L["urgent"], star=True, important=True, never_spam=True, query=f"{subj(u['risk_subjects'])} {ex}"))

    m = p["mkt"]
    if m.get("use_category_promotions"):
        # the Promotions category also catches some finance transactional mail, so exclude finance senders here
        fx = grp("-from:", fin_ex) if m.get("promo_exclude_fin_txn") else ""
        B.append(dict(id="B3-promo", desc="Gmail Promotions category -> archive", label=L["mkt"],
                      query=f"category:promotions {protect} {fx} {grp('-from:', m.get('promo_exclude_senders', []))}", **arch))
    for i, g in enumerate(m.get("brand_sender_groups", []), 1):
        B.append(dict(id=f"B4-brands{i}", desc=f"known marketing senders #{i} -> archive", label=L["mkt"],
                      query=f"{grp('from:', g)} {protect}", **arch))
    if p["fin"].get("mkt_senders"):
        B.append(dict(id="B5-finmkt", desc="marketing addresses of banks / brokers / exchanges -> archive", label=L["mkt"],
                      query=f"{grp('from:', p['fin']['mkt_senders'])} {protect}", **arch))
    soc = " OR ".join(x for x in ("category:social" if m.get("use_category_social") else "",
                                  grp("from:", m.get("social_senders", []))) if x)
    if soc:
        sx = "-" + subj(m["social_exclude_subjects"]) if m.get("social_exclude_subjects") else ""
        B.append(dict(id="B6-social", desc="social notifications (except replies / DMs) -> archive", label=L["social"],
                      query=f"({soc}) {protect} {sx}", **arch))
    if m.get("cold_senders"):
        B.append(dict(id="B7-cold", desc="cold outreach -> archive", label=L["cold"],
                      query=f"{grp('from:', m['cold_senders'])} {protect}", **arch))
    if m.get("kw_subjects"):
        B.append(dict(id="B8-kw", desc="promo words in subject -> archive (subject only)", label=L["mkt"],
                      query=f"{subj(m['kw_subjects'])} {protect} {grp('-from:', fin_ex)}", **arch))
    if p["infra"].get("github_noise"):
        keep = p["infra"].get("github_keep_cc", ["mention", "review_requested", "assign", "security_alert", "author", "comment"])
        B.append(dict(id="B9-github", desc="GitHub notifications not about you -> archive", label=L["infra"],
                      query="from:notifications@github.com -cc:(" + " OR ".join(f"{c}@noreply.github.com" for c in keep)
                            + f") {protect}", **arch))
    # routine infra mail is archived by an explicit subject whitelist; archiving a whole sender would also
    # swallow its login codes, deletion alerts and nameserver warnings
    for i, r in enumerate(p["infra"].get("archive_rules", []), 1):
        B.append(dict(id=f"B10-infra{i}", desc=f"{r['desc']} -> archive", label=L["infra"], query=f"{r['query']} {protect}", **arch))
    for i, r in enumerate(p["fin"].get("archive_rules", []), 1):
        B.append(dict(id=f"B11-fin{i}", desc=f"{r['desc']} -> archive", label=L["fin"], query=r["query"], **arch))
    if p.get("biz", {}).get("archive_query"):
        B.append(dict(id="B12-biz-test", desc="own test mail -> archive", label=L["biz"],
                      query=f"{p['biz']['archive_query']} {protect}", **arch))
    for i, r in enumerate(p.get("extra_rules", []), 1):
        q = r["query"] + (f" {protect}" if r.get("archive") else "")
        target = B if (r.get("archive") or r.get("star")) else A
        target.append(dict(id=f"X{i}", desc=r.get("desc", ""), label=r["label"], query=q,
                           **{k: r[k] for k in r if k not in ("query", "desc", "label")}))

    for f in A + B:
        f["query"] = " ".join(f["query"].split())
        assert len(f["query"]) <= MAX_QUERY, (f["id"], len(f["query"]))
        assert f["query"].count("{") == f["query"].count("}") and f["query"].count("(") == f["query"].count(")"), f["id"]
    return A, B


PROPS = (("archive", "shouldArchive"), ("read", "shouldMarkAsRead"), ("star", "shouldStar"),
         ("important", "shouldAlwaysMarkAsImportant"), ("never_spam", "shouldNeverSpam"),
         ("never_important", "shouldNeverMarkAsImportant"))


def write_xml(filters, path, owner):
    path = os.fspath(path)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = ["<?xml version='1.0' encoding='UTF-8'?><feed xmlns='http://www.w3.org/2005/Atom' "
           "xmlns:apps='http://schemas.google.com/apps/2006'>",
           "<title>Mail Filters</title>", f"<id>tag:mail.google.com,2008:filters:{os.path.basename(path)}</id>",
           f"<updated>{now}</updated>",
           f"<author><name>{html.escape(owner)}</name><email>{html.escape(owner)}</email></author>"]
    for i, f in enumerate(filters, 1):
        out.append(f"<entry><category term='filter'></category><title>Mail Filter</title>"
                   f"<id>tag:mail.google.com,2008:filter:{i:03d}</id><updated>{now}</updated><content></content>")
        out.append(f"<apps:property name='hasTheWord' value='{html.escape(f['query'], quote=True)}'/>")
        if f.get("label"):
            out.append(f"<apps:property name='label' value='{html.escape(f['label'], quote=True)}'/>")
        for key, prop in PROPS:
            if f.get(key):
                out.append(f"<apps:property name='{prop}' value='true'/>")
        out.append("<apps:property name='sizeOperator' value='s_sl'/><apps:property name='sizeUnit' value='s_smb'/></entry>")
    out.append("</feed>")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    import xml.dom.minidom
    xml.dom.minidom.parse(path)


def to_gmailctl(filters, owner):
    """gmailctl (github.com/mbrt/gmailctl) config, v1alpha3. JSON is valid Jsonnet."""
    labels = sorted({f["label"] for f in filters if f.get("label")})
    rules = []
    for f in filters:
        a = {}
        if f.get("archive"):
            a["archive"] = True
        if f.get("read"):
            a["markRead"] = True
        if f.get("star"):
            a["star"] = True
        if f.get("important"):
            a["markImportant"] = True
        if f.get("never_important"):
            a["markImportant"] = False
        if f.get("never_spam"):
            a["markSpam"] = False
        if f.get("label"):
            a["labels"] = [f["label"]]
        rules.append({"filter": {"query": f["query"]}, "actions": a})
    return {"version": "v1alpha3", "author": {"name": owner, "email": owner},
            "labels": [{"name": n} for n in labels], "rules": rules}


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    profile_path, outdir = argv[0], argv[1]
    p = json.load(open(profile_path, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    A, B = build_design(p)
    owner = p.get("owner", "me@example.com")
    write_xml(A, os.path.join(outdir, "batchA.xml"), owner)
    write_xml(B, os.path.join(outdir, "batchB.xml"), owner)
    with open(os.path.join(outdir, "tests.json"), "w", encoding="utf-8") as fh:
        json.dump([dict(id=f["id"], desc=f["desc"], label=f["label"], archive=bool(f.get("archive")),
                        star=bool(f.get("star")), query=f["query"]) for f in A + B], fh, ensure_ascii=False, indent=1)
    if "--gmailctl" in argv:
        with open(os.path.join(outdir, "gmailctl.jsonnet"), "w", encoding="utf-8") as fh:
            json.dump(to_gmailctl(A + B, owner), fh, ensure_ascii=False, indent=2)
    for f in A + B:
        flags = ("star " if f.get("star") else "") + ("archive" if f.get("archive") else "")
        print(f"{f['id']:<18} {len(f['query']):>5}  {f['label']:<12} {flags:<12} {f['desc']}")
    print(f"batch A: {len(A)} label-only (may apply to existing mail) | batch B: {len(B)} star/archive (new mail only) -> {outdir}")


if __name__ == "__main__":
    main(sys.argv[1:])
