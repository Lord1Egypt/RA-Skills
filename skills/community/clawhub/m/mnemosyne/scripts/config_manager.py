#!/usr/bin/env python3
import os, json, sys

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config/user_config.json')

DEFAULT_CONFIG = {
    "custom_types": {},
    "auto_trigger": True,
    "tier_rules": {
        "boss_decision": "permanent",
        "boss_preference": "permanent",
        "boss_info": "permanent",
        "work_context": "current",
        "learning": "current",
        "insight": "current",
        "error_recovery": "permanent",
        "default": "current"
    }
}

def load():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save(cfg):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def get_tier(mtype):
    cfg = load()
    return cfg.get("tier_rules", {}).get(mtype, cfg.get("tier_rules", {}).get("default", "current"))

cmd = sys.argv[1] if len(sys.argv) > 1 else "show"

if cmd == "show":
    print(json.dumps(load(), ensure_ascii=False, indent=2))
elif cmd == "get_tier" and len(sys.argv) > 2:
    print(get_tier(sys.argv[2]))
elif cmd == "add_type" and len(sys.argv) > 3:
    cfg = load()
    cfg.setdefault("custom_types", {})[sys.argv[2]] = {"description": sys.argv[3]}
    save(cfg)
    print(f"OK: added {sys.argv[2]}")
elif cmd == "set_tier" and len(sys.argv) > 3:
    cfg = load()
    cfg["tier_rules"][sys.argv[2]] = sys.argv[3]
    save(cfg)
    print(f"OK: {sys.argv[2]} -> {sys.argv[3]}")
else:
    print("Usage: config_manager.py show|get_tier|add_type|set_tier")
