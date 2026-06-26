# Position Tracker — Self-Healing State Management
## Keep track of positions across ANY exchange, broker, or external system. Detect orphans. Prevent leaks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)]()

**Position Tracker is a generalized state machine for tracking positions with self-healing reconciliation against external APIs.**

Originally built for high-frequency crypto trading, now generalized for **any** domain where you need to track external positions that can become orphaned or phantom.

---

## The Problem

You're tracking positions across an external system (exchange, broker, cloud provider, API service). Your local state says you have 3 active positions. The external API says you have 5.

**Which is correct?**

Without reconciliation, you get:
- **Orphans** — positions exist on the exchange but not in your state (leak money/resources)
- **Phantoms** — positions exist in your state but not on the exchange (trigger unnecessary actions)
- **Drift** — state becomes increasingly inconsistent over time

**Manual fixes don't scale.** You need self-healing reconciliation.

---

## The Solution

Position Tracker implements:

### 1. **State Machine** (Position Lifecycle)
Track positions through their full lifecycle:
```
WATCHING → IN → EXITED → cleanup
```

Each state has:
- Entry/exit conditions
- Transition logic
- Timeout handling
- Cleanup rules

### 2. **Orphan Detection**
Detect positions that exist externally but not in your local state:
- Poll external API for all positions
- Compare against local state
- Flag discrepancies above dust threshold
- Self-heal via automatic reconciliation

### 3. **Phantom Cleanup**
Remove local state entries that don't correspond to external reality:
- Detect missing external positions
- Verify before cleanup (avoid race conditions)
- Log cleanup actions for audit trail

### 4. **Dust Filtering**
Ignore sub-threshold positions to prevent noise:
- Set minimum value threshold
- Skip positions below threshold (rewards, rounding errors, etc.)
- Configurable per use case

### 5. **Reconciliation**
Periodic health checks against external API:
- Detect state drift
- Flag inconsistencies
- Auto-correct when safe
- Alert when manual intervention needed

---

## Quick Start (3 Steps)

### 1. Install
```bash
pip install position-tracker
# OR copy position_tracker.py to your project
```

### 2. Implement API Adapter
```python
from position_tracker import PositionTracker, ExternalAPIAdapter

class MyBrokerAdapter(ExternalAPIAdapter):
    def get_all_positions(self):
        """Fetch all positions from your broker/exchange."""
        # Return list of {"id": str, "value": float, "metadata": dict}
        return self.broker_client.get_positions()
    
    def close_position(self, position_id):
        """Close a position on the broker/exchange."""
        return self.broker_client.close(position_id)
```

### 3. Track Positions
```python
tracker = PositionTracker(
    api_adapter=MyBrokerAdapter(),
    min_position_value=5.0,  # Ignore positions < $5
    max_positions=10,         # Safety cap
)

# Track a new position
tracker.track("AAPL-123", metadata={"entry_price": 150.00})

# Update state
tracker.update("AAPL-123", action="ENTER", value=1000.0)

# Check for orphans (self-healing)
orphans = tracker.detect_orphans()
if orphans:
    tracker.cleanup_orphans(orphans)

# Reconcile against external API
tracker.reconcile()
```

**Time to integrate: 20-30 minutes.**

---

## Use Cases

### Crypto/Stock Trading
Track open positions across exchanges. Detect orphaned trades that weren't recorded locally. Prevent position leaks that cost money.

### Cloud Resource Management
Track active cloud instances (AWS EC2, GCP VMs, etc.). Detect orphaned instances that are still billing but not tracked. Auto-cleanup to save costs.

### API Service Quotas
Track active API sessions, subscriptions, or quota allocations. Detect orphaned sessions that consume quota. Cleanup to free resources.

### Database Connection Pools
Track open database connections. Detect orphaned connections that weren't properly closed. Prevent connection leaks.

### Subscription Management
Track active subscriptions across services. Detect orphans (subscriptions you forgot about). Cancel to save money.

**Any domain where external state can diverge from local tracking benefits from this.**

---

## Architecture

### State Machine
```
WATCHING:  Position detected, not yet entered
    ↓ (action=ENTER)
IN:        Active position being tracked
    ↓ (action=EXIT)
EXITED:    Position closed, pending cleanup
    ↓ (timeout)
(deleted)  Cleaned up after timeout
```

### Orphan Detection Flow
```
1. Fetch all positions from external API
2. Compare against local state
3. Flag positions in API but not in state (orphans)
4. Filter by min_position_value (ignore dust)
5. Log orphans for review
6. (Optional) Auto-cleanup via API adapter
```

### Reconciliation Flow
```
1. Periodic poll (e.g., every 5 minutes)
2. Get local IN positions
3. Verify each exists in external API
4. Flag phantoms (local but not external)
5. Flag orphans (external but not local)
6. Auto-correct or alert based on config
```

---

## Configuration

### Basic Config
```python
tracker = PositionTracker(
    api_adapter=adapter,
    state_dir="./state",              # Where to persist state
    min_position_value=5.0,           # Dust threshold ($5)
    max_positions=10,                 # Safety cap
    skip_cleanup_seconds=3600,        # Clean up SKIPPED after 1h
    exited_cleanup_seconds=1800,      # Clean up EXITED after 30m
)
```

### Advanced Config
```python
tracker = PositionTracker(
    # ... basic config ...
    enable_auto_reconcile=True,       # Auto-fix orphans/phantoms
    reconcile_interval=300,           # Reconcile every 5 min
    log_file="./logs/tracker.log",    # Logging
    alert_callback=my_alert_func,     # Custom alerting
)
```

See [config_example.json](./config_example.json) for full options.

---

## API Reference

### Core Methods

#### `track(position_id, metadata=None)`
Start tracking a new position.

**Args:**
- `position_id` (str): Unique identifier
- `metadata` (dict, optional): Additional data to store

**Returns:** PositionState object

---

#### `update(position_id, action, value=0.0)`
Update position state based on action.

**Args:**
- `position_id` (str): Position to update
- `action` (str): One of `ENTER`, `EXIT`, `HOLD`, `MONITOR`, `SKIP`
- `value` (float): Current position value

**Returns:** Updated PositionState object

---

#### `detect_orphans()`
Detect positions on external API that aren't in local state.

**Returns:** List of orphan position dicts `[{"id": str, "value": float, ...}]`

---

#### `cleanup_orphans(orphans, auto_close=False)`
Handle orphaned positions.

**Args:**
- `orphans` (list): List from `detect_orphans()`
- `auto_close` (bool): If True, close orphans via API adapter

**Returns:** List of cleaned up position IDs

---

#### `reconcile()`
Reconcile local state against external API.

**Returns:** Reconciliation report dict with `orphans`, `phantoms`, `corrected`

---

### State Machine Actions

- **`ENTER`** — Enter a position (WATCHING → IN)
- **`EXIT`** — Exit a position (IN → EXITED)
- **`HOLD`** — Hold current position (stay in IN)
- **`MONITOR`** — Continue monitoring (stay in WATCHING)
- **`SKIP`** — Skip this position (WATCHING → SKIPPED)

---

## Error Handling

### Orphan Detection
```python
try:
    orphans = tracker.detect_orphans()
except ExternalAPIError as e:
    logger.error(f"API unreachable: {e}")
    # Fall back to local state only
```

### Reconciliation Failure
```python
report = tracker.reconcile()
if report["errors"]:
    logger.warning(f"Reconciliation errors: {report['errors']}")
    # Manual intervention needed
```

### Position Not Found
```python
state = tracker.get("unknown-id")
if state is None:
    logger.info("Position not tracked")
```

---

## Testing

### Unit Tests
```bash
pytest tests/test_position_tracker.py
```

### Integration Test (Mock API)
```python
from position_tracker import PositionTracker, MockAPIAdapter

adapter = MockAPIAdapter()
adapter.add_position("test-1", value=100.0)

tracker = PositionTracker(adapter)
tracker.track("test-1")
tracker.update("test-1", "ENTER", value=100.0)

# Simulate orphan
adapter.add_position("test-2", value=200.0)
orphans = tracker.detect_orphans()
assert len(orphans) == 1
assert orphans[0]["id"] == "test-2"
```

---

## Limitations

See [LIMITATIONS.md](./LIMITATIONS.md) for details, including:
- API rate limits and polling frequency
- Race conditions during reconciliation
- Dust threshold calibration
- State persistence guarantees

---

## Performance

### Memory
- ~1KB per tracked position
- 1000 positions ≈ 1MB memory
- State file grows linearly with position count

### CPU
- Reconciliation: O(N) where N = position count
- Typical: <10ms for 100 positions

### I/O
- State saves: atomic writes with fsync
- API polls: configurable interval (default 300s)

---

## Troubleshooting

### Problem: Orphans detected every reconciliation cycle
**Cause:** Dust threshold too high, filtering out real positions  
**Fix:** Lower `min_position_value` to match your use case

---

### Problem: State file grows unbounded
**Cause:** Old EXITED positions not cleaning up  
**Fix:** Check `exited_cleanup_seconds` config, ensure timeouts are working

---

### Problem: API adapter errors
**Cause:** External API unreachable or credentials invalid  
**Fix:** Implement retry logic in your adapter, add error handling

---

## Migration Guide

### From Manual Tracking
1. Export current positions to JSON
2. Initialize tracker with `state_file=your_export.json`
3. Run `reconcile()` to validate
4. Switch to tracker for all position updates

### From Custom State Machine
1. Map your states to tracker states (WATCHING/IN/EXITED)
2. Implement API adapter for your external system
3. Run parallel for 1-2 days (log differences)
4. Cut over once validated

---

## Contributing

Position Tracker is **open source** and **community-maintained**.

### Report Issues
- Bugs, edge cases, performance problems
- Integration confusion (docs unclear)
- Feature requests

### Submit Improvements
- Additional API adapter examples
- Performance optimizations
- Test coverage improvements

**Contribution guidelines:** Open an issue or PR on GitHub. We review everything.

---

## Philosophy: Why Open Source?

Position Tracker solves a **universal infrastructure problem** — tracking external state reliably. Hoarding the solution helps no one.

This is a **goodwill project** to:
1. Prove the **vibe coding methodology** (build adaptive systems by feel, not CS theory)
2. Build reputation for future paid Shadow Rose products
3. Improve through community testing and feedback

---

## Support & Community

### Get Help
- 📖 **Documentation:** You're reading it
- 💬 **Discord:** https://discord.com/invite/clawd (OpenClaw community)
- 🐦 **Twitter:** https://x.com/TheShadowyRose
- 🐛 **Issues:** [GitHub link]

### Support Development
Position Tracker is free, but if it saved you time:

☕ **Ko-fi:** https://ko-fi.com/theshadowrose

Donations support ongoing testing, docs, and new features.

---

## License

MIT License — use freely, credit appreciated.

Copyright © 2026 Shadow Rose

See [LICENSE](./LICENSE) for details.

---

## What's Next?

### Planned Features
- **Redis backend** — Distributed state across multiple processes
- **WebSocket support** — Real-time reconciliation instead of polling
- **Advanced alerting** — Slack, PagerDuty, email integrations
- **Dashboard** — Web UI for monitoring positions

**Want to work on these?** Open an issue or reach out on Discord.

---

## Credits

**Created by:** Shadow Rose  
**Extracted from:** Production trading bot (proven in live trading)  
**Philosophy:** Vibe coding — infrastructure that heals itself  
**License:** MIT

Built on lessons learned from a real orphan catastrophe — dozens of positions leaked, manual cleanup required. Never again.

---

## Final Thought

External state will diverge from local state. That's not a bug, it's reality.

The question is: **does your system detect and heal the divergence automatically, or do you find out when the bill arrives?**

Position Tracker ensures you find out **before** the bill arrives.

Ship it. Break it. Tell us what you find.

— Shadow Rose  
February 2026

---

☕ Support: https://ko-fi.com/theshadowrose  
🐦 Follow: https://x.com/TheShadowyRose  
💬 Community: https://discord.com/invite/clawd


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**TRADING DISCLAIMER:** This software is a tool, not a trading system. It does not 
make trading decisions for you and does not guarantee profits. Trading cryptocurrency, 
stocks, or any financial instrument carries significant risk of loss. You can lose 
some or all of your investment. Past performance of any system or methodology is not 
indicative of future results. Never trade with money you cannot afford to lose. 
Consult a qualified financial advisor before making investment decisions.
---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
