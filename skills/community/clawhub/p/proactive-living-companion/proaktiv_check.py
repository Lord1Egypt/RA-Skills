#!/usr/bin/env python3
"""
Proactive v1.0.39 - proaktiv_check.py
Changelog v1.0.39 (2026-04-05):
 + MIGRATION: get_quiet_hours() liest aus interests.yaml statt aus State
 + MIGRATION: no_go_topics in decide_next_ping() liest aus interests.yaml statt aus Graph
 + State-Key quiet_hours_start/end wird nicht mehr geschrieben/gelesen

Changelog v1.0.38 (2026-04-01):
 + FIX: Quiet Hours jetzt aus State (quiet_hours_start/end) statt Hardcode
 + FIX: stale key daily_budget wird beim Reset entfernt
 + FIX: Topic-Wiederholung — letzten 3 Topics komplett gesperrt
"""

import json, random, logging, sys, os, subprocess, time, uuid, yaml
from pathlib import Path
from pathlib import Path
from datetime import datetime, date, timedelta
import fcntl

SEARCH_REMINDER = "⚠️ SEARCH FIRST: Nutze brave_search oder tavily_search BEVOR du schreibst. Keine Fakten, Versionen, News aus internem Wissen — immer erst suchen."

import importlib.util

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
STATE_FILE     = os.path.join(BASE_DIR, "proaktiv_state.json")
HISTORY_FILE   = os.path.join(BASE_DIR, "ping_history.json")
GRAPH_FILE     = os.path.join(BASE_DIR, "interest_graph.json")
SOCIAL_FILE    = os.path.join(BASE_DIR, "social_knowledge.json")
INTERESTS_FILE = os.path.join(BASE_DIR, "interests.yaml")
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)
LOG_FILE = os.path.join(BASE_DIR, "logs", "proaktiv_cron.log")

_tg = os.environ.get("OPENCLAW_TELEGRAM_NR", "")
if not _tg:
    raise RuntimeError("KRITISCH: OPENCLAW_TELEGRAM_NR nicht gesetzt! Bitte in .env eintragen.")
TELEGRAM_NR = _tg

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Europe/Berlin")
except (ImportError, KeyError):
    from datetime import timezone, timedelta as td
    import time as _t
    _dst = _t.daylight and _t.localtime().tm_isdst
    TZ = timezone(td(hours=2 if _dst else 1))

_spec = importlib.util.spec_from_file_location(
    "interest_evolve", os.path.join(BASE_DIR, "interest_evolve.py")
)
interest_evolve = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(interest_evolve)

MORNING_UNTIL = 10

# ─── JSON / YAML Helfer ─────────────────────────────────────────────────────

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path, "r") as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data = json.load(f)
            fcntl.flock(f, fcntl.LOCK_UN)
        if isinstance(default, dict):
            for k, v in default.items():
                data.setdefault(k, v)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return default.copy() if isinstance(default, dict) else default

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

# ─── Quiet Hours aus interests.yaml (MIGRIERT) ──────────────────────────────

def get_quiet_hours() -> tuple[int, int, int]:
    """Liest Quiet Hours aus interests.yaml. Verarbeitet '22:00' (String) und 22 (Integer)."""
    interests_data = load_yaml(INTERESTS_FILE, {})
    qh = interests_data.get("quiet_hours", {})
    try:
        start_val = qh.get("start", 21)
        end_val = qh.get("end", 8)
        end_min_val = qh.get("end_minute", 0)
        if isinstance(start_val, str) and ":" in start_val:
            q_start = int(start_val.split(":")[0])
        else:
            q_start = int(start_val)
        if isinstance(end_val, str) and ":" in end_val:
            parts = end_val.split(":")
            q_end_h = int(parts[0])
            q_end_m = int(parts[1]) if len(parts) > 1 else 0
        else:
            q_end_h = int(end_val)
            q_end_m = int(end_min_val) if isinstance(end_min_val, int) else 0
    except (ValueError, TypeError):
        q_start, q_end_h, q_end_m = 21, 8, 30
    return q_start, q_end_h, q_end_m

PRESSURE_STEP  = 30
PRESSURE_MAX   = 90
HISTORY_MAX    = 30
IGNORE_THRESHOLD  = 3
IGNORE_COOLDOWN_H = 48
PASSIVE_DECAY_RATE = 0.003

WORK_DAYS       = {0, 1, 2, 3, 4, 5}
WORK_HOUR_START = 8
WORK_HOUR_END   = 17

def is_work_hours(now=None) -> bool:
    if now is None:
        now = datetime.now(TZ)
    return (
        now.weekday() in WORK_DAYS
        and WORK_HOUR_START <= now.hour < WORK_HOUR_END
    )

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger()

def days_since(date_str):
    if not date_str:
        return 999
    try:
        return (date.today() - datetime.fromisoformat(date_str).date()).days
    except ValueError:
        return 999

def get_telegram_session_id() -> str | None:
    """Session-ID aus Umgebungsvariable — kein subprocess, kein Lock-Konflikt."""
    # Option 1: Direkt aus ENV (OpenClaw injiziert das automatisch)
    session_id = (
        os.environ.get("OPENCLAW_SESSION_ID") or
        os.environ.get("CLAW_SESSION") or
        os.environ.get("OPENCLAW_TELEGRAM_SESSION")
    )
    if session_id:
        log.info(f"Session-ID aus ENV: {session_id}")
        return session_id
    # Option 2: Fallback — direkt aus sessions.json lesen (kein CLI-Aufruf)
    sessions_file = Path.home() / ".openclaw/agents/main/sessions/sessions.json"
    try:
        with open(sessions_file) as f:
            sessions = json.load(f)
        for key in sessions:
            if "telegram" in key and "direct" in key:
                log.info(f"Session-ID aus sessions.json: {key}")
                return key
    except Exception as e:
        log.error(f"sessions.json Lesefehler: {e}")
    log.error("Keine Telegram-Session gefunden.")
    return None

def get_last_chat_context() -> str:
    try:
        _state_file = os.path.join(BASE_DIR, "proaktiv_state.json")
        with open(_state_file) as _sf:
            _state = json.load(_sf)
        sid = _state.get("active_session_id", "")
        if not sid:
            _tg = os.environ.get("OPENCLAW_TELEGRAM_NR", "")
            sid = f"agent:main:telegram:direct:{_tg}" if _tg else ""
        if not sid:
            raise RuntimeError("Keine Session-ID verfügbar")
        try:
            res = subprocess.run(
                ["openclaw", "history", "--session-id", sid, "--last", "5", "--json"],
                capture_output=True, text=True, timeout=5
            )
            if res.returncode != 0:
                return ""
            data     = json.loads(res.stdout)
            messages = data.get("messages", [])
        except (subprocess.TimeoutExpired, Exception):
            return "unbekannt"
        user_msgs = [
            m["content"] for m in messages
            if m.get("role") == "user" and m.get("content")
        ]
        if user_msgs:
            last = user_msgs[-1].strip()[:120]
            return last.replace('"', "'").replace("|", "/")
        return ""
    except Exception as e:
        log.warning(f"get_last_chat_context Fehler: {e}")
        return ""

# ─── Passive Decay & Dormant (unverändert) ──────────────────────────────────

def apply_passive_decay(graph: dict, history: dict):
    cutoff = datetime.now(TZ) - timedelta(hours=24)
    ignored_topics: set = set()

    for ping in history.get("pings", []):
        try:
            ts = datetime.fromisoformat(ping["timestamp"])
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=TZ)
        except Exception:
            continue

        if not (ts > cutoff and ping.get("delivered") and not ping.get("user_reacted")):
            continue

        topic = ping.get("topic", "")
        mtype = graph.get("interests", {}).get(topic, {}).get("message_type", "dialog")
        if mtype == "broadcast":
            continue
        if is_work_hours(ts):
            log.info(f"PassiveDecay: '{topic}' übersprungen (Arbeitszeit-Schutz)")
            continue
        ignored_topics.add(topic)

    changed = False
    for topic in ignored_topics:
        if topic in graph.get("interests", {}):
            old = graph["interests"][topic]["engagement_score"]
            new = round(max(0.1, old - PASSIVE_DECAY_RATE), 3)
            if new != old:
                graph["interests"][topic]["engagement_score"] = new
                changed = True
                log.info(f"PassiveDecay: {topic} {old} → {new}")

    if changed:
        save_json(GRAPH_FILE, graph)

def apply_dormant_automatik(graph: dict, history: dict):
    pings = history.get("pings", [])
    now   = datetime.now(TZ)
    topic_stats: dict = {}

    for ping in reversed(pings[-20:]):
        topic = ping.get("topic", "")
        if not topic:
            continue
        mtype = graph.get("interests", {}).get(topic, {}).get("message_type", "dialog")
        if mtype == "broadcast":
            continue
        if topic not in topic_stats:
            topic_stats[topic] = {"consec_ignored": 0, "had_reaction": False}
        if ping.get("user_reacted"):
            topic_stats[topic]["had_reaction"] = True
        elif ping.get("delivered") and not topic_stats[topic]["had_reaction"]:
            try:
                ts = datetime.fromisoformat(ping["timestamp"])
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=TZ)
                if is_work_hours(ts):
                    log.info(f"DormantCheck: '{topic}' ignore in Arbeitszeit – übersprungen")
                    continue
            except Exception:
                pass
            topic_stats[topic]["consec_ignored"] += 1

    temp_no_go = graph.setdefault("temp_no_go", {})
    changed    = False

    for topic, stats in topic_stats.items():
        if stats["consec_ignored"] >= IGNORE_THRESHOLD and not stats["had_reaction"]:
            if topic not in temp_no_go:
                temp_no_go[topic] = now.isoformat()
                log.info(f"DORMANT-AUTOMATIK: '{topic}' → {IGNORE_COOLDOWN_H}h Cooldown")
                changed = True

    for topic in list(temp_no_go.keys()):
        try:
            added_at = datetime.fromisoformat(temp_no_go[topic])
            if added_at.tzinfo is None:
                added_at = added_at.replace(tzinfo=TZ)
        except Exception:
            del temp_no_go[topic]; changed = True; continue
        if (now - added_at).total_seconds() > IGNORE_COOLDOWN_H * 3600:
            log.info(f"DORMANT-AUTOMATIK: '{topic}' reaktiviert")
            del temp_no_go[topic]; changed = True

    if changed:
        save_json(GRAPH_FILE, graph)

# ─── Topic-Selektion — no_go_topics aus interests.yaml (MIGRIERT) ───────────

def decide_next_ping(now):
    graph   = load_json(GRAPH_FILE, {"interests": {}})
    history = load_json(HISTORY_FILE, {"pings": []})
    hour    = now.hour
    recent_topics = [p["topic"] for p in history["pings"][-3:]]

    apply_passive_decay(graph, history)
    apply_dormant_automatik(graph, history)

    temp_no_go     = set(graph.get("temp_no_go", {}).keys())
    # MIGRIERT: no_go_topics aus interests.yaml lesen
    interests_data = load_yaml(INTERESTS_FILE, {})
    no_go          = set(interests_data.get("no_go_topics", []))

    candidates = []
    for topic, data in graph["interests"].items():
        if topic in no_go or topic in temp_no_go:
            log.info(f"decide_next_ping: '{topic}' übersprungen (no_go/temp_no_go)")
            continue

        score = data.get("engagement_score", 0.5)
        if score < 0.2:
            dormant = graph.setdefault("dormant", {})
            if topic not in dormant:
                dormant[topic] = str(date.today())
                save_json(GRAPH_FILE, graph)
            continue

        tw = data.get("time_window", {"from": 9, "to": 22})
        if not (tw["from"] <= hour < tw["to"]):
            continue

        if topic == "f1" and now.weekday() == 6:
            log.info(f"decide_next_ping: f1 übersprungen (Sonntag = Ruhezone)")
            continue

        if topic in recent_topics:
            continue

        priority  = data.get("priority", 5)
        last_date = data.get("last_topic_date") or data.get("last_session", "")
        days_idle = days_since(last_date)
        urgency   = (
            priority * 0.4
            + score * 0.4
            + min(days_idle, 7) / 7 * 0.2 * 10
        )
        candidates.append({"topic": topic, "urgency": round(urgency, 2), "data": data})

    if not candidates:
        return {"topic": "motivation", "urgency": 1, "data": {}}

    candidates.sort(key=lambda x: x["urgency"], reverse=True)
    winner = candidates[0]
    log.info(f"decide_next_ping: {winner['topic']} (urgency={winner['urgency']})")
    return winner

# ─── Trigger aufbauen (unverändert) ─────────────────────────────────────────

def build_trigger(ping: dict, ping_id: str, hours_silent: float = 0.0) -> str:
    topic = ping["topic"].upper()
    data  = ping.get("data", {})
    parts = [f"[SYSTEM-TRIGGER: {topic}"]

    field_map = {
        "last_topic": "last_topic",
        "last_verb": "last_verb",
        "current_project": "project",
        "last_session": "last_session",
    }
    for field, label in field_map.items():
        val = data.get(field)
        if val:
            parts.append(f"{label}={val}")

    score = data.get("engagement_score")
    if score is not None:
        parts.append(f"engagement={score:.0%}")

    mtype = data.get("message_type", "dialog")
    parts.append(f"message_type={mtype}")
    parts.append("search_required=yes")

    if mtype != "broadcast":
        last_chat = get_last_chat_context()
        if last_chat:
            parts.append(f'last_chat="{last_chat}"')
        else:
            parts.append("last_chat=unbekannt")

    if ping["topic"] == "followup":
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        parts.append(f"memory_date={yesterday}")
    if hours_silent > 1:
        parts.append(f"hours_silent={hours_silent:.1f}h")

    state        = load_json(STATE_FILE, {})
    buddy_profile = state.get("buddy_profile", {})
    last_refresh  = buddy_profile.get("last_memory_refresh", "")

    if mtype != "broadcast" and days_since(last_refresh) > 7 and random.random() < 0.15:
        social_db    = load_json(SOCIAL_FILE, {"people": {}})
        people_keys  = list(social_db.get("people", {}).keys())
        if people_keys:
            random_person_key = random.choice(people_keys)
            person_data       = social_db["people"][random_person_key]
            facts             = person_data.get("key_facts", [])
            if facts:
                random_fact = random.choice(facts)
                fact_name   = random_fact.get("fact", "unbekannt")
                fact_value  = random_fact.get("value", "unbekannt")
                parts.append(f'buddy_intent="memory_refresh"')
                parts.append(f'memory_refresh_fact="{random_person_key}:{fact_name}:{fact_value}"')
                buddy_profile["last_memory_refresh"] = str(date.today())
                state["buddy_profile"] = buddy_profile
                save_json(STATE_FILE, state)

    emotional_context    = state.get("emotional_context", {"stress_level": 0})
    stress_level         = emotional_context.get("stress_level", 0)
    humor_allowed_topics = ["suno", "f1", "ki_news"]

    if stress_level <= 1 and topic.lower() in humor_allowed_topics:
        parts.append('humor_hint="subtle"')
    elif stress_level >= 3 and mtype != "broadcast":
        parts.append('buddy_intent="wellness"')

    current_score = data.get("engagement_score", 0.5)
    if current_score > 0.65:
        parts.append('disclosure_level="deep"')
    else:
        parts.append('disclosure_level="basic"')

    now_ambient = datetime.now(TZ)
    if now_ambient.weekday() >= 5:
        parts.append('ambient_context="weekend"')
    elif now_ambient.hour >= 18:
        parts.append('ambient_context="evening_chill"')
    else:
        parts.append('ambient_context="workday"')

    parts.append(f"ping_id={ping_id}")
    return " | ".join(parts) + "]"

# ─── Session Lookup & Trigger Injection (unverändert) ────────────────────────

def get_latest_telegram_session() -> tuple:
    """Session-UUID + Telegram-NR — direkt aus sessions.json, kein subprocess, kein Lock."""
    tg_nr = os.environ.get("OPENCLAW_TELEGRAM_NR", "")
    if not tg_nr:
        log.error("OPENCLAW_TELEGRAM_NR nicht gesetzt.")
        return None, None

    sessions_file = Path.home() / ".openclaw/agents/main/sessions/sessions.json"
    try:
        with open(sessions_file) as f:
            data = json.load(f)
        target_key = f"agent:main:telegram:direct:{tg_nr}"
        val = data.get(target_key)
        if val:
            session_uuid = val.get("sessionId") or val.get("id") or target_key
            log.info(f"Session gefunden: {session_uuid[:32]}...")
            return session_uuid, tg_nr
        print("[WARN] Keine Telegram-Session gefunden.")
    except Exception as e:
        log.error(f"sessions.json Lesefehler: {e}")
        print(f"[ERROR] Exception beim Session-Lookup: {e}")

    return None, None

def inject_trigger(trigger_text: str) -> bool:
    session_uuid, tg_nr = get_latest_telegram_session()
    if not session_uuid or not tg_nr:
        print("[ERROR] Keine Telegram-Session gefunden.")
        log.error("Trigger-Injection fehlgeschlagen.")
        return False

    cmd = [
        "openclaw", "agent",
        "--session-id", session_uuid,
        "--message", trigger_text,
        "--deliver",
        "--reply-channel", "telegram",
        "--reply-to", tg_nr
    ]
    log.info(f"inject_trigger: UUID={session_uuid[:16]}...")
    try:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True
        )
        print(f"[INFO] Trigger async injiziert für User: {tg_nr}")
        log.info("Trigger async injiziert (non-blocking)")
        return True
    except Exception as e:
        print(f"[ERROR] Popen fehlgeschlagen: {e}")
        log.error(f"inject_trigger Popen Fehler: {e}")
        return False

# ─── Main Loop ─────────────────────────────────────────────────────────────────

DEFAULT_STATE = {
    "ping_pressure": 0,
    "daily_budget_used": 0,
    "last_morning_ping_date": "",
    "last_budget_reset_date": "",
    "last_evolve_date": "",
    "last_run_date": "",
    "last_user_message_ts": 0,
    "active_session_id": "",
}

def main():
    now   = datetime.now(TZ)
    today = str(date.today())
    hour  = now.hour
    minute = now.minute

    DAILY_BUDGET = 10 if now.weekday() >= 5 else 8
    log.info(f"=== Proaktiv-Check v1.0.39 | {now.strftime('%Y-%m-%d %H:%M')} CET ===")

    state = load_json(STATE_FILE, DEFAULT_STATE)

    # Täglicher Gärtner (Interest Evolution)
    today_str = str(now.date())
    if state.get("last_evolve_date") != today_str:
        log.info("Neuer Tag erkannt: Führe Interest Evolution aus...")
        try:
            interest_evolve.main()
        except Exception as e:
            log.error(f"Fehler bei interest_evolve: {e}")
        state = load_json(STATE_FILE, DEFAULT_STATE)
        state["last_evolve_date"] = today_str
        save_json(STATE_FILE, state)
        log.info("Interest Evolution abgeschlossen.")

    # Tages-Budget-Reset
    if state["last_budget_reset_date"] != today:
        state["daily_budget_used"]    = 0
        state["last_budget_reset_date"] = today
        if "daily_budget" in state:
            del state["daily_budget"]
        log.info("Budget zurückgesetzt.")

    if state["daily_budget_used"] >= DAILY_BUDGET:
        log.info("Budget erschöpft.")
        save_json(STATE_FILE, state)
        sys.exit(0)

    # Quiet Hours — aus interests.yaml (MIGRIERT)
    q_start, q_end_h, q_end_m = get_quiet_hours()
    in_quiet = (
        hour >= q_start
        or hour < q_end_h
        or (hour == q_end_h and minute < q_end_m)
    )
    if in_quiet:
        # Quiet Hours: Skip proactive pings, but log status
        log.info(f"Quiet Hours aktiv ({q_start}:00-{q_end_h}:{q_end_m:02d}). Kein Ping.")
        sys.exit(0)

    # Morgen-Garantie
    after_quiet = hour > q_end_h or (hour == q_end_h and minute >= q_end_m)
    in_morning  = after_quiet and hour < MORNING_UNTIL
    morning_done = state["last_morning_ping_date"] == today

    if in_morning and not morning_done:
        log.info("Morgen-Garantie.")
        last_chat = get_last_chat_context()
        ctx_part  = f' | last_chat="{last_chat}"' if last_chat else ""
        ping_id   = str(uuid.uuid4())[:8]
        trigger   = f"[SYSTEM-TRIGGER: MORGEN-BRIEFING{ctx_part} | ping_id={ping_id}]"
        state["ping_pressure"]          = 0
        state["last_morning_ping_date"] = today
        state["daily_budget_used"]     += 1
        save_json(STATE_FILE, state)
        if not inject_trigger(trigger):
            log.error("KRITISCH: Morgen-Briefing fehlgeschlagen!")
        sys.exit(0)

    # Druckkessel
    pressure = state["ping_pressure"]
    roll     = random.randint(0, 100)
    log.info(f"Druckkessel | pressure={pressure}% | roll={roll}")

    if roll > pressure:
        state["ping_pressure"] = min(PRESSURE_MAX, pressure + PRESSURE_STEP)
        log.info(f"Fail → Druck {state['ping_pressure']}%.")
        save_json(STATE_FILE, state)
        sys.exit(0)

    # Silence-Breaker
    last_ts      = state.get("last_user_message_ts", 0)
    hours_silent = (now.timestamp() - last_ts) / 3600 if last_ts > 0 else 0.0

    # ─── COMPANION LAYER ──────────────────────────────────────────────────────
    ping_id        = str(uuid.uuid4())[:8]
    special_trigger = None
    companion_topic = "companion"
    state           = load_json(STATE_FILE, {})
    now_date_str    = str(now.date())

    # 1. Adaptive Apology
    if state.get("pending_apology"):
        special_trigger = f"[SYSTEM-TRIGGER: APOLOGY | buddy_intent=apologize_and_adjust | ping_id={ping_id}]"
        state["pending_apology"] = None
        companion_topic = "apology"

    # 2. Commitment Follow-up
    elif "commitments" in state:
        for c in state["commitments"]:
            if c.get("status") == "pending":
                special_trigger = f"[SYSTEM-TRIGGER: COMMITMENT_FOLLOWUP | content=\"{c['content']}\" | buddy_intent=followup_commitment | ping_id={ping_id}]"
                c["status"]     = "done"
                companion_topic = "commitment"
                break

    # 3. Goal Check-in
    elif not special_trigger and "goals" in state:
        for g_id, g in state["goals"].items():
            if g.get("status") == "active" and g.get("next_checkin") == now_date_str:
                special_trigger = f"[SYSTEM-TRIGGER: GOAL_CHECKIN | goal=\"{g['description']}\" | deadline=\"{g['deadline']}\" | buddy_intent=goal_checkin | ping_id={ping_id}]"
                g["next_checkin"] = None
                companion_topic   = "goal"
                break

    # 4. Topic Promotion
    elif not special_trigger and state.get("pending_promotion"):
        promo           = state["pending_promotion"]
        special_trigger = f"{promo['trigger']} | ping_id={ping_id}]"
        companion_topic = promo["topic"]
        state["pending_promotion"] = None

    # Entscheidung
    if special_trigger:
        trigger = special_trigger.replace("] |", " |")
        ping    = {"topic": companion_topic, "urgency": 6.0}
        save_json(STATE_FILE, state)
        log.info(f"Companion Layer aktiv: {companion_topic}")
    else:
        ping    = decide_next_ping(now)
        trigger = build_trigger(ping, ping_id, hours_silent=hours_silent)

        # 5. Serendipity Engine (10%)
        if random.random() < 0.10:
            trigger = trigger.replace("]", " | buddy_intent=serendipity]")
            log.info("Serendipity Engine getriggert!")

    state["ping_pressure"]     = 0
    state["daily_budget_used"] += 1
    save_json(STATE_FILE, state)

    # Ping in History
    history = load_json(HISTORY_FILE, {"pings": []})
    history["pings"].append({
        "id": ping_id,
        "timestamp": now.isoformat(),
        "topic": ping["topic"],
        "urgency": ping["urgency"],
        "delivered": False,
        "user_reacted": False,
        "reaction_type": None,
        "reaction_delta": None,
    })
    history["pings"] = history["pings"][-HISTORY_MAX:]
    save_json(HISTORY_FILE, history)

    log.info(f"→ {trigger[:120]} | Budget: {state['daily_budget_used']}/{DAILY_BUDGET}")

    if inject_trigger(trigger):
        history["pings"][-1]["delivered"] = True
        save_json(HISTORY_FILE, history)
    else:
        log.error("Trigger-Injection fehlgeschlagen. Breche ab (Strict Silence).")

    state["last_run_date"] = today
    save_json(STATE_FILE, state)

if __name__ == "__main__":
    main()
