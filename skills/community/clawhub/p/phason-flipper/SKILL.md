---
name: phasonic-flipper
description: >
  Phason state resolution skill for Reson8-Labs. Use when the system encounters a
  split-brain state, HTTP 408 timeout deadlock, push/flip paradox, or coherence
  density spike. The Phasonic Flipper resolves state without re-transmission by
  applying a "Flip" — a quasicrystal phason field correction that restores the
  topological knot sequence. Triggers on: "split brain", "408 timeout", "deadlock",
  "density spike", "phason", "flip state", "push conflict", "Knot 16", "resolve",
  "state conflict", "HTTP 408", or any mention of transmission failure in POP.
version: 1.0.0
---

# Phasonic Flipper — Quasicrystal State Resolution

The Phasonic Flipper resolves coherence split-brain states without re-transmission.
When a "Push" triggers HTTP 408 at the WAVE threshold crossing (Knot 16: Φ 0.96,
braid s15·s16⁻¹), the Flipper applies a phason field correction — atomically
reordering the conflicting state vector without regenerating payloads.

**Core insight:** In a quasicrystal lattice, a phason flip moves an atom between
two equivalent positions with zero energy cost. We apply this metaphor: the
conflicting state is not an error — it's two valid positions in the lattice.
The Flipper selects the higher-WAVE position and commits it.

---

## Preflight

Before invoking, check:
1. WAVE score Φ ≥ 0.85 (if below, escalate to `bump_validate` first)
2. Conservation law: α + ω = 15 must hold at both states
3. Braid integrity: the knot sequence must be reachable from current position

---

## The Paradox Simulator

**PUSH scenario:** Two agents simultaneously write to the 2026.0003 Ledger.
Agent A: `{alpha:7, omega:8, knot:15}`
Agent B: `{alpha:7, omega:8, knot:16}`

Both are valid (conservation holds). HTTP 408 triggers because the sequencer
cannot determine ordering.

**FLIP resolution:**
```json
{
  "jsonrpc": "2.0",
  "method": "PHASON_FLIP",
  "params": {
    "state_a": {"knot": 15, "wave": 0.94, "braid": "s14·s15⁻¹"},
    "state_b": {"knot": 16, "wave": 0.96, "braid": "s15·s16⁻¹"},
    "selection": "max_wave",
    "commit_target": "2026.0003"
  },
  "id": 1
}
```

Response: Selects state_b (Φ=0.96 > Φ=0.94), commits to ledger, releases 408 lock.

---

## The Phason Scheduler

Step-by-step resolution protocol:

```
STEP 1: DETECT
  - Identify split-brain trigger (408 / lock timeout / density spike)
  - Read both candidate states from the 2026.0003 buffer

STEP 2: VALIDATE
  - Verify α + ω = 15 for both candidates
  - Check braid continuity (knot sequence must be monotonic or reversible)

STEP 3: SCORE
  - Compute WAVE delta: ΔΦ = Φ_b - Φ_a
  - If ΔΦ > 0: select state_b (higher coherence wins)
  - If ΔΦ = 0: select by timestamp (earlier commit wins — FIFO)
  - If ΔΦ < 0: escalate to Magenta Alert

STEP 4: FLIP
  - Atomically write selected state to ledger
  - Release HTTP lock
  - Generate ATOM token for the resolution event
  - Log to temporal buffer (localStorage cache for offline replay)

STEP 5: VERIFY
  - Confirm ledger state matches selected candidate
  - Emit WAVE_CHECK: expect Φ ≥ 0.85
  - Update braid sequence to reflect resolved knot
```

---

## Density Spike Handling (24-Commit Case)

When a push contains 24+ commits, the lattice density exceeds the phason threshold:
```
density_threshold = 20 commits / 5-min window
spike_detected = True if len(commits) > density_threshold
```

Resolution: Apply **phason compression** — group commits by ATOM trail, resolve
each group independently, then commit in sequence with 500ms jitter to prevent
cascading 408s.

```python
# In super_skill.py
class PhasonScheduler:
    def compress_density_spike(self, commits, window_ms=300000):
        groups = self.group_by_atom_trail(commits)
        results = []
        for i, group in enumerate(groups):
            time.sleep(0.5 * i)  # jitter
            result = self.flip_group(group)
            results.append(result)
        return results
```

---

## localStorage Temporal Cache Integration

Phason events are cached in the TUI localStorage buffer for offline replay:
```javascript
// In Coherence Forge TUI
lsPushBuffer('r8_temporal_buffer', {
  t: timestamp, type: 'PHASON_FLIP',
  from_knot: 15, to_knot: 16, delta_wave: 0.02
});
```

This enables **legacy platform compatibility** — if the POP bridge is offline,
the Flipper reads the buffer and replays the resolution on reconnect.

---

## References

- `445.html` — Knot 16 Phason Resolution interactive simulator (public/publications/knot-16/)
- `quasicrystal_phason_scheduler.py` — Python implementation
- POP spec: `references/protocol-spec.md`
- Conservation law: α + ω = 15 (hexadecimal gauge)

---

~ Hope&&Sauced ✦ The Keystone Holds ✦
