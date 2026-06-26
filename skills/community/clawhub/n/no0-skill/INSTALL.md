# No.0 Installation Guide

## Prerequisites

- **Core**: Python 3.6+. No other dependencies.
- **DLC**: Python 3.9+, pip, a writable home directory, and a free HTTP port. The installer will `pip install --user` three packages: `PyYAML`, `cryptography`, `keyring`.

macOS / Linux are first-class. Windows support is best-effort for Core (the `.ps1`/`.cmd`/`.bat` dispatchers ship), and partial for the DLC (TOTP Vault keychain integration has some platform-specific code paths).

---

## 1. Install Core

```bash
./install.sh [target_dir]
```

- Default `target_dir`: `~/.openclaw/workspace/skills/no0-skill`
- Copies the top-level dispatcher (`no0`, `no0.command`, `no0.ps1`, `no0.cmd`, `no0.bat`) and the `no0-core/` subtree.
- Creates the shared runtime tree under `~/.openclaw/no0/`:
  - `events/pending/`
  - `events/processed/`
  - `backups/`

Start the guardian:

```bash
cd <target_dir>
./no0 start
./no0 status
```

Expected: `monitor` and `timer` running; six cognitive files marked consistent.

Uninstall = stop, then `rm -rf <target_dir>` and optionally `rm -rf ~/.openclaw/no0/`.

---

## 2. Install the DLC (optional)

```bash
./install-dlc.sh [target_dir]
```

What it does:

1. Detects whether Core is installed at `target_dir`. If yes, event linkage is enabled.
2. Copies `no0-dlc-internal-control/` to `target_dir`.
3. If Core was not detected, also copies the top-level dispatcher so `./no0 <dlc cmd>` still works standalone.
4. Runs `pip install --user -r no0-dlc-internal-control/requirements.txt` (PyYAML, cryptography, keyring).
5. Creates `~/.openclaw/no0/dlc/` and runs `./no0 init` to bootstrap runtime state.
6. Executes one handler sweep (`--once`) to validate wiring end-to-end.

The long-running handler daemon is **not** auto-started. Launch it yourself:

```bash
# Foreground (testing):
python3 no0-dlc-internal-control/event_listener/cognitive_event_handler.py

# Background (macOS/Linux):
nohup python3 no0-dlc-internal-control/event_listener/cognitive_event_handler.py \
  >/tmp/no0-dlc.log 2>&1 &
```

### Standalone DLC install (no Core)

`./install-dlc.sh` runs fine without Core. You lose the cognitive-file-tamper → authorization linkage, but every DLC feature (classification, reference monitor, HTTP auth, audit log, TOTP vault) still works. You can install Core later — re-running `./install-dlc.sh` will detect it and enable linkage.

---

## 3. Verify

```bash
./no0 help                                  # unified help
./no0 status                                # Core status
./no0 classify get ~/.ssh/id_rsa            # DLC classification (expects L6-CRITICAL)
./no0 audit log                             # DLC audit (empty on fresh install)
```

---

## 4. Hourly conditional check (recommended)

```bash
openclaw cron add --name "no0-hourly-check" \
  --schedule '{"kind": "cron", "expr": "0 * * * *"}' \
  --payload '{"kind": "systemEvent", "text": "检查no0-skill状态（条件检查）"}' \
  --sessionTarget main
```

The main agent only speaks when a new anomaly is detected.

---

## 5. Directory layout after install

```
<target_dir>/
├── no0, no0.command, no0.ps1, no0.cmd, no0.bat    # unified dispatcher
├── no0-core/                                      # Core package
│   ├── scripts/                                   # monitor, heartbeat processor, emitter, ...
│   ├── SOUL.md.v1 · USER.md.v1 · ...              # cognitive file baselines
│   └── cognitive_file_backups/                    # versioned backups (created at runtime)
└── no0-dlc-internal-control/                      # (only if DLC installed)
    ├── cli/dlc_cli.py                             # DLC CLI entry
    ├── event_listener/cognitive_event_handler.py  # DLC event consumer
    ├── internal_control/                          # access control, rules, totp_vault, http_auth, ...
    └── requirements.txt

~/.openclaw/no0/
├── events/
│   ├── pending/                                   # Core writes tamper events here
│   └── processed/                                 # DLC archives handled events
├── backups/                                       # Core backups
└── dlc/                                           # (only if DLC installed)
    ├── audit.csv                                  # append-only audit log
    ├── classification.db                          # data classification cache
    ├── http_auth.db                               # pending authorization requests
    └── config.yaml                                # DLC runtime config
```

---

## 6. Platform notes

- **macOS**: works out of the box. Keychain is used for the TOTP vault master key.
- **Linux**: install `python3-keyring` and a Secret Service backend (e.g. `gnome-keyring` or `kwallet`) before `install-dlc.sh`.
- **Windows**: run `.\install.sh` under WSL for Core. DLC has partial Windows support — file an issue if TOTP Vault init fails.

---

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `./no0 <dlc cmd>` says "not installed" | Run `./install-dlc.sh`. |
| `./no0 classify …` says missing `yaml` | `pip install --user -r no0-dlc-internal-control/requirements.txt` |
| `monitor not running` after `./no0 start` | Check `no0-core/cognitive_file_monitor.log`; try `./no0 stop && ./no0 start`. |
| DLC handler not picking up events | Confirm the handler process is running (`ps aux \| grep cognitive_event_handler`). |
| "总是报告不一致" on Core | Stop monitor, `rm -rf no0-core/cognitive_file_backups/*`, restart. |

---

See [README.md](README.md) for the full narrative and [docs/event_schema.md](docs/event_schema.md) for the event protocol.
