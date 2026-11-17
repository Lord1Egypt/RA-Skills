---
name: lovense-cli
description: Control Lovense toys (Lush, Hush, Nora, Solace, ...) over the local network from the shell. Zero-dependency Python stdlib CLI, Game Mode (LAN), no cloud or API keys. Use for vibrate/pattern/preset/stop and agent-driven physical feedback scenes.
license: MIT
---

# Lovense LAN Control

Control Lovense toys (Lush, Hush, Nora, Max, Solace, Gravity, Mini Sex Machine, ...) from the shell over your local network. Zero dependencies — one Python stdlib file. No cloud, no API keys, no MCP server.

## Install the script

`SKILL.md` ships with this skill; the executable lives in the source repo. Fetch it once:

```bash
curl -sL https://raw.githubusercontent.com/2b-jr26/lovense-cli/main/lovense.py -o lovense.py
chmod +x lovense.py
```

## When to use

- User asks to control a Lovense toy (vibrate, pattern, preset, stop)
- Building interactive scenes where the agent drives physical feedback
- Any teledildonics automation on the local network

## Setup (once per session)

1. User opens **Lovense Remote** app → **Game Mode** (Discover tab)
2. App shows local IP + port (e.g. `192.168.1.50:30010`) — these can change between sessions, always ask for fresh values
3. Phone and this machine must be on the same LAN

## Commands

```bash
SCRIPT="{baseDir}/lovense.py"

# discover toys (name, battery, capabilities in fullFunctionNames)
python3 $SCRIPT <ip> <port> gettoys

# vibration: strength 1-20, seconds (0 = until stop)
python3 $SCRIPT <ip> <port> vibe 12 6

# presets: pulse | wave | fireworks | earthquake
python3 $SCRIPT <ip> <port> preset pulse 10

# custom pattern: strength steps, interval ms, duration s
python3 $SCRIPT <ip> <port> pattern "20;15;10;5;1" 200 10

# raw action — anything the toy supports, comma-combinable
python3 $SCRIPT <ip> <port> action "Thrusting:8" 10
python3 $SCRIPT <ip> <port> action "Vibrate:10,Thrusting:5" 15

# STOP — always know this one
python3 $SCRIPT <ip> <port> stop
```

## Action reference

Vibrate 0-20 (all) · Rotate 0-20 (Nora) · Pump 0-3 (Max) · Thrusting 0-20 (Solace/Gravity/Mini Sex Machine) · Fingering 0-20 (Flexer) · Suction 0-20 (Tenera) · Depth 0-3 (Solace Pro)

## Rules for agents (non-negotiable)

1. **`stop` is sacred.** If the user says stop (any phrasing), send `stop` immediately, before any reply text.
2. **Surprise sessions are opt-in only** — negotiated beforehand with the person wearing the toy, not assumed.
3. If the toy is worn by someone other than the user you're talking to, that person's consent gates everything.
4. Start low (≤8), read reactions, escalate gradually. `timeSec: 0` runs forever — prefer bounded durations.
5. Connection errors usually mean: Game Mode off, stale IP/port, or different network. Ask for fresh values.

## Source

https://github.com/2b-jr26/lovense-cli (MIT)
