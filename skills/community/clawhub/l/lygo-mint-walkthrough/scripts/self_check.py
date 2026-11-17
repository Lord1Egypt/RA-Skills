#!/usr/bin/env python3
from __future__ import annotations
import json, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mint_walkthrough as m  # noqa: E402

def main() -> int:
    intro = m.step_intro()
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write("# Test Pack\n\nHello LYGO.\n")
        pack = f.name
    minted = m.step_mint(pack, "test.v1", "Test Pack", i_consent=True)
    digest = minted.get("record", {}).get("sha256", "")
    ver = m.step_verify(pack=pack)
    snip = m.step_snippet(digest, "Test Pack")
    ok = intro.get("ok") and minted.get("ok") and ver.get("ok") and snip.get("ok") and len(digest) == 64
    print(json.dumps({"ok": ok, "sha256": digest[:16], "in_ledger": ver.get("in_local_ledger")}, indent=2))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
