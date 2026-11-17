#!/usr/bin/env python3
"""Self-check for the LYGO TV package: identity, isolation, and the ClawHub audit's findings as rules.

Every check returns a named boolean, so a failure says which rule broke instead of just "ok": false.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import lygo_tv as t  # noqa: E402

SHIPPED_TEXT = [
    "SKILL.md", "README.md", "claw.json", "skill-card.md", "examples/quickstart.md",
    "embed/README.md", "embed/lygo-tv-embed.html", "references/SECURITY.md",
]


def main() -> int:
    src = (HERE / "lygo_tv.py").read_text(encoding="utf-8")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    fleet = {rel: (ROOT / rel).read_text(encoding="utf-8", errors="replace")
             for rel in SHIPPED_TEXT if (ROOT / rel).is_file()}
    embed_js = (ROOT / "embed" / "lygo-tv-ninja.js").read_text(encoding="utf-8", errors="replace")
    embed_html = fleet.get("embed/lygo-tv-embed.html", "")
    m = t.map_payload()
    u = t.urls()
    embed = t.embed()

    # The declared version is the one in SKILL.md; the script and the signature follow it, so a release needs
    # the version written once. Hardcoding it here meant editing three files and forgetting one still passed.
    found = re.search(r"(?m)^version:\s*([0-9][0-9.]*)\s*$", skill)
    declared = found.group(1) if found else ""

    # The vendored player is a copy of the site's file; its hash is published in embed/README.md, so
    # re-vendoring without updating the hash is caught here rather than by whoever pastes it.
    hashes_ok = True
    for name in ("lygo-tv-ninja.js", "lygo-tv-ninja.css"):
        f = ROOT / "embed" / name
        got = "sha256-" + base64.b64encode(hashlib.sha256(f.read_bytes()).digest()).decode()
        if got not in fleet.get("embed/README.md", ""):
            hashes_ok = False

    checks = {
        "scripts: no subprocess": not re.search(r"(?m)^\s*import\s+subprocess\b", src),
        "scripts: no network imports": not any(k in src for k in ("urllib", "requests", "http.client")),
        "identity: version declared": bool(declared),
        "identity: script matches SKILL.md": t.VERSION == declared,
        "identity: signature matches": t.SIG == "Delta9Phi963-LYGO-TV-v" + declared,
        "identity: player urls": (u["player"] == "https://chatagent.ca/sources/"
                                  and u["catalog"].endswith("/sources/catalog.json")
                                  and u["terms"].endswith("/terms.html")
                                  and u["disclaimer"].endswith("/disclaimer.html")
                                  and u["emblem"].endswith("/emblem.svg")),
        "identity: emblem file": (ROOT / "emblem.svg").is_file(),
        "contract: catalog is RESOURCE": m["class"] == "RESOURCE" and m["live_star_chart_ingest"] is False,
        "contract: forbidden list intact": "CORS or pirate proxy" in m["forbidden"],
        "contract: plain starts with the name": t.plain().startswith("LYGO TV"),
        "embed: urls are canonical": (u["player_js"].endswith("/assets/lygo-tv-ninja.js")
                                      and u["player_css"].endswith("/assets/lygo-tv-ninja.css")),
        "embed: snippet + files": ("<div data-lygo-tv></div>" in embed and "data-lygo-tv" in skill
                                   and (ROOT / "embed" / "lygo-tv-ninja.js").is_file()
                                   and (ROOT / "embed" / "lygo-tv-ninja.css").is_file()
                                   and (ROOT / "embed" / "lygo-tv-embed.html").is_file()),
        "embed: vendored hashes published": hashes_ok,
        # --- the ClawHub audit's findings, kept from coming back -------------------------------------
        "audit RP1: nothing installs a floating version": all("clawhub@latest" not in v for v in fleet.values())
                                                          and "clawhub@latest" not in src,
        "audit SDI-1: cdn dependency pinned (SRI)": "HLS_SRI" in embed_js and "integrity" in embed_js
                                                    and "sha384-" in embed_js,
        "audit T09: catalog urls validated": "urlAllowed" in embed_js and "EMBED_HOSTS" in embed_js,
        "audit SDI-4: player comment matches the terms flow": "Terms tick" in embed_js,
        "audit P2: no comments in the embed page": "<!--" not in embed_html,
        "audit SQP-2: the page discloses what it loads": "What this player loads" in embed_html,
        "audit TP4: the embed boundary is declared, scripts split from embed": (
            "runs_in" in skill and "permissions:" in skill and "embed:" in skill and "scripts:" in skill),
        "audit LP3: tool scope declared": "allowed-tools" in skill,
        "audit SQP-1: the trigger has exclusions": "When not to use" in skill,
    }
    ok = all(checks.values())
    print(json.dumps({
        "ok": ok,
        "declared_in_skill_md": declared,
        "script_version": t.VERSION,
        "signature": t.SIG,
        "failed": [k for k, v in checks.items() if not v],
        "checks": checks,
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
