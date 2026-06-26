#!/usr/bin/env python3
"""
Proactive v1.0.11 - feedback_update.py
Changelog v1.0.11 (2026-04-05):
 + MIGRATION: SETUP-QUIET schreibt quiet_hours in interests.yaml (nicht mehr proaktiv_state.json)
 + MIGRATION: SETUP-NOGO schreibt no_go_topics in interests.yaml (nicht mehr interest_graph.json)
 + CANDIDATE bleibt in interest_graph.json (Graph-Evolution, kein User-Rohdatum)

Changelog v1.0.10 (2026-03-30):
 + Sensor-Tags: CANDIDATE, GOAL, COMMITMENT, CONTEXT
 + SETUP-QUIET und SETUP-NOGO für Onboarding-Interview (Telegram)
 + Tags werden aus Nachricht extrahiert und in State gespeichert

Changelog v4.0 (2026-03-27):
 + Stress-Tracking: emotional_context in State

Changelog v3.0 (2026-03-26):
 + Positive Reaktion hebt temp_no_go (Dormant-Cooldown) sofort auf
 + Negative Reaktion setzt Topic direkt in temp_no_go
"""

import json, sys, logging, argparse, re, time, os, yaml
from datetime import datetime, timezone, timedelta
import fcntl

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE   = os.path.join(BASE_DIR, "ping_history.json")
GRAPH_FILE     = os.path.join(BASE_DIR, "interest_graph.json")
INTERESTS_FILE = os.path.join(BASE_DIR, "interests.yaml")
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)
LOG_FILE = os.path.join(BASE_DIR, "logs", "proaktiv_cron.log")
LEARNING_RATE       = 0.05
HARD_NEG_COOLDOWN_H = 24

logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger()

# ─── JSON / YAML Helfer ─────────────────────────────────────────────────────

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
        return default.copy()

def save_json(path, data):
    try:
        with open(path, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0); f.truncate()
            json.dump(data, f, indent=2)
            fcntl.flock(f, fcntl.LOCK_UN)
    except FileNotFoundError:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

def load_yaml(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except (FileNotFoundError, yaml.YAMLError):
        return default.copy()

def save_yaml(path, data):
    with open(path, "w") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

# ─── Sentiment Decoder ──────────────────────────────────────────────────────

def decode_sentiment(message: str, reply_delay_minutes: float) -> float:
    msg = message.lower().strip()
    if any(k in msg for k in ["ja", "cool", "geil", "super", "👍", "perfekt",
                               "nice", "danke", "genau", "stimmt", "🔥", "interessant"]):
        delta = +0.15
    elif any(k in msg for k in ["nö", "nee", "egal", "schon wieder", "nerve",
                                "hör auf", "stop", "🙄", "bitte nicht", "zu viel"]):
        delta = -0.25
    elif len(message) < 8:
        delta = -0.05
    elif len(message) > 50:
        delta = +0.10
    else:
        delta = +0.05

    if reply_delay_minutes > 120:
        delta *= 0.5
    elif reply_delay_minutes > 60:
        delta *= 0.75
    return round(delta * LEARNING_RATE, 4)

# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ping_id", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--delay_minutes", type=float, default=0)
    parser.add_argument("--session_id", default=None, help="Active session ID for routing")
    args = parser.parse_args()

    # ─── Session-ID Tracking ─────────────────────────────────────────────────
    active_session = getattr(args, 'session_id', None)
    state_file_path = os.path.join(BASE_DIR, "proaktiv_state.json")
    fb_state = load_json(state_file_path, {})
    if active_session:
        fb_state["active_session_id"] = active_session
        save_json(state_file_path, fb_state)

    # ─── Sensoren auswerten ──────────────────────────────────────────────────
    msg_text  = args.message
    now_iso   = datetime.now(timezone.utc).isoformat()
    state_file = os.path.join(BASE_DIR, "proaktiv_state.json")

    # 1. CANDIDATE (Neues Interesse) → bleibt in interest_graph.json
    cand_match = re.search(r'\[CANDIDATE:\s*(.*?)\]', msg_text, re.IGNORECASE)
    if cand_match:
        candidate  = cand_match.group(1).strip().lower()
        graph      = load_json(GRAPH_FILE, {"interests": {}})
        candidates = graph.setdefault("candidate_topics", {})

        if candidate not in candidates:
            candidates[candidate] = {"mentions": 1, "positive_replies": 1, "last_seen": now_iso}
        else:
            candidates[candidate]["mentions"]        += 1
            candidates[candidate]["positive_replies"] += 1
            candidates[candidate]["last_seen"]         = now_iso

        save_json(GRAPH_FILE, graph)
        msg_text = re.sub(r'\[CANDIDATE:\s*.*?\]', '', msg_text, flags=re.IGNORECASE)

    # 2. GOAL (Ziel mit Deadline)
    goal_match = re.search(r'\[GOAL:\s*(.*?)\s*\|\s*DEADLINE:\s*(.*?)\]', msg_text, re.IGNORECASE)
    if goal_match:
        goal_desc = goal_match.group(1).strip()
        deadline  = goal_match.group(2).strip()
        state     = load_json(state_file, {})
        goals     = state.setdefault("goals", {})

        goal_id          = goal_desc.lower().replace(" ", "_")[:15]
        goals[goal_id]   = {"description": goal_desc, "deadline": deadline, "status": "active"}
        save_json(state_file, state)
        msg_text = re.sub(r'\[GOAL:\s*.*?\]', '', msg_text, flags=re.IGNORECASE)

    # 3. COMMITMENT (Versprechen)
    comm_match = re.search(r'\[COMMITMENT:\s*(.*?)\s*\|\s*WHEN:\s*(.*?)\]', msg_text, re.IGNORECASE)
    if comm_match:
        comm_desc   = comm_match.group(1).strip()
        when        = comm_match.group(2).strip()
        state       = load_json(state_file, {})
        commitments = state.setdefault("commitments", [])

        commitments.append({
            "id": f"comm_{int(time.time())}",
            "content": comm_desc,
            "when": when,
            "status": "pending"
        })
        save_json(state_file, state)
        msg_text = re.sub(r'\[COMMITMENT:\s*.*?\]', '', msg_text, flags=re.IGNORECASE)

    # 4. CONTEXT (Stress & Timing)
    ctx_match = re.search(r'\[CONTEXT:\s*(.*?)\]', msg_text, re.IGNORECASE)
    if ctx_match:
        ctx_type      = ctx_match.group(1).strip()
        state         = load_json(state_file, {})
        cooldown_time = (datetime.now(timezone.utc) + timedelta(hours=4)).isoformat()
        state["current_context"] = {
            "type": ctx_type,
            "detected_at": now_iso,
            "cooldown_until": cooldown_time
        }
        save_json(state_file, state)
        msg_text = re.sub(r'\[CONTEXT:\s*.*?\]', '', msg_text, flags=re.IGNORECASE)

    # 5. SETUP-QUIET → schreibt in interests.yaml (MIGRIERT)
    setup_quiet_match = re.search(r'\[SETUP-QUIET:\s*(\d{1,2})-(\d{1,2})\]', msg_text, re.IGNORECASE)
    if setup_quiet_match:
        start_h       = int(setup_quiet_match.group(1))
        end_h         = int(setup_quiet_match.group(2))
        interests_data = load_yaml(INTERESTS_FILE, {})
        interests_data.setdefault("quiet_hours", {})
        interests_data["quiet_hours"]["start"]      = start_h
        interests_data["quiet_hours"]["end"]        = end_h
        interests_data["quiet_hours"]["end_minute"] = 0
        save_yaml(INTERESTS_FILE, interests_data)
        log.info(f"Onboarding: quiet_hours set to {start_h:02d}-{end_h:02d} in interests.yaml")
        msg_text = re.sub(r'\[SETUP-QUIET:\s*.*?\]', '', msg_text, flags=re.IGNORECASE)

    # 6. SETUP-NOGO → schreibt in interests.yaml (MIGRIERT)
    setup_nogo_match = re.search(r'\[SETUP-NOGO:\s*(.*?)\]', msg_text, re.IGNORECASE)
    if setup_nogo_match:
        nogo_topic     = setup_nogo_match.group(1).strip().lower()
        interests_data = load_yaml(INTERESTS_FILE, {})
        no_go_list     = interests_data.setdefault("no_go_topics", [])
        if nogo_topic not in no_go_list:
            no_go_list.append(nogo_topic)
            save_yaml(INTERESTS_FILE, interests_data)
        log.info(f"Onboarding: no_go_topics += '{nogo_topic}' in interests.yaml")
        msg_text = re.sub(r'\[SETUP-NOGO:\s*.*?\]', '', msg_text, flags=re.IGNORECASE)

    # Tags entfernt — Sentiment nur anhand echtem Text
    args.message = msg_text.strip()

    # ─── Ping aus History holen ──────────────────────────────────────────────
    history = load_json(HISTORY_FILE, {"pings": []})
    ping    = next((p for p in history["pings"] if p["id"] == args.ping_id), None)
    if not ping:
        sys.exit(0)

    topic = ping["topic"]
    delta = decode_sentiment(args.message, args.delay_minutes)
    graph = load_json(GRAPH_FILE, {"interests": {}})

    if topic not in graph.get("interests", {}):
        sys.exit(0)

    # Score updaten
    old_score = graph["interests"][topic]["engagement_score"]
    new_score = round(max(0.0, min(1.0, old_score + delta)), 3)
    graph["interests"][topic]["engagement_score"] = new_score

    # temp_no_go Logik
    now_iso_v2 = datetime.now(timezone.utc).isoformat()
    temp_no_go = graph.setdefault("temp_no_go", {})

    if delta > 0:
        if topic in temp_no_go:
            del temp_no_go[topic]
            log.info(f"Feedback positiv: '{topic}' aus temp_no_go entfernt")
    elif delta <= -0.01:
        if topic not in temp_no_go:
            temp_no_go[topic] = now_iso_v2
            log.info(f"Feedback negativ: '{topic}' → {HARD_NEG_COOLDOWN_H}h Cooldown gesetzt")

        state = load_json(state_file, {})
        state["pending_apology"] = True
        save_json(state_file, state)

    save_json(GRAPH_FILE, graph)

    # Emotional Context & Stress-Tracking
    state            = load_json(state_file, {})
    emotional_context = state.setdefault("emotional_context", {"stress_level": 0})
    current_stress    = emotional_context.get("stress_level", 0)

    if delta < 0 or (len(args.message) < 8 and delta <= 0):
        emotional_context["stress_level"] = min(5, current_stress + 1)
    elif delta > 0:
        emotional_context["stress_level"] = max(0, current_stress - 1)

    state["emotional_context"] = emotional_context
    save_json(state_file, state)

    ping["user_reacted"]    = True
    ping["reaction_type"]   = "positive" if delta > 0 else ("negative" if delta < 0 else "neutral")
    ping["reaction_delta"]  = delta
    save_json(HISTORY_FILE, history)

    log.info(f"Feedback: topic={topic} | score {old_score} → {new_score} | delta={delta}")

if __name__ == "__main__":
    main()
