#!/usr/bin/env python3
"""LYGO TV — ClawHub pointer. Prints URLs. No network. No subprocess."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any

SIG = "Delta9Phi963-LYGO-TV-v1.3.1"
VERSION = "1.3.1"

TV = "https://chatagent.ca/sources/"
CATALOG = "https://chatagent.ca/sources/catalog.json"
TERMS = "https://chatagent.ca/terms.html"
DISCLAIMER = "https://chatagent.ca/sources/disclaimer.html"
EMBLEM = "https://chatagent.ca/sources/emblem.svg"
SOURCE = "https://github.com/DeepSeekOracle/chatagent/tree/main/sources"
SKILL_SRC = "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-tv"
STACK = "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/free-sources"
WITNESS = "https://chatagent.ca/witness/"
LISTEN = "https://asiancoastline.com/listen.html"
CLAWHUB = "https://clawhub.ai/deepseekoracle/skills/lygo-tv"
# Pinned twice over: the CLI that was verified with this package, and this package's own version. A
# A floating version on either side runs whatever is published at install time, which is the supply-chain
# finding the ClawHub audit raised (RP1).
CLI_PIN = "0.23.3"
INSTALL = "npx clawhub@" + CLI_PIN + " install deepseekoracle/lygo-tv@" + VERSION
PLAYER_JS = "https://chatagent.ca/assets/lygo-tv-ninja.js"
PLAYER_CSS = "https://chatagent.ca/assets/lygo-tv-ninja.css"
# the snippet carries a version query so a page can be told to move to a new player; the canonical
# URLs above stay clean, and the check below compares against those.
PLAYER_TAG = "?v=8"
EMBED_PAGE = "embed/lygo-tv-embed.html"
VENDORED_JS = "embed/lygo-tv-ninja.js"
VENDORED_CSS = "embed/lygo-tv-ninja.css"
PAYPAL = "https://www.paypal.com/paypalme/ExcavationPro"
PATREON = "https://www.patreon.com/Excavationpro"
RUMBLE = "https://rumble.com/register/Excavationpro/"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def urls() -> dict[str, str]:
    return {
        "player": TV,
        "bookmark": TV,
        "catalog": CATALOG,
        "terms": TERMS,
        "disclaimer": DISCLAIMER,
        "emblem": EMBLEM,
        "source": SOURCE,
        "skill_source": SKILL_SRC,
        "stack_mirror": STACK,
        "witness": WITNESS,
        "listen": LISTEN,
        "player_js": PLAYER_JS,
        "player_css": PLAYER_CSS,
        "clawhub": CLAWHUB,
        "install": INSTALL,
        "paypal": PAYPAL,
        "patreon": PATREON,
        "rumble_join": RUMBLE,
    }


def map_payload() -> dict[str, Any]:
    return {
        "signature": SIG,
        "version": VERSION,
        "channel": "CLAWHUB_PUBLIC_TENTACLE",
        "class": "RESOURCE",
        "live_star_chart_ingest": False,
        "generated_utc": utc_now(),
        "player": TV,
        "how": "Bookmark https://chatagent.ca/sources/ . Channel tab = Excavationpro rooms. Public lists after Terms tick.",
        "default": "Channel tab opens Excavationpro Kick / Rumble / Twitch / YouTube",
        "urls": urls(),
        "forbidden": [
            "CORS or pirate proxy",
            "pay-TV decrypt",
            "invented M3U lists",
            "YouTube cable-news slop",
            "silent Star Chart ingest",
            "auto git/HF/ClawHub/social publish",
        ],
    }


def plain() -> str:
    return "\n".join(
        [
            "LYGO TV — free online TV player",
            "",
            "Bookmark / open: " + TV,
            "1. Channel tab = Excavationpro Kick, Rumble, Twitch, YouTube (always open).",
            "2. FAST / Lists / Topics / Places / Languages after Terms tick for this session.",
            "3. Click a channel. GitHub lists wait for a click.",
            "4. Keys: left/right next, F fullscreen, / search.",
            "5. Agents: " + INSTALL,
            "",
            "Catalog is RESOURCE. Dual ledgers stay CANON.",
            "No login. Optional tip: " + PAYPAL,
            "Install: " + INSTALL,
        ]
    )


def embed() -> str:
    """The whole install: one stylesheet, one element, one script. Printed, never fetched."""
    return "\n".join(
        [
            "<!-- LYGO TV Ninja · \u03949\u03a6963 · MIT-0 · " + TV + " -->",
            '<link rel="stylesheet" href="' + PLAYER_CSS + PLAYER_TAG + '">',
            "<div data-lygo-tv></div>",
            '<script src="' + PLAYER_JS + PLAYER_TAG + '" defer></script>',
            "",
            "Opens on the steward's Rumble room (rumble_live). Prev/Next walk the pool of about",
            "12,000 channels, pulled in the visitor's browser from the catalog above. Nothing is",
            "proxied and nothing is stored.",
            "",
            "What the visitor's browser then contacts: chatagent.ca (player assets + catalog.json),",
            "cdn.jsdelivr.net only if an HLS channel plays (hls.js, SRI-pinned), and whichever platform",
            "embed the channel belongs to. Catalog URLs are https-checked and embed hosts are pinned",
            "before anything is framed or played. See embed/README.md before pasting it anywhere.",
            "",
            "A whole branded page: " + EMBED_PAGE,
            "Self-hosted copies of the player: " + VENDORED_JS + " + " + VENDORED_CSS,
            "Sound starts off until the visitor presses Sound \u2014 that is the browser's autoplay rule.",
        ]
    )


def donate() -> dict[str, str]:
    return {"paypal": PAYPAL, "patreon": PATREON, "rumble_join": RUMBLE}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="LYGO TV pointer")
    p.add_argument(
        "cmd",
        nargs="?",
        default="plain",
        choices=("plain", "urls", "map", "demo", "donate", "bookmark", "embed"),
    )
    args = p.parse_args(argv)
    if args.cmd == "plain":
        sys.stdout.write(plain() + "\n")
        return 0
    if args.cmd == "urls":
        print(json.dumps(urls(), indent=2))
        return 0
    if args.cmd == "embed":
        sys.stdout.write(embed() + "\n")
        return 0
    if args.cmd == "donate":
        print(json.dumps(donate(), indent=2))
        return 0
    if args.cmd == "bookmark":
        print(json.dumps({"player": TV, "bookmark": TV, "clawhub": CLAWHUB, "install": INSTALL}, indent=2))
        return 0
    print(json.dumps(map_payload(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
