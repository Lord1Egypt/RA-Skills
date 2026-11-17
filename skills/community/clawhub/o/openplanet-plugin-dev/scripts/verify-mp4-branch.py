#!/usr/bin/env python3
"""Static check that an Openplanet .as file's MP4 branch uses only cross-game-safe API.

AngelScript for Maniaplanet 4 has NO offline compiler, so this is a cheap
pre-load guard (complement to the in-game kill+relaunch+greplog check):
extract the `#elif MP4` (and `#else`) branch and confirm it contains NO
TMNEXT-only symbols, and that every `app.<member>` it uses exists in
Openplanet4.json (ns.Game.CGameCtnApp.m[]).

Usage:
    python verify-mp4-branch.py <file.as> [Openplanet4.json]

Exits 0 on PASS, 1 on FAIL. Designed to be run from a terminal/skill, not by hand
re-typed each time. Default reflection DB path matches this user's MP4 install.
"""
import json, io, re, sys


def main():
    if len(sys.argv) < 2:
        print("usage: verify-mp4-branch.py <file.as> [Openplanet4.json]")
        sys.exit(2)
    aspath = sys.argv[1]
    jsppath = sys.argv[2] if len(sys.argv) > 2 else r'C:/Users/tomekdot/Openplanet4/Openplanet4.json'

    txt = io.open(aspath, encoding='utf-8').read()
    lines = txt.splitlines()

    # Extract the #elif MP4 (+ #else) branch, stopping at #endif.
    branch = []
    cap = False
    for ln in lines:
        s = ln.strip()
        if s.startswith('#if TMNEXT'):
            cap = False
        elif s.startswith('#elif MP4'):
            cap = True
        elif s.startswith('#else'):
            if cap:
                cap = False
                continue
        elif s.startswith('#endif'):
            if cap:
                cap = False
        if cap:
            branch.append(ln)
    code = "\n".join(branch)

    forbidden = ['CTrackManiaMenus', 'NGameLoadProgress', 'LoadProgress']
    bad = [t for t in forbidden if t in code]

    db = json.load(io.open(jsppath, encoding='utf-8'))
    appm = {m['n'] for m in db['ns']['Game']['CGameCtnApp']['m']}
    used = set(re.findall(r'app\.(\w+)', code))
    missing = [u for u in used if u not in appm]

    ok = (not bad) and (not missing)
    print(f"MP4 branch lines           : {len(branch)}")
    print(f"forbidden TMNEXT symbols    : {bad if bad else 'none'}")
    print(f"app.<member> missing in MP4  : {missing if missing else 'none'}")
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
