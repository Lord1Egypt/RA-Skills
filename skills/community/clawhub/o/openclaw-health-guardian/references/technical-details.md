# Technical Implementation Details

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LaunchAgent (launchd)                     │
│              StartInterval: 300s (5 minutes)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              openclaw-health-check.sh                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Check Status│→ │ Check HTTP  │→ │ Check doctor        │ │
│  │ openclaw    │  │ :18789      │  │ output              │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐  ┌──────────┐  ┌──────────┐
    │ Healthy │  │  Cooldown│  │ Rate     │
    │  Exit 0 │  │  Check   │  │ Limit    │
    └─────────┘  └──────────┘  └──────────┘
                       │             │
                       ▼             ▼
              ┌─────────────────────────┐
              │  Record restart event   │
              │  - last_restart         │
              │  - restart_count        │
              │  - hour_marker          │
              └───────────┬─────────────┘
                          ▼
              ┌─────────────────────────┐
              │  Execute restart        │
              │  - doctor --fix         │
              │  - gateway restart      │
              │  - force start fallback │
              └─────────────────────────┘
```

## State Management

### Files in `~/.openclaw/state/`

| File | Format | Purpose |
|------|--------|---------|
| `last_restart` | Unix timestamp | Last restart time for cooldown |
| `restart_count` | Integer | Current hour restart count |
| `hour_marker` | `YYYYMMDDHH` | Hour marker for counter reset |

### Cooldown Algorithm

```bash
COOLDOWN_SECONDS=180

if [ -f "$LAST_RESTART_FILE" ]; then
    last_restart=$(cat "$LAST_RESTART_FILE")
    now=$(date +%s)
    diff=$((now - last_restart))
    
    if [ $diff -lt $COOLDOWN_SECONDS ]; then
        # In cooldown period, skip restart
        exit 0
    fi
fi
```

### Rate Limit Algorithm

```bash
MAX_RESTARTS_PER_HOUR=5
current_hour=$(date +%Y%m%d%H)

# Reset if hour changed
if [ "$marked_hour" != "$current_hour" ]; then
    restart_count=0
fi

if [ "$restart_count" -ge "$MAX_RESTARTS_PER_HOUR" ]; then
    # Rate limit exceeded, skip restart
    exit 0
fi
```

## Restart Flow

1. **Check cooldown** → Skip if < 180s since last restart
2. **Check rate limit** → Skip if ≥ 5 restarts this hour
3. **Record event** → Update state files
4. **Run doctor --fix** → Attempt automatic repair
5. **Restart gateway** → Normal restart first
6. **Verify HTTP** → Check :18789 responds
7. **Force start** → If normal restart fails
8. **Terminal alert** → If all methods fail

## LaunchAgent Configuration

```xml
<key>StartInterval</key>
<integer>300</integer>

<key>KeepAlive</key>
<dict>
    <key>Crashed</key>
    <true/>
</dict>

<key>ThrottleInterval</key>
<integer>60</integer>
```

- `StartInterval`: Run every 5 minutes
- `KeepAlive.Crashed`: Restart if script crashes
- `ThrottleInterval`: Minimum 60s between runs (safety)

## Platform Compatibility

| Platform | Support | Notes |
|----------|---------|-------|
| macOS 10.14+ | ✅ Full | LaunchAgent native support |
| macOS 10.13 | ⚠️ Partial | May need manual service setup |
| Linux | ❌ No | Use systemd instead |
| Windows | ❌ No | Use Task Scheduler instead |

## Security Considerations

- Scripts run as current user (no sudo required)
- No network access except localhost:18789
- State files stored in user home directory
- Logs may contain system paths (no credentials)
