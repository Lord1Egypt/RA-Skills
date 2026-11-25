#!/usr/bin/env python3
"""Gig Setlist Builder — energy-arc set sequencing with key/BPM transitions.

Input: song book JSON (see sample_songbook.json).
Output: ordered set(s) with running clock, transition report, ASCII energy
curve, runtime verdict vs your slot.

stdlib only.
"""
import argparse
import json
import math
import sys

NOTES = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4,
         "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
         "A#": 10, "Bb": 10, "B": 11}
REL_MINOR = {0: 9, 1: 10, 2: 11, 3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5,
             9: 6, 10: 7, 11: 8}  # major -> its relative minor pitch class

ARC = [(0.0, 7.5), (0.15, 8.5), (0.30, 7.0), (0.45, 4.5),
       (0.60, 5.5), (0.75, 8.0), (0.90, 9.5), (1.0, 10.0)]


def parse_key(s):
    s = (s or "").strip()
    minor = s.endswith("m")
    if minor:
        s = s[:-1]
    pc = NOTES.get(s)
    if pc is None:
        raise SystemExit(f"bad key: {s!r}")
    return pc, minor


def key_distance(a, b):
    """Circle-of-fifths distance; relative major/minor = 0."""
    pc_a, min_a = a
    pc_b, min_b = b
    # normalize minor to its relative major position on the circle of fifths
    FIFTHS = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]  # pitch class -> fifth-step
    pa = FIFTHS.index(pc_a if not min_a else REL_MINOR[pc_a])
    pb = FIFTHS.index(pc_b if not min_b else REL_MINOR[pc_b])
    d = abs(pa - pb)
    d = min(d, 12 - d)
    rel = (pc_a == REL_MINOR[pc_b]) or (pc_b == REL_MINOR[pc_a])
    return 0 if (rel and min_a != min_b) else d


def arc_target(frac):
    for (x0, y0), (x1, y1) in zip(ARC, ARC[1:]):
        if x0 <= frac <= x1:
            t = (frac - x0) / (x1 - x0) if x1 > x0 else 0
            return y0 + t * (y1 - y0)
    return ARC[-1][1]


def bpm_penalty(prev, cur):
    if prev is None or not prev.get("bpm") or not cur.get("bpm"):
        return 0.0
    rel = abs(cur["bpm"] - prev["bpm"]) / prev["bpm"]
    return max(0.0, rel - 0.12) * 40.0


def key_penalty(prev, cur):
    if prev is None or not prev.get("key") or not cur.get("key"):
        return 0.0
    return key_distance(parse_key(prev["key"]), parse_key(cur["key"])) * 1.5


def deal_snake(songs, n_sets):
    """Deal songs energy-desc in snaking order so every set gets a
    comparable energy mix (0,1,...,n-1,n-2,...,1 repeating)."""
    decks = [[] for _ in range(n_sets)]
    order = sorted(songs, key=lambda s: -s.get("energy", 5))
    seq = list(range(n_sets))
    if n_sets > 1:
        seq += list(range(n_sets - 2, 0, -1))
    for i, s in enumerate(order):
        decks[seq[i % len(seq)]].append(s)
    return decks


def build_set(songs, minutes, reserve_encore):
    pool = [dict(s) for s in songs]
    reserved = []
    if reserve_encore and len(pool) > 2:
        best = max(pool, key=lambda s: s.get("energy", 5))
        pool.remove(best)
        reserved = [best]
    total_min = sum(s.get("minutes", 4.2) for s in pool)
    avg = total_min / len(pool)
    n_slots = max(1, min(len(pool), int(round(minutes / avg))))
    chosen = []
    unused = list(pool)
    prev = None
    for i in range(n_slots):
        frac = i / max(1, n_slots - 1)
        target = arc_target(frac)
        # valley-stack guard: previous two slots both <=4 pushes target up
        if len(chosen) >= 2 and chosen[-1].get("energy", 5) <= 4 \
                and chosen[-2].get("energy", 5) <= 4:
            target = max(target, 6.0)

        def cost(s):
            c = (2.0 * abs(s.get("energy", 5) - target)
                 + bpm_penalty(prev, s) + key_penalty(prev, s))
            if s.get("must_play"):
                c -= 3.0  # musts gravitate to fitting slots, not slot 1
            return c

        musts_left = [s for s in unused if s.get("must_play")]
        slots_left = n_slots - i
        if musts_left and len(musts_left) >= slots_left:
            pick = min(musts_left, key=cost)   # forced: last chances
        else:
            pick = min(unused, key=cost)
        unused.remove(pick)
        chosen.append(pick)
        prev = pick
    return chosen, unused + reserved


def sparkline(energies):
    blocks = " .:-=+*#%@"
    out = []
    for e in energies:
        idx = min(9, max(0, int((e / 10.0) * 9.999)))
        out.append(blocks[idx])
    return "".join(out)


def fmt_mm(mins):
    h = int(mins // 60)
    m = int(round(mins % 60))
    return f"{h:d}:{m:02d}" if h else f"{m:d}m"


def verdict_bpm(prev, cur):
    if not prev or not prev.get("bpm") or not cur.get("bpm"):
        return ""
    rel = (cur["bpm"] - prev["bpm"]) / prev["bpm"]
    if abs(rel) > 0.12:
        return f"{prev['bpm']}->{cur['bpm']} BPM {rel:+.0%} HARD (walk it or MC over)"
    if abs(rel) > 0.06:
        return f"{prev['bpm']}->{cur['bpm']} BPM {rel:+.0%} ok"
    return f"{prev['bpm']}->{cur['bpm']} BPM smooth"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("songbook")
    p.add_argument("--minutes", type=float, default=45)
    p.add_argument("--sets", type=int, default=1)
    p.add_argument("--break-min", type=float, default=15)
    p.add_argument("--encore", action="store_true")
    p.add_argument("--only-must", action="store_true")
    a = p.parse_args()

    book = json.load(open(a.songbook, encoding="utf-8"))
    songs = book["songs"] if isinstance(book, dict) else book
    if a.only_must:
        songs = [s for s in songs if s.get("must_play")]
    if not songs:
        print("empty song book"); return 1

    clock = 0.0
    leftovers = []
    decks = deal_snake(songs, a.sets)
    for setno in range(1, a.sets + 1):
        pool = decks[setno - 1]
        chosen, unused = build_set(pool, a.minutes,
                                   a.encore and setno == a.sets)
        leftovers = unused
        run = sum(s.get("minutes", 4.2) for s in chosen)
        print("=" * 66)
        head = f"SET {setno}  ({len(chosen)} songs, {fmt_mm(run)} of {fmt_mm(a.minutes)} slot)"
        print(head + ("" if run <= a.minutes + 0.01 else "  ** OVER SLOT **"))
        print("=" * 66)
        t = 0.0
        energies = []
        for i, s in enumerate(chosen):
            clock_min = t
            t += s.get("minutes", 4.2)
            energies.append(s.get("energy", 5))
            key = s.get("key", "-")
            bpm = s.get("bpm", "")
            mark = " *" if s.get("must_play") else ""
            print(f"{i+1:>2}. {fmt_mm(clock_min):>5}  {s['title'][:34]:<34} "
                  f"{key:<4}{bpm:>4}  E{s.get('energy',5):<2}{mark}")
            if i > 0:
                prev = chosen[i - 1]
                if prev.get("key") and s.get("key"):
                    d = key_distance(parse_key(prev["key"]), parse_key(s["key"]))
                    kmsg = f"key {prev['key']}->{s['key']} dist {d}"
                    if d == 0:
                        kmsg = f"key {prev['key']}->{s['key']} smooth"
                    elif d >= 4:
                        kmsg = f"key {prev['key']}->{s['key']} CLASHY (dist {d})"
                else:
                    kmsg = "key n/a"
                bmsg = verdict_bpm(prev, s)
                print(f"      transition: {kmsg}; {bmsg}")
        print(f"energy arc: [{sparkline(energies)}]")
        if run > a.minutes + 0.01:
            cuts = sorted(chosen, key=lambda s: s.get("energy", 5))
            cands = [s["title"] for s in cuts if not s.get("must_play")][:2]
            print(f"OVER by {fmt_mm(run - a.minutes)} - cut candidates: "
                  + "; ".join(cands))
        if setno < a.sets:
            clock += run + a.break_min
            print(f"--- BREAK {fmt_mm(a.break_min)} (next set at "
                  f"T+{fmt_mm(clock)}) ---")
    if a.encore:
        cand = max(leftovers or songs, key=lambda s: s.get("energy", 5), default=None)
        if cand:
            print(f"\nENCORE reserved: {cand['title']} "
                  f"(E{cand.get('energy',5)}, {cand.get('key','-')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
