#!/usr/bin/env python3
import argparse
import copy
import html
import json
import random
import shutil
import subprocess
from datetime import datetime
from itertools import combinations
from pathlib import Path


def norm_name(name):
    return " ".join(name.strip().split())


def load_state(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def timestamp():
    return datetime.now().isoformat(timespec="seconds")


def parse_players(raw):
    parts = raw.split(",")
    players = [norm_name(p) for p in parts if norm_name(p)]
    seen = set()
    out = []
    for p in players:
        key = p.casefold()
        if key not in seen:
            out.append(p)
            seen.add(key)
    if len(out) < 4:
        raise SystemExit("Need at least 4 players.")
    return out


def ensure_player_statuses(state):
    statuses = state.setdefault("player_statuses", {})
    for p in state.get("players", []):
        statuses.setdefault(p, "active")
    for rnd in state.get("rounds", []):
        for p in rnd.get("byes", []):
            statuses.setdefault(p, "inactive")
        for m in rnd.get("matches", []):
            for p in m["team1"] + m["team2"]:
                statuses.setdefault(p, "inactive")
    return statuses


def add_event(state, event_type, **payload):
    payload["type"] = event_type
    payload["at"] = timestamp()
    state.setdefault("events", []).append(payload)


def last_round_has_unscored_matches(state):
    if not state.get("rounds"):
        return False
    last_round = state["rounds"][-1]
    return any(not m.get("score") for m in last_round.get("matches", []))


def require_open_ended(state):
    if not state.get("open_ended"):
        raise SystemExit("This command is only for open-ended sessions. Use new-session to create one.")


def empty_stats(players):
    return {
        p: {
            "games": 0,
            "wins": 0,
            "losses": 0,
            "points_for": 0,
            "points_against": 0,
            "diff": 0,
            "byes": 0,
        }
        for p in players
    }


def completed_matches(state):
    for rnd in state["rounds"]:
        for match in rnd["matches"]:
            if match.get("score"):
                yield rnd, match


def compute_history(state):
    partner = {}
    opponent = {}
    played = {}
    byes = {}
    for p in state["players"]:
        partner[p] = {}
        opponent[p] = {}
        played[p] = 0
        byes[p] = 0
    for rnd in state["rounds"]:
        for p in rnd.get("byes", []):
            byes[p] = byes.get(p, 0) + 1
        for m in rnd["matches"]:
            t1, t2 = m["team1"], m["team2"]
            players = t1 + t2
            for p in players:
                played[p] = played.get(p, 0) + 1
            add_pair(partner, t1[0], t1[1])
            add_pair(partner, t2[0], t2[1])
            for a in t1:
                for b in t2:
                    add_pair(opponent, a, b)
    return partner, opponent, played, byes


def add_pair(table, a, b, inc=1):
    table.setdefault(a, {})
    table.setdefault(b, {})
    table[a][b] = table[a].get(b, 0) + inc
    table[b][a] = table[b].get(a, 0) + inc


def pair_count(table, a, b):
    return table.get(a, {}).get(b, 0)


def best_pairing(group, partner_hist, opponent_hist):
    a, b, c, d = group
    options = [
        ((a, b), (c, d)),
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    ]
    best = None
    for t1, t2 in options:
        partner_penalty = pair_count(partner_hist, t1[0], t1[1]) + pair_count(partner_hist, t2[0], t2[1])
        opponent_penalty = sum(pair_count(opponent_hist, x, y) for x in t1 for y in t2)
        score = partner_penalty * 5 + opponent_penalty
        if best is None or score < best[0]:
            best = (score, t1, t2)
    return list(best[1]), list(best[2])


def rolling_bench(players, active_count, rnd_idx, cycle_start_round):
    bench_count = len(players) - active_count
    if bench_count <= 0:
        return players[:], []
    start = ((rnd_idx - cycle_start_round) * bench_count) % len(players)
    bench_indexes = {(start + i) % len(players) for i in range(bench_count)}
    bench = [p for i, p in enumerate(players) if i in bench_indexes]
    active = [p for i, p in enumerate(players) if i not in bench_indexes]
    return active, bench


def choose_round(players, courts, partner_hist, opponent_hist, played, byes, rnd_idx, rng, cycle_start_round):
    capacity = courts * 4
    active_count = min(len(players), capacity)
    active_count -= active_count % 4
    if active_count < 4:
        raise SystemExit("Not enough active players for a match.")

    active, bench = rolling_bench(players, active_count, rnd_idx, cycle_start_round)

    groups = []
    remaining = active[:]
    for _ in range(active_count // 4):
        if len(remaining) == 4:
            groups.append(remaining[:])
            remaining = []
            break
        best = None
        sample_combos = list(combinations(remaining, 4))
        if len(sample_combos) > 450:
            rng.shuffle(sample_combos)
            sample_combos = sample_combos[:450]
        for combo in sample_combos:
            combo = list(combo)
            _, t1, t2 = (0, *best_pairing(combo, partner_hist, opponent_hist))
            partner_penalty = pair_count(partner_hist, t1[0], t1[1]) + pair_count(partner_hist, t2[0], t2[1])
            opponent_penalty = sum(pair_count(opponent_hist, x, y) for x in t1 for y in t2)
            played_spread = max(played.get(p, 0) for p in combo) - min(played.get(p, 0) for p in combo)
            score = partner_penalty * 7 + opponent_penalty * 2 + played_spread
            if best is None or score < best[0]:
                best = (score, combo)
        group = list(best[1])
        groups.append(group)
        remaining = [p for p in remaining if p not in group]

    matches = []
    for court, group in enumerate(groups, start=1):
        t1, t2 = best_pairing(group, partner_hist, opponent_hist)
        matches.append({"court": court, "team1": t1, "team2": t2, "score": None})
        add_pair(partner_hist, t1[0], t1[1])
        add_pair(partner_hist, t2[0], t2[1])
        for a in t1:
            for b in t2:
                add_pair(opponent_hist, a, b)
        for p in group:
            played[p] = played.get(p, 0) + 1
    for p in bench:
        byes[p] = byes.get(p, 0) + 1

    return {"round": rnd_idx, "matches": matches, "byes": bench}


def capacity_summary(players, courts):
    player_count = len(players)
    capacity = courts * 4
    active_count = min(player_count, capacity)
    active_count -= active_count % 4
    byes = player_count - active_count
    used_courts = active_count // 4
    ideal_courts = player_count // 4 if player_count % 4 == 0 else None
    return {
        "player_count": player_count,
        "capacity": capacity,
        "active_count": active_count,
        "byes": byes,
        "used_courts": used_courts,
        "idle_courts": max(courts - used_courts, 0),
        "ideal_courts": ideal_courts,
    }


def print_capacity_warnings(players, courts):
    summary = capacity_summary(players, courts)
    if summary["active_count"] < 4:
        return
    if summary["byes"] > 0:
        print(
            f"Warning: {summary['player_count']} players on {courts} court(s) means "
            f"{summary['byes']} bye player(s) per round."
        )
    if summary["idle_courts"] > 0:
        print(
            f"Warning: only {summary['used_courts']} of {courts} court(s) can be used with "
            f"{summary['player_count']} active players."
        )
    if summary["ideal_courts"] is not None and courts < summary["ideal_courts"]:
        print(
            f"Tip: {summary['player_count']} players need {summary['ideal_courts']} court(s) "
            "for everyone to play every round."
        )


def generate_rounds(players, courts, rounds, seed, preserve_state=None, from_round=1, cycle_start_round=None):
    rng = random.Random(seed)
    if cycle_start_round is None:
        cycle_start_round = from_round
    partner_hist = {p: {} for p in players}
    opponent_hist = {p: {} for p in players}
    played = {p: 0 for p in players}
    byes = {p: 0 for p in players}
    new_rounds = []

    if preserve_state:
        for rnd in preserve_state["rounds"]:
            if rnd["round"] < from_round:
                new_rounds.append(copy.deepcopy(rnd))
                for p in rnd.get("byes", []):
                    byes[p] = byes.get(p, 0) + 1
                for m in rnd["matches"]:
                    t1, t2 = m["team1"], m["team2"]
                    add_pair(partner_hist, t1[0], t1[1])
                    add_pair(partner_hist, t2[0], t2[1])
                    for a in t1:
                        for b in t2:
                            add_pair(opponent_hist, a, b)
                    for p in t1 + t2:
                        played[p] = played.get(p, 0) + 1

    for rnd_idx in range(from_round, rounds + 1):
        new_rounds.append(choose_round(players, courts, partner_hist, opponent_hist, played, byes, rnd_idx, rng, cycle_start_round))
    return new_rounds


LEADERBOARD_SORTS = ("official", "points", "wins", "points-pct", "wins-pct")


def pct(numerator, denominator):
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def leaderboard_sort_key(row, sort_by):
    name = row["player"].casefold()
    if sort_by == "official":
        return (-row["wins"], -row["wins_pct"], -row["points_for"], -row["diff"], row["games"], name)
    if sort_by == "points":
        return (-row["points_for"], -row["diff"], -row["wins"], -row["points_pct"], row["games"], name)
    if sort_by == "wins":
        return (-row["wins"], -row["wins_pct"], -row["points_for"], -row["diff"], row["games"], name)
    if sort_by == "points-pct":
        return (-row["points_pct"], -row["points_for"], -row["diff"], -row["wins"], -row["games"], name)
    if sort_by == "wins-pct":
        return (-row["wins_pct"], -row["wins"], -row["points_pct"], -row["points_for"], -row["diff"], -row["games"], name)
    raise SystemExit(f"Unknown leaderboard sort: {sort_by}")


def leaderboard_tie_key(row, sort_by):
    if sort_by == "official":
        return (row["wins"], round(row["wins_pct"], 10), row["points_for"], row["diff"], row["games"])
    if sort_by == "points":
        return (row["points_for"], row["diff"], row["wins"], round(row["points_pct"], 10), row["games"])
    if sort_by == "wins":
        return (row["wins"], round(row["wins_pct"], 10), row["points_for"], row["diff"], row["games"])
    if sort_by == "points-pct":
        return (round(row["points_pct"], 10), row["points_for"], row["diff"], row["wins"], row["games"])
    if sort_by == "wins-pct":
        return (round(row["wins_pct"], 10), row["wins"], round(row["points_pct"], 10), row["points_for"], row["diff"], row["games"])
    raise SystemExit(f"Unknown leaderboard sort: {sort_by}")


def rank_rows(rows, sort_by):
    ranked = []
    previous_key = None
    current_rank = 0
    for index, row in enumerate(rows, 1):
        tie_key = leaderboard_tie_key(row, sort_by)
        if tie_key != previous_key:
            current_rank = index
            previous_key = tie_key
        ranked.append({"rank": current_rank, **row})
    return ranked


def format_percent(value):
    return f"{value * 100:.1f}%"


def leaderboard_columns(sort_by):
    common_tail = [("Diff", "diff"), ("W-L", "record"), ("Games", "games"), ("Byes", "byes")]
    if sort_by in ("official", "wins"):
        return [("Wins", "wins"), ("Win%", "wins_pct"), ("Pts", "points_for"), *common_tail]
    if sort_by == "points":
        return [("Pts", "points_for"), ("Pts%", "points_pct"), ("Wins", "wins"), *common_tail]
    if sort_by == "points-pct":
        return [("Pts%", "points_pct"), ("Pts", "points_for"), ("Wins", "wins"), *common_tail]
    if sort_by == "wins-pct":
        return [("Win%", "wins_pct"), ("Wins", "wins"), ("Pts", "points_for"), ("Pts%", "points_pct"), *common_tail]
    raise SystemExit(f"Unknown leaderboard sort: {sort_by}")


def format_leaderboard_value(row, key):
    if key in ("points_pct", "wins_pct"):
        return format_percent(row[key])
    if key == "diff":
        return f"{row[key]:+}"
    if key == "record":
        return f"{row['wins']}-{row['losses']}"
    return str(row[key])


def leaderboard(state, sort_by="points"):
    if sort_by not in LEADERBOARD_SORTS:
        raise SystemExit(f"Unknown leaderboard sort: {sort_by}")
    all_players = list(state["players"])
    seen = {p.casefold() for p in all_players}
    for rnd in state["rounds"]:
        for p in rnd.get("byes", []):
            if p.casefold() not in seen:
                all_players.append(p)
                seen.add(p.casefold())
        for m in rnd["matches"]:
            for p in m["team1"] + m["team2"]:
                if p.casefold() not in seen:
                    all_players.append(p)
                    seen.add(p.casefold())
    stats = empty_stats(all_players)
    for rnd in state["rounds"]:
        for p in rnd.get("byes", []):
            stats[p]["byes"] += 1
        for m in rnd["matches"]:
            if not m.get("score"):
                continue
            a, b = m["score"]
            t1, t2 = m["team1"], m["team2"]
            for p in t1:
                stats[p]["games"] += 1
                stats[p]["points_for"] += a
                stats[p]["points_against"] += b
            for p in t2:
                stats[p]["games"] += 1
                stats[p]["points_for"] += b
                stats[p]["points_against"] += a
            if a > b:
                for p in t1: stats[p]["wins"] += 1
                for p in t2: stats[p]["losses"] += 1
            elif b > a:
                for p in t2: stats[p]["wins"] += 1
                for p in t1: stats[p]["losses"] += 1
    points_per_game = state.get("points_per_game") or 0
    for p, s in stats.items():
        s["diff"] = s["points_for"] - s["points_against"]
        s["max_points_possible"] = s["games"] * points_per_game
        s["points_pct"] = pct(s["points_for"], s["max_points_possible"])
        s["max_wins_possible"] = s["games"]
        s["wins_pct"] = pct(s["wins"], s["max_wins_possible"])
    rows = [{"player": p, **s} for p, s in stats.items()]
    rows.sort(key=lambda r: leaderboard_sort_key(r, sort_by))
    return rank_rows(rows, sort_by)


def format_match(m):
    score = "-" if not m.get("score") else f"{m['score'][0]}-{m['score'][1]}"
    return f"Court {m['court']}: {m['team1'][0]} / {m['team1'][1]} vs {m['team2'][0]} / {m['team2'][1]} [{score}]"


def cmd_new(args):
    players = parse_players(args.players)
    rounds = generate_rounds(players, args.courts, args.rounds, args.seed, None, 1)
    state = {
        "name": args.name,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "players": players,
        "courts": args.courts,
        "round_count": args.rounds,
        "points_per_game": args.points,
        "seed": args.seed,
        "open_ended": False,
        "player_statuses": {p: "active" for p in players},
        "rounds": rounds,
    }
    save_state(state, args.out)
    print(f"Created {args.out}")
    print_capacity_warnings(players, args.courts)
    print_schedule(state)


def cmd_new_session(args):
    players = parse_players(args.players)
    state = {
        "name": args.name,
        "created_at": timestamp(),
        "players": players,
        "courts": args.courts,
        "round_count": None,
        "points_per_game": args.points,
        "seed": args.seed,
        "open_ended": True,
        "player_statuses": {p: "active" for p in players},
        "events": [],
        "rounds": [],
    }
    add_event(state, "session_started", players=players)
    save_state(state, args.out)
    print(f"Created open-ended session {args.out}")
    print_capacity_warnings(players, args.courts)
    print_schedule(state)


def print_schedule(state):
    print(f"\n{state['name']}")
    label = "Active players" if state.get("open_ended") else "Players"
    print(f"{label}: {', '.join(state['players'])}")
    for rnd in state["rounds"]:
        print(f"\nRound {rnd['round']}")
        for m in rnd["matches"]:
            print("  " + format_match(m))
        if rnd.get("byes"):
            print("  Bye: " + ", ".join(rnd["byes"]))


def cmd_schedule(args):
    print_schedule(load_state(args.state))


def cmd_next_round(args):
    state = load_state(args.state)
    require_open_ended(state)
    if last_round_has_unscored_matches(state) and not args.force:
        raise SystemExit("Current round still has unscored matches. Score it first, or use --force to create another round anyway.")
    if len(state["players"]) < 4:
        raise SystemExit("Need at least 4 active players to generate a round.")
    if args.seed is not None:
        state["seed"] = args.seed
    next_round = max((rnd["round"] for rnd in state["rounds"]), default=0) + 1
    state["rounds"] = generate_rounds(
        state["players"],
        state["courts"],
        next_round,
        state["seed"],
        preserve_state=state,
        from_round=next_round,
        cycle_start_round=1,
    )
    add_event(state, "round_generated", round=next_round, active_players=list(state["players"]))
    save_state(state, args.state)
    print(f"Generated round {next_round}")
    print_schedule({"name": state["name"], "players": state["players"], "rounds": [state["rounds"][-1]], "open_ended": True})


def parse_score(raw):
    if "-" not in raw:
        raise SystemExit("Score format must be like 14-10.")
    a, b = raw.split("-", 1)
    return [int(a.strip()), int(b.strip())]


def validate_score_total(score, points_per_game):
    if points_per_game <= 0:
        return
    total = sum(score)
    if total != points_per_game:
        raise SystemExit(
            f"Invalid score {score[0]}-{score[1]}. Total points must be exactly {points_per_game}; "
            "please enter the game score again."
        )


def cmd_score(args):
    state = load_state(args.state)
    found = None
    for rnd in state["rounds"]:
        if rnd["round"] == args.round:
            for m in rnd["matches"]:
                if m["court"] == args.court:
                    found = m
                    break
    if not found:
        raise SystemExit("Match not found.")
    score = parse_score(args.score)
    validate_score_total(score, state.get("points_per_game") or 0)
    found["score"] = score
    save_state(state, args.state)
    print(f"Recorded round {args.round} court {args.court}: {args.score}")
    print_leaderboard(state)


def print_leaderboard(state, sort_by="points"):
    rows = leaderboard(state, sort_by)
    print(f"\nLeaderboard by {sort_by}")
    columns = leaderboard_columns(sort_by)
    print("Rank | Player | " + " | ".join(label for label, _ in columns))
    for r in rows:
        print(f"{r['rank']:>4} | {r['player']} | " + " | ".join(format_leaderboard_value(r, key) for _, key in columns))


def cmd_leaderboard(args):
    print_leaderboard(load_state(args.state), args.sort)


def cmd_switch(args):
    state = load_state(args.state)
    out_player = norm_name(args.out_player)
    in_player = norm_name(args.in_player)
    if out_player not in state["players"]:
        raise SystemExit(f"{out_player} is not in tournament players.")
    if in_player in state["players"]:
        raise SystemExit(f"{in_player} is already in tournament players.")

    for rnd in state["rounds"]:
        if rnd["round"] >= args.from_round:
            for m in rnd["matches"]:
                if m.get("score") and out_player in (m["team1"] + m["team2"]):
                    raise SystemExit("Cannot switch from a round with completed score for outgoing player. Choose a later round.")

    state["players"] = [in_player if p == out_player else p for p in state["players"]]
    state["rounds"] = generate_rounds(
        state["players"],
        state["courts"],
        state["round_count"],
        state["seed"],
        preserve_state=state,
        from_round=args.from_round,
    )
    state.setdefault("switches", []).append({
        "out": out_player,
        "in": in_player,
        "from_round": args.from_round,
        "at": datetime.now().isoformat(timespec="seconds"),
    })
    save_state(state, args.state)
    print(f"Switched {out_player} -> {in_player} from round {args.from_round}")
    print_schedule(state)


def cmd_add_player(args):
    state = load_state(args.state)
    player = norm_name(args.player)
    if not player:
        raise SystemExit("Player name cannot be empty.")
    if player in state["players"]:
        raise SystemExit(f"{player} is already in tournament players.")
    for rnd in state["rounds"]:
        if rnd["round"] >= args.from_round:
            for m in rnd["matches"]:
                if m.get("score"):
                    raise SystemExit("Cannot add a player from a round that already has completed scores. Choose a later round.")

    state["players"].append(player)
    if args.seed is not None:
        state["seed"] = args.seed
    ensure_player_statuses(state)[player] = "active"
    state["rounds"] = generate_rounds(
        state["players"],
        state["courts"],
        state["round_count"],
        state["seed"],
        preserve_state=state,
        from_round=args.from_round,
    )
    state.setdefault("player_additions", []).append({
        "player": player,
        "from_round": args.from_round,
        "at": timestamp(),
    })
    save_state(state, args.state)
    print(f"Added {player} from round {args.from_round}")
    print_schedule(state)


def cmd_join_player(args):
    state = load_state(args.state)
    require_open_ended(state)
    player = norm_name(args.player)
    if not player:
        raise SystemExit("Player name cannot be empty.")
    if player in state["players"]:
        raise SystemExit(f"{player} is already active.")
    statuses = ensure_player_statuses(state)
    state["players"].append(player)
    statuses[player] = "active"
    add_event(state, "player_joined", player=player, effective_round=len(state["rounds"]) + 1)
    save_state(state, args.state)
    print(f"{player} joined. Effective from next generated round.")
    print_schedule(state)


def cmd_leave_player(args):
    state = load_state(args.state)
    require_open_ended(state)
    player = norm_name(args.player)
    if player not in state["players"]:
        raise SystemExit(f"{player} is not active.")
    remaining_players = [p for p in state["players"] if p != player]
    if len(remaining_players) < 4:
        raise SystemExit("Need at least 4 active players after a player leaves.")
    state["players"] = remaining_players
    ensure_player_statuses(state)[player] = "left"
    add_event(state, "player_left", player=player, effective_round=len(state["rounds"]) + 1)
    save_state(state, args.state)
    print(f"{player} left. Effective from next generated round.")
    print_schedule(state)


def cmd_pause_player(args):
    state = load_state(args.state)
    require_open_ended(state)
    player = norm_name(args.player)
    if player not in state["players"]:
        raise SystemExit(f"{player} is not active.")
    remaining_players = [p for p in state["players"] if p != player]
    if len(remaining_players) < 4:
        raise SystemExit("Need at least 4 active players after pausing a player.")
    state["players"] = remaining_players
    ensure_player_statuses(state)[player] = "paused"
    add_event(state, "player_paused", player=player, effective_round=len(state["rounds"]) + 1)
    save_state(state, args.state)
    print(f"{player} paused. Effective from next generated round.")
    print_schedule(state)


def cmd_resume_player(args):
    state = load_state(args.state)
    require_open_ended(state)
    player = norm_name(args.player)
    if player in state["players"]:
        raise SystemExit(f"{player} is already active.")
    statuses = ensure_player_statuses(state)
    if statuses.get(player) != "paused":
        raise SystemExit(f"{player} is not paused.")
    state["players"].append(player)
    statuses[player] = "active"
    add_event(state, "player_resumed", player=player, effective_round=len(state["rounds"]) + 1)
    save_state(state, args.state)
    print(f"{player} resumed. Effective from next generated round.")
    print_schedule(state)


def cmd_remove_player(args):
    state = load_state(args.state)
    player = norm_name(args.player)
    if player not in state["players"]:
        raise SystemExit(f"{player} is not in tournament players.")
    remaining_players = [p for p in state["players"] if p != player]
    if len(remaining_players) < 4:
        raise SystemExit("Need at least 4 players after removing a player.")

    for rnd in state["rounds"]:
        if rnd["round"] >= args.from_round:
            for m in rnd["matches"]:
                if m.get("score"):
                    raise SystemExit("Cannot remove a player from a round that already has completed scores. Choose a later round.")

    state["players"] = remaining_players
    if args.seed is not None:
        state["seed"] = args.seed
    ensure_player_statuses(state)[player] = "left"
    state["rounds"] = generate_rounds(
        state["players"],
        state["courts"],
        state["round_count"],
        state["seed"],
        preserve_state=state,
        from_round=args.from_round,
    )
    state.setdefault("player_removals", []).append({
        "player": player,
        "from_round": args.from_round,
        "at": timestamp(),
    })
    save_state(state, args.state)
    print(f"Removed {player} from round {args.from_round}")
    print_schedule(state)


def html_report(state):
    def esc(x): return html.escape(str(x))
    def leaderboard_table(sort_by, title):
        rows = leaderboard(state, sort_by)
        columns = leaderboard_columns(sort_by)
        lb_rows = [
            f"<tr><td>{r['rank']}</td><td>{esc(r['player'])}</td>"
            + "".join(f"<td>{esc(format_leaderboard_value(r, key))}</td>" for _, key in columns)
            + "</tr>"
            for r in rows
        ]
        header = "<tr><th>#</th><th>Player</th>" + "".join(f"<th>{esc(label)}</th>" for label, _ in columns) + "</tr>"
        return f"<h2>{esc(title)}</h2><table><thead>{header}</thead><tbody>{''.join(lb_rows)}</tbody></table>"
    schedule_rows = []
    for rnd in state["rounds"]:
        for m in rnd["matches"]:
            score = "-" if not m.get("score") else f"{m['score'][0]}-{m['score'][1]}"
            schedule_rows.append(
                f"<tr><td>{rnd['round']}</td><td>{m['court']}</td><td>{esc(' / '.join(m['team1']))}</td>"
                f"<td>{esc(' / '.join(m['team2']))}</td><td>{score}</td></tr>"
            )
    leaderboard_sections = "".join([
        leaderboard_table("points", "Americano Leaderboard by Points"),
        leaderboard_table("official", "Alternative Leaderboard by Wins"),
        leaderboard_table("wins", "Leaderboard by Wins"),
        leaderboard_table("points-pct", "Leaderboard by %Points"),
        leaderboard_table("wins-pct", "Leaderboard by %Wins"),
    ])
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>
@page {{ size: A4; margin: 12mm; }}
body {{ font-family: Arial, sans-serif; color: #18232f; font-size: 10pt; }}
h1 {{ margin: 0 0 4px; font-size: 22pt; }}
h2 {{ margin: 16px 0 6px; font-size: 14pt; color: #0f766e; }}
.meta {{ color:#536170; margin-bottom: 10px; }}
table {{ width:100%; border-collapse: collapse; margin-bottom: 10px; }}
th, td {{ border:1px solid #cbd5e1; padding:5px 6px; text-align:left; }}
th {{ background:#e8f7f4; }}
tr:nth-child(even) td {{ background:#f8fafc; }}
</style></head><body>
<h1>{esc(state['name'])}</h1>
<div class='meta'>Players: {esc(', '.join(state['players']))} | Courts: {state['courts']} | Rounds: {state['round_count'] or len(state['rounds'])} | Points/game: {state['points_per_game']}</div>
{leaderboard_sections}
<h2>Schedule & Scores</h2>
<table><thead><tr><th>Round</th><th>Court</th><th>Team 1</th><th>Team 2</th><th>Score</th></tr></thead><tbody>{''.join(schedule_rows)}</tbody></table>
</body></html>"""


def cmd_export_pdf(args):
    state = load_state(args.state)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    html_path = out.with_suffix(".html")
    html_path.write_text(html_report(state), encoding="utf-8")
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print(f"No Chrome/Chromium found. Wrote HTML instead: {html_path}")
        return
    subprocess.run([
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={out}",
        html_path.as_uri(),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Exported {out}")


def build_parser():
    parser = argparse.ArgumentParser(description="Manage Padel Americano schedule, scoring, open-ended sessions, player changes, leaderboard, and PDF export.")
    subcommands = parser.add_subparsers(dest="cmd", required=True)

    new_parser = subcommands.add_parser("new", help="Create a new Americano tournament")
    new_parser.add_argument("--name", default="Padel Americano")
    new_parser.add_argument("--players", required=True, help="Comma-separated player names")
    new_parser.add_argument("--courts", type=int, required=True)
    new_parser.add_argument("--rounds", type=int, required=True)
    new_parser.add_argument("--points", type=int, required=True, help="Total points per game, for example 5 or 21")
    new_parser.add_argument("--seed", type=int, default=42)
    new_parser.add_argument("--out", required=True)
    new_parser.set_defaults(func=cmd_new)

    new_session_parser = subcommands.add_parser("new-session", help="Create an open-ended Americano session without a fixed round count")
    new_session_parser.add_argument("--name", default="Padel Americano")
    new_session_parser.add_argument("--players", required=True, help="Comma-separated player names")
    new_session_parser.add_argument("--courts", type=int, required=True)
    new_session_parser.add_argument("--points", type=int, required=True, help="Total points per game, for example 5 or 21")
    new_session_parser.add_argument("--seed", type=int, default=42)
    new_session_parser.add_argument("--out", required=True)
    new_session_parser.set_defaults(func=cmd_new_session)

    schedule_parser = subcommands.add_parser("schedule", help="Print schedule")
    schedule_parser.add_argument("state")
    schedule_parser.set_defaults(func=cmd_schedule)

    next_round_parser = subcommands.add_parser("next-round", help="Generate the next round for an open-ended session")
    next_round_parser.add_argument("state")
    next_round_parser.add_argument("--force", action="store_true", help="Allow generating even if the current round is not fully scored")
    next_round_parser.add_argument("--seed", type=int)
    next_round_parser.set_defaults(func=cmd_next_round)

    score_parser = subcommands.add_parser("score", help="Record score for a game")
    score_parser.add_argument("state")
    score_parser.add_argument("--round", type=int, required=True)
    score_parser.add_argument("--court", type=int, required=True)
    score_parser.add_argument("--score", required=True, help="Example: 14-10")
    score_parser.set_defaults(func=cmd_score)

    leaderboard_parser = subcommands.add_parser("leaderboard", help="Print leaderboard")
    leaderboard_parser.add_argument("state")
    leaderboard_parser.add_argument("--sort", choices=LEADERBOARD_SORTS, default="points", help="Ranking mode")
    leaderboard_parser.set_defaults(func=cmd_leaderboard)

    switch_parser = subcommands.add_parser("switch", help="Replace a player from a round onward and regenerate future rounds")
    switch_parser.add_argument("state")
    switch_parser.add_argument("--out-player", required=True)
    switch_parser.add_argument("--in-player", required=True)
    switch_parser.add_argument("--from-round", type=int, required=True)
    switch_parser.set_defaults(func=cmd_switch)

    add_player_parser = subcommands.add_parser("add-player", help="Add a new player from a future round and regenerate future rounds with rolling byes")
    add_player_parser.add_argument("state")
    add_player_parser.add_argument("--player", required=True)
    add_player_parser.add_argument("--from-round", type=int, required=True)
    add_player_parser.add_argument("--seed", type=int)
    add_player_parser.set_defaults(func=cmd_add_player)

    remove_player_parser = subcommands.add_parser("remove-player", help="Remove a player from a future round and regenerate future rounds with rolling byes")
    remove_player_parser.add_argument("state")
    remove_player_parser.add_argument("--player", required=True)
    remove_player_parser.add_argument("--from-round", type=int, required=True)
    remove_player_parser.add_argument("--seed", type=int)
    remove_player_parser.set_defaults(func=cmd_remove_player)

    join_player_parser = subcommands.add_parser("join-player", help="Add or reactivate a player for future open-ended rounds")
    join_player_parser.add_argument("state")
    join_player_parser.add_argument("--player", required=True)
    join_player_parser.set_defaults(func=cmd_join_player)

    leave_player_parser = subcommands.add_parser("leave-player", help="Mark an active player as left for future open-ended rounds")
    leave_player_parser.add_argument("state")
    leave_player_parser.add_argument("--player", required=True)
    leave_player_parser.set_defaults(func=cmd_leave_player)

    pause_player_parser = subcommands.add_parser("pause-player", help="Temporarily remove an active player from future open-ended rounds")
    pause_player_parser.add_argument("state")
    pause_player_parser.add_argument("--player", required=True)
    pause_player_parser.set_defaults(func=cmd_pause_player)

    resume_player_parser = subcommands.add_parser("resume-player", help="Resume a paused player for future open-ended rounds")
    resume_player_parser.add_argument("state")
    resume_player_parser.add_argument("--player", required=True)
    resume_player_parser.set_defaults(func=cmd_resume_player)

    export_pdf_parser = subcommands.add_parser("export-pdf", help="Export schedule, scores, and leaderboard to PDF")
    export_pdf_parser.add_argument("state")
    export_pdf_parser.add_argument("--out", required=True)
    export_pdf_parser.set_defaults(func=cmd_export_pdf)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
