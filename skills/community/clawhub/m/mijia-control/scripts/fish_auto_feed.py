#!/usr/bin/env python3
"""
Auto Fish Feeder v2 - polls door lock events and feeds fish once per day.

Flow:
1. OpenClaw cron (every 5min) runs this script
2. Script checks door lock event log for auto-lock events (action=1) today
3. If found and not fed today → feed fish → record state → done
4. If already fed today → skip immediately

Usage:
  python3 fish_auto_feed.py              # Normal run
  python3 fish_auto_feed.py --dry-run    # Check without feeding
  python3 fish_auto_feed.py --force      # Feed regardless of state
  python3 fish_auto_feed.py --status     # Show current state
"""

import sys, os, json, time, datetime
from pathlib import Path

STATE_FILE = Path.home() / ".fish_feed_state.json"
MIJIA_SCRIPT = Path(__file__).parent.parent / "skills" / "mijia-control" / "scripts" / "mijia.py"

# Config
LOCK_DID = "1175215651"          # 智能门锁2 Pro
LOCK_EVENT_KEY = "2.1020"        # Lock Event
FISH_DID = "2026943875"          # 智能鱼缸
FISH_FEED_SIID = 2
FISH_FEED_AIID = 1
FEED_AMOUNT = 1                  # 1-3 portions

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def get_cloud():
    """Import and init micloud from mijia.py."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("mijia_mod", str(MIJIA_SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.get_cloud()

def check_lock_events_today(mc):
    """Check if there's an auto-lock event (leaving home) today."""
    now_ts = int(time.time())
    now_dt = datetime.datetime.now()
    # Cycle starts at 06:00 today, or 06:00 yesterday if before 06:00
    if now_dt.hour < 6:
        cycle_start = (now_dt - datetime.timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
    else:
        cycle_start = now_dt.replace(hour=6, minute=0, second=0, microsecond=0)
    ts_start = int(cycle_start.timestamp())

    params = {"data": json.dumps({
        "did": LOCK_DID,
        "key": LOCK_EVENT_KEY,
        "type": "event",
        "time_start": ts_start,
        "time_end": now_ts,
        "limit": 20
    })}
    r = mc.request_country("/user/get_user_device_data", "cn", params)
    data = json.loads(r if isinstance(r, str) else r.decode())

    events = data.get("result", [])
    for evt in events:
        try:
            props = json.loads(evt["value"])
            prop_map = {p["piid"]: p["value"] for p in props}
            action = prop_map.get(3)   # piid:3 = Lock Action
            # action=1 means Lock (auto-lock after leaving)
            if action == 1:
                evt_time = datetime.datetime.fromtimestamp(evt["time"])
                print(f"[FOUND] Auto-lock event at {evt_time.strftime('%H:%M:%S')}")
                return True
        except:
            continue

    return False

def feed_fish(mc):
    """Trigger fish feeder via miotspec action."""
    params = {"data": json.dumps({"params": {
        "did": FISH_DID,
        "siid": FISH_FEED_SIID,
        "aiid": FISH_FEED_AIID,
        "in": [FEED_AMOUNT]
    }})}
    r = mc.request_country("/miotspec/action", "cn", params)
    data = json.loads(r if isinstance(r, str) else r.decode())
    code = data.get("result", {}).get("code", -1)
    print(f"[INFO] Fish feed API response code: {code}")
    return code in (0, 1)

def main():
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    status = "--status" in sys.argv

    # "Today" runs from 06:00 to next day 06:00
    now = datetime.datetime.now()
    if now.hour < 6:
        feed_day = (now.date() - datetime.timedelta(days=1)).isoformat()
    else:
        feed_day = now.date().isoformat()

    state = load_state()

    if status:
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return

    # Already fed this cycle? Skip entirely.
    if state.get("last_feed_date") == feed_day and not force:
        print(f"[OK] Already fed this cycle ({feed_day}). Done.")
        return

    mc = get_cloud()

    # Check for auto-lock event today
    has_left = check_lock_events_today(mc)
    if not has_left and not force:
        print(f"[OK] No auto-lock event today. BOSS hasn't left home yet.")
        return

    print(f"[TRIGGER] BOSS has left home. Feeding fish...")

    if dry_run:
        print("[DRY-RUN] Would feed fish now. Skipping.")
        return

    success = feed_fish(mc)

    # Record state regardless of success — only attempt once per day
    state["last_feed_date"] = feed_day
    state["last_feed_time"] = datetime.datetime.now().isoformat()
    state["last_feed_success"] = success
    state["total_feeds"] = state.get("total_feeds", 0) + (1 if success else 0)
    save_state(state)

    if success:
        print(f"[DONE] Fed fish. Total feeds: {state['total_feeds']}")
    else:
        print(f"[WARN] Feeding may have failed. Will NOT retry today.")

if __name__ == "__main__":
    main()
