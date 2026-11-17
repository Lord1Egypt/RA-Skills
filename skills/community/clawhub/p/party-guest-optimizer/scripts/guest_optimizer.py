#!/usr/bin/env python3
"""guest_optimizer.py — guest-graph analysis, invite selection, seating charts.

Subcommands:
  analyze  — graph stats: isolation risks, clusters, energy balance
  invite   — pick max-N subset maximizing mix quality
  seat     — seating chart (round/long table or pods) via simulated annealing

Guest JSON schema in SKILL.md. Pure stdlib.
"""
import argparse
import json
import math
import random
import sys
from collections import defaultdict

EDGE_WEIGHT = {"close": 3, "know": 2, "friend": 2, "tension": -6, "ex": -6}


def load(path):
    with open(path) as f:
        return json.load(f)


class Graph:
    def __init__(self, data):
        self.guests = {g["id"]: g for g in data["guests"]}
        self.edges = {}
        for e in data.get("edges", []):
            self.edges[frozenset((e["a"], e["b"]))] = e["type"]
        self.keep_apart = [frozenset(p) for p in data.get("keep_apart", [])]
        self.must = set(data.get("must_invite", []))

    def edge(self, a, b):
        return self.edges.get(frozenset((a, b)))

    def ids(self):
        return list(self.guests)

    def interests(self, gid):
        return set(self.guests[gid].get("interests", []))

    def shared(self, a, b):
        return len(self.interests(a) & self.interests(b))

    def tension(self, a, b):
        e = self.edge(a, b)
        return e in ("tension", "ex") or frozenset((a, b)) in self.keep_apart

    def degree(self, gid, types=("close", "know", "friend")):
        return sum(1 for e, t in self.edges.items()
                   if gid in e and t in types)


def pair_score(g, a, b):
    """Quality of having a and b near each other."""
    s = 0.0
    e = g.edge(a, b)
    if e:
        s += EDGE_WEIGHT.get(e, 0)
    else:
        s += 2 * min(g.shared(a, b), 2)      # strangers with common ground
    if g.tension(a, b):
        s -= 6
    # talker dynamics: two max-talkers compete; talker+listener complement
    ta = g.guests[a].get("talker", 3)
    tb = g.guests[b].get("talker", 3)
    if ta + tb >= 9:
        s -= 1.5
    elif abs(ta - tb) == 2:
        s += 0.5
    return s


def cmd_analyze(g, args):
    print("=" * 60)
    print(f"GUEST GRAPH — {len(g.ids())} guests, {len(g.edges)} edges")
    print("=" * 60)
    isolated = []
    for gid in g.ids():
        d = g.degree(gid)
        if d == 0:
            isolated.append(gid)
    if isolated:
        print("\nISOLATION RISK (know nobody else):")
        for gid in isolated:
            ints = ", ".join(sorted(g.interests(gid))) or "no interests listed"
            print(f"  - {gid}: {ints}")
        print("  -> buddy-invite them with a friend, or add shared-interest guests")
    clusters = connected_clusters(g)
    print(f"\nClusters (mutual know/close): {len(clusters)}")
    for i, c in enumerate(sorted(clusters, key=len, reverse=True), 1):
        print(f"  cluster {i}: {', '.join(sorted(c))}")
    talkers = [gid for gid in g.ids() if g.guests[gid].get("talker", 3) >= 4]
    listeners = [gid for gid in g.ids() if g.guests[gid].get("talker", 3) <= 2]
    print(f"\nEnergy: {len(talkers)} big talkers ({', '.join(talkers) or '-'}), "
          f"{len(listeners)} quiet listeners ({', '.join(listeners) or '-'})")
    if len(talkers) > 2 * len(listeners) + 2 and len(g.ids()) > 6:
        print("  -> talker-heavy: sprinkle listeners per table/pod, or it's monologue city")
    tensions = [(a, b) for e in g.edges if g.edges[e] in ("tension", "ex")
                for a in [tuple(e)[0]] for b in [tuple(e)[1]]]
    for pair in g.keep_apart:
        if pair not in [frozenset(t) for t in tensions]:
            tensions.append(tuple(pair))
    if tensions:
        print("\nTension pairs (never adjacent):")
        for a, b in tensions:
            print(f"  - {a} <-> {b}")
    strangers = stranger_links(g)
    if strangers:
        print("\nBest new-connection opportunities (strangers, shared interests):")
        for a, b, n in strangers[:8]:
            common = ", ".join(sorted(g.interests(a) & g.interests(b)))
            print(f"  - {a} + {b}: {common}")
    return 0


def connected_clusters(g):
    seen, clusters = set(), []
    adj = defaultdict(set)
    for e, t in g.edges.items():
        if t in ("close", "know", "friend"):
            a, b = tuple(e)
            adj[a].add(b)
            adj[b].add(a)
    for gid in g.ids():
        if gid in seen:
            continue
        comp, stack = set(), [gid]
        while stack:
            cur = stack.pop()
            if cur in comp:
                continue
            comp.add(cur)
            stack.extend(adj[cur] - comp)
        seen |= comp
        clusters.append(comp)
    return clusters


def stranger_links(g):
    ids = g.ids()
    out = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if g.edge(a, b) is None and not g.tension(a, b):
                n = g.shared(a, b)
                if n:
                    out.append((a, b, n))
    return sorted(out, key=lambda t: -t[2])


def subset_score(g, subset):
    s = 0.0
    subset = list(subset)
    for i in range(len(subset)):
        for j in range(i + 1, len(subset)):
            a, b = subset[i], subset[j]
            s += pair_score(g, a, b)
            if g.tension(a, b):
                s -= 4
    for gid in subset:
        if g.degree(gid) == 0:
            # isolation is softer if they share interests with someone
            if not any(g.shared(gid, o) for o in subset if o != gid):
                s -= 5
    talkers = sum(1 for gid in subset if g.guests[gid].get("talker", 3) >= 4)
    listeners = sum(1 for gid in subset if g.guests[gid].get("talker", 3) <= 2)
    s += 2 * min(talkers, listeners)     # balance bonus
    return s


def cmd_invite(g, args):
    ids = [i for i in g.ids()]
    if args.max >= len(ids):
        print("[i] pool fits entirely — nothing to select")
        return 0
    # greedy seed: must-invites first, then best marginal gain
    chosen = [i for i in ids if i in g.must]
    rest = [i for i in ids if i not in chosen]
    random.seed(42)
    while len(chosen) < args.max and rest:
        best, best_score = None, -1e18
        for cand in rest:
            trial = chosen + [cand]
            sc = subset_score(g, trial) / len(trial)
            if sc > best_score:
                best, best_score = cand, sc
        chosen.append(best)
        rest.remove(best)
    # local swaps
    improved = True
    while improved:
        improved = False
        for out in list(chosen):
            if out in g.must:
                continue
            for inc in rest:
                trial = [x for x in chosen if x != out] + [inc]
                if subset_score(g, trial) > subset_score(g, chosen):
                    chosen.remove(out)
                    chosen.append(inc)
                    rest.remove(inc)
                    rest.append(out)
                    improved = True
                    break
            if improved:
                break
    cut = sorted(set(ids) - set(chosen))
    print("INVITE (max %d of %d):" % (args.max, len(ids)))
    for gid in sorted(chosen):
        tags = []
        if gid in g.must:
            tags.append("must")
        d = g.degree(gid)
        tags.append(f"knows {d}")
        print(f"  + {gid} ({', '.join(tags)})")
    print("\nCUT (host may override):")
    for gid in cut:
        print(f"  - {gid}")
    return 0


def seat_neighbors(seats, i, n, ring=True):
    left = seats[(i - 1) % n]
    right = seats[(i + 1) % n]
    if not ring and i == 0:
        left = None
    if not ring and i == n - 1:
        right = None
    return left, right


def seat_score(g, seats, ring=True):
    n = len(seats)
    total = 0.0
    for i, gid in enumerate(seats):
        left, right = seat_neighbors(seats, i, n, ring)
        for nb in (left, right):
            if nb:
                total += pair_score(g, gid, nb)
        if ring and n % 2 == 0:
            across = seats[(i + n // 2) % n]
            total += 0.5 * pair_score(g, gid, across)
    # hard constraint check
    seat_pos = {gid: i for i, gid in enumerate(seats)}
    for pair in g.keep_apart:
        a, b = tuple(pair)
        if a in seat_pos and b in seat_pos:
            d = min((seat_pos[a] - seat_pos[b]) % n,
                    (seat_pos[b] - seat_pos[a]) % n)
            if d <= 1 or (ring and d == n - 1) or (ring and n % 2 == 0 and d == n // 2):
                total -= 1000
    return total


def cmd_seat(g, args):
    ids = g.ids()
    if args.table and len(ids) > args.table:
        print(f"[!] {len(ids)} guests > table size {args.table}")
        return 1
    n = len(ids)
    ring = args.round
    random.seed(7)
    best, best_score = None, -1e18
    for restart in range(8):
        seats = ids[:]
        random.shuffle(seats)
        cur = seat_score(g, seats, ring)
        T0, T1, iters = 2.0, 0.01, 6000
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            i, j = random.randrange(n), random.randrange(n)
            if i == j:
                continue
            seats[i], seats[j] = seats[j], seats[i]
            new = seat_score(g, seats, ring)
            if new >= cur or random.random() < math.exp((new - cur) / T):
                cur = new
            else:
                seats[i], seats[j] = seats[j], seats[i]
        if cur > best_score:
            best, best_score = seats, cur
    print("=" * 60)
    kind = "round table" if ring else "long table"
    print(f"SEATING CHART ({kind}, {n} guests) — score {best_score:.1f}")
    print("=" * 60)
    # linear print with neighbor annotations
    width = max(len(x) for x in ids)
    for i, gid in enumerate(best):
        left, right = seat_neighbors(best, i, n, ring)
        l = left or "wall"
        r = right or "wall"
        print(f"  seat {i+1:>2}: {gid:<{width}}   (L: {l:<{width}}  R: {r})")
    if ring:
        print(f"  (seat {n} wraps next to seat 1)")
    print("\nMIX REPORT (introduction cheat sheet):")
    for a, b, _n in stranger_links(g)[:12]:
        for i, gid in enumerate(best):
            left, right = seat_neighbors(best, i, n, ring)
            if gid == a and b in (left, right):
                common = ", ".join(sorted(g.interests(a) & g.interests(b)))
                print(f"  seated together: {a} + {b} — both into {common}")
    for a, b, _n in stranger_links(g)[:12]:
        if a in best and b in best:
            common = ", ".join(sorted(g.interests(a) & g.interests(b)))
            print(f"  introduce: {a} + {b} ({common})")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("analyze", help="graph analysis")
    p.add_argument("file")
    p.set_defaults(fn=lambda g, a: cmd_analyze(g, a))
    p = sub.add_parser("invite", help="select max-N subset")
    p.add_argument("file")
    p.add_argument("--max", type=int, required=True)
    p.set_defaults(fn=lambda g, a: cmd_invite(g, a))
    p = sub.add_parser("seat", help="seating chart")
    p.add_argument("file")
    p.add_argument("--table", type=int, default=None)
    p.add_argument("--round", action="store_true")
    p.add_argument("--pods", type=int, default=None)
    p.set_defaults(fn=lambda g, a: cmd_seat(g, a))
    args = ap.parse_args()
    g = Graph(load(args.file))
    return args.fn(g, args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
