# No.0 Quickstart

## Install Core (3 steps)

```bash
./install.sh
cd ~/.openclaw/workspace/skills/no0-skill
./no0 start
```

Verify:

```bash
./no0 status
```

You should see `monitor` and `timer` running and all six cognitive files reported as *consistent*.

## Add the DLC (optional)

```bash
./install-dlc.sh
```

Run the event handler in the background:

```bash
nohup python3 no0-dlc-internal-control/event_listener/cognitive_event_handler.py \
  >/tmp/no0-dlc.log 2>&1 &
```

## 30-second smoke test (Core)

```bash
# 1. Modify a cognitive file
echo "# test change" >> ~/.openclaw/workspace/MEMORY.md

# 2. Wait one poll cycle
sleep 35

# 3. See the event
./no0 log --last 1

# 4. Roll back
./no0 rollback MEMORY.md v1
```

## 30-second smoke test (DLC)

```bash
./no0 classify get ~/.ssh/id_rsa       # L6-CRITICAL
./no0 classify get ~/Desktop           # classification or "excluded"
./no0 audit log                        # empty on a fresh install
```

## Linked-flow smoke test (Core + DLC)

```bash
# Trigger a Level-5 tamper on SOUL.md (requires running monitor)
python3 no0-core/scripts/tamper_simulator.py --file SOUL.md --severity 5

# Within seconds, the event appears in pending/
ls ~/.openclaw/no0/events/pending/

# The handler sweeps it and records an audit row
./no0 audit log --last 1
```

## Useful commands

```bash
./no0 status                       # guardian + consistency report
./no0 log --last 5                 # recent changes
./no0 versions MEMORY.md           # history
./no0 diff MEMORY.md v2            # compare v2 to current
./no0 rollback MEMORY.md v2        # restore
./no0 stop                         # stop the monitor

./no0 classify get <path>          # DLC: classify a file
./no0 classify dir <path> -r       # DLC: classify a tree
./no0 audit log [--last N]         # DLC: read the audit log
```

## Hourly conditional check (recommended)

```bash
openclaw cron add --name "no0-hourly-check" \
  --schedule '{"kind": "cron", "expr": "0 * * * *"}' \
  --payload '{"kind": "systemEvent", "text": "检查no0-skill状态（条件检查）"}' \
  --sessionTarget main
```

The main agent will only notify you when a new anomaly is detected — silent otherwise.

## Troubleshooting

- **`./no0 <dlc cmd>` says "not installed"**: run `./install-dlc.sh`.
- **`./no0 classify …` says "missing yaml"**: `pip install -r no0-dlc-internal-control/requirements.txt`.
- **Monitor not running**: `ps aux | grep skill_launcher`; check `no0-core/cognitive_file_monitor.log`.
- **"总是报告不一致"**: stop monitor, `rm -rf no0-core/cognitive_file_backups/*`, start again.

See [README.md](README.md) for full narrative and [docs/event_schema.md](docs/event_schema.md) for the event protocol.
