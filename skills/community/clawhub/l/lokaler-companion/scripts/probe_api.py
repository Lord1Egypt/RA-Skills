#!/usr/bin/env python3
"""Endpunkte abfragen und die tatsaechliche JSON-Struktur drucken.

Der Sinn: Eine Oberflaeche gegen geratene Feldnamen zu schreiben ist der
haeufigste Grund fuer Anzeigen voller "undefined". Erst messen, dann schreiben.

    python probe_api.py http://127.0.0.1:8765 /api/status /api/live/all

Ohne Pfadangaben werden ein paar uebliche durchprobiert.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

USUAL = ["/api/status", "/api/state", "/api/events", "/api/items", "/api/health"]
MAX_DEPTH = 4


def sample(value: str, width: int = 58) -> str:
    """Einzeiliger, gekuerzter Beispielwert."""
    text = str(value).replace("\n", " ").replace("\r", " ")
    return text if len(text) <= width else text[: width - 1] + "…"


def describe(node, prefix: str = "", depth: int = 0) -> None:
    """Struktur eines JSON-Knotens rekursiv ausgeben."""
    pad = "  " * (depth + 1)

    if isinstance(node, dict):
        if depth >= MAX_DEPTH:
            print(f"{pad}{{…{len(node)} Schluessel}}")
            return
        for key, val in node.items():
            if isinstance(val, dict):
                print(f"{pad}{key}: Objekt")
                describe(val, prefix, depth + 1)
            elif isinstance(val, list):
                kinds = {type(x).__name__ for x in val[:5]}
                print(f"{pad}{key}: Liste[{len(val)}] {'/'.join(sorted(kinds)) or '-'}")
                if val and isinstance(val[0], (dict, list)):
                    describe(val[0], prefix, depth + 1)
                elif val:
                    print(f"{pad}  z. B. {sample(val[0])}")
            elif val is None:
                print(f"{pad}{key}: null   <- unbekannt, nicht mit false verwechseln")
            else:
                print(f"{pad}{key}: {type(val).__name__} = {sample(val)}")

    elif isinstance(node, list):
        kinds = {type(x).__name__ for x in node[:5]}
        print(f"{pad}Liste[{len(node)}] {'/'.join(sorted(kinds)) or '-'}")
        if node:
            describe(node[0], prefix, depth + 1)

    else:
        print(f"{pad}{type(node).__name__} = {sample(node)}")


def probe(base: str, path: str, timeout: int = 10) -> bool:
    url = base.rstrip("/") + path
    print(f"\n=== {path} ===")
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "?")
            raw = resp.read()
            print(f"  HTTP {resp.status} · {ctype} · {len(raw):,} B")
            cors = resp.headers.get("Access-Control-Allow-Origin")
            print(f"  CORS: {cors if cors else 'FEHLT — Abruf aus der App wird scheitern'}")
    except urllib.error.HTTPError as err:
        print(f"  HTTP {err.code} {err.reason}")
        return False
    except Exception as err:                                   # noqa: BLE001
        print(f"  nicht erreichbar: {err}")
        return False

    try:
        describe(json.loads(raw))
    except json.JSONDecodeError:
        print(f"  kein JSON: {sample(raw[:200].decode('utf-8', 'replace'))}")
    return True


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    base, paths = argv[0], argv[1:] or USUAL
    print(f"Server: {base}")
    ok = sum(probe(base, p) for p in paths)
    print(f"\n{ok} von {len(paths)} Endpunkten geantwortet.")
    if not ok:
        print("Laeuft der Server? Stimmt der Port?")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
