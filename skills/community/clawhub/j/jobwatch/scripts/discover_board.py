#!/usr/bin/env python3
"""信源探测器：给一个公司名/slug 猜测，探测它用的是哪家 ATS、board slug 是什么。

用法: python3 scripts/discover_board.py anthropic
      python3 scripts/discover_board.py "Google DeepMind" deepmind google-deepmind

对每个候选 slug 依次探测 Greenhouse / Ashby / Lever 的公开 API，
输出可直接粘进 config.json sources 的 JSON 片段。

SCOPE / OUTBOUND (accurate as of v1.2.0): this script is **not** an autonomous
crawler. It runs once per company that the user named out loud during the
onboarding interview, and never on its own schedule — the cron pipeline reads
`config.json` sources only and never calls this file. What leaves the machine is
one HTTP GET per (candidate slug × ATS), carrying only the guessed slug — a
lowercase squashing of the company name the user just typed. No profile data, no
credentials, and no user identifier are sent. Because the payload is a public
company slug rather than user data, these probes are not routed through
`require_egress_consent()`; instead every destination is printed to stderr before
it is contacted, so the probe is never silent. See SKILL.md "Privacy & Data Flow".
"""
import json
import re
import sys

from common import http_json

PROBES = [
    ("greenhouse", "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs",
     lambda d: len(d.get("jobs", []))),
    ("ashby", "https://api.ashbyhq.com/posting-api/job-board/{slug}",
     lambda d: len(d.get("jobs", []))),
    ("lever", "https://api.lever.co/v0/postings/{slug}?mode=json",
     lambda d: len(d) if isinstance(d, list) else 0),
]


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def _announce(candidates):
    """Print every outbound destination before any of them is contacted.

    Discovery is the one place where the skill contacts a host that the user did
    not name in config.json, so the full probe list is disclosed up front rather
    than after the fact.
    """
    hosts = sorted({url_tpl.split("/")[2] for _, url_tpl, _ in PROBES})
    print(
        f"[jobwatch] source discovery: about to send {len(candidates)} guessed "
        f"company slug(s) {candidates} to the public ATS APIs at "
        f"{', '.join(hosts)}. Only the slug is sent — no profile data, no keys.",
        file=sys.stderr,
    )


def discover(candidates):
    hits = []
    _announce(candidates)
    for slug in candidates:
        for kind, url_tpl, count_fn in PROBES:
            try:
                data = http_json(url_tpl.format(slug=slug), timeout=20)
                n = count_fn(data)
                if n > 0:
                    hits.append({"kind": kind, "board": slug, "jobs": n})
            except Exception:  # noqa: BLE001
                continue
    return hits


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: discover_board.py <company name> [extra slug guesses...]")
    name = sys.argv[1]
    cands = list(dict.fromkeys([slugify(name)] + [slugify(s) for s in sys.argv[2:]]))
    hits = discover(cands)
    if not hits:
        print(f"# 未探测到 {name} 的 Greenhouse/Ashby/Lever board。")
        print("# 试试公司 careers 页 URL 里的 slug，或改用 RSS 信源（kind: rss）。")
    else:
        best = max(hits, key=lambda h: h["jobs"])
        print(f"# {name}: 探测到 {len(hits)} 个候选，推荐（岗位数最多）：")
        print(json.dumps({"id": best["board"], "kind": best["kind"],
                          "board": best["board"], "company": name},
                         ensure_ascii=False, indent=2))
        print(f"# 全部命中: {hits}")
