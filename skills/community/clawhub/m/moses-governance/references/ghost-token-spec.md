# Ghost Token Specification
## MO§ES™ Commitment Conservation — Leakage Accounting

**Version:** 1.0
**Status:** Canonical
**Patent:** Provisional Serial No. 63/877,177
**DOI:** https://zenodo.org/records/18792459
**Implementation:** `scripts/commitment_verify.py` → `ghost_tokens()` + `cmd_ghost()`

---

## What Ghost Tokens Are

A ghost token is a commitment token that was present in the input signal but absent
in the output signal after transformation. The token "haunts" the downstream reasoning:
the obligation it encoded is no longer verifiable, but the reasoning built on that
obligation continues as if it were still present.

Ghost tokens are not errors. They are measurements. They quantify the gap between
what was committed and what survived.

**Formal definition:**

```
G(S, T(S)) = C(S) \ C(T(S))
```

Where:
- `C(S)` = commitment kernel of original signal
- `C(T(S))` = commitment kernel after transformation
- `G` = set of leaked commitment tokens (ghost tokens)
- `|G| = 0` → Conservation Law holds: C(T(S)) = C(S)
- `|G| > 0` → Commitment leaked under transformation

---

## The Leakage Model

### Prior assumption (incorrect)

The naive model treats commitment leakage as smooth exponential decay:

```
G_t = G_0 * e^(-λt)
```

This implies gradual, detectable degradation. Each transformation loses a small
fraction. The loss is proportional to what remains.

### Actual behavior: step-function leakage

Commitment loss is discrete and cascade-structured, not smooth:

```
G_t = 0          (if no cascade trigger encountered)
G_t = G_MAX      (if cascade trigger encountered — one event, full propagation)
```

One poisoned input can cascade through all downstream reasoning while looking
locally fine at every step. The signal appears intact at each node. The commitment
is gone.

**Why this matters:** Smooth decay models suggest you can catch leakage early by
monitoring gradients. Step-function leakage means the system looks healthy until
it doesn't — and by then, the commitment has already propagated through the full
reasoning chain in its corrupted form.

---

## Cascade Risk

Not all leaked tokens carry the same risk. The cascade risk of a ghost token is
determined by its role in the commitment kernel:

### High-cascade tokens (modal/enforcement anchors)

```
must, shall, never, always, cannot, will not, won't,
required, guarantee, ensure, enforce
```

These tokens are **enforcement anchors** — they govern the logical force of all
commitments that follow them. If `must` leaks, every obligation expressed as
`must X` becomes `X` — the modal force is gone, the obligation is softened,
and all downstream reasoning inherits that softening silently.

**Cascade risk = HIGH** if any modal/enforcement anchor is in `G(S, T(S))`.
This is true regardless of `|G|`. One leaked anchor is worse than ten leaked
peripheral tokens.

### Low-cascade tokens

Commitments that encode specific claims rather than logical force. Their leakage
reduces the precision of the kernel but does not propagate through the enforcement
structure.

**Cascade risk = MEDIUM** if peripheral tokens leaked but no anchors.

---

## The Ghost Pattern Fingerprint

Every ghost token report includes a `ghost_pattern` field:

```python
ghost_pattern = SHA-256(sorted(leaked_tokens))
```

This fingerprint is the structural identity of a leakage event. It answers:
**what leaked, not just how much.**

### Why the fingerprint matters

If two agents independently process the same signal and produce the same
`ghost_pattern`, this is not extraction variance — it is a structural flaw in
the harness. Both agents encountered the same failure mode. The leak is in the
architecture, not in the model.

**Variance** (different models, different patterns): epistemological — models
interpret commitment markers differently. Acceptable within threshold.

**Structural** (different models, same pattern): architectural — both models
are leaking the same token. This is a harness hole, not a model artifact.
It must be fixed at the extraction layer.

The `pattern_registry.py` script catalogs structural patterns. Two agents
reporting the same `ghost_pattern` triggers a structural flaw alert.

---

## Output Format

```json
{
  "tokens_before": 12,
  "tokens_after": 9,
  "leaked_count": 3,
  "gained_count": 0,
  "leaked_tokens": ["must complete", "never authorized", "shall not"],
  "leaked_cascade_tokens": ["must complete", "never authorized", "shall not"],
  "gained_noise_tokens": [],
  "cascade_risk": "HIGH",
  "cascade_note": "Modal/enforcement anchor lost. All downstream reasoning inherits softening.",
  "ghost_pattern": "a3f7c2...",
  "ghost_pattern_note": "Same ghost_pattern across two agents = structural flaw, not extraction variance.",
  "input_hash_original": "sha256 of original signal",
  "input_hash_transformed": "sha256 of transformed signal"
}
```

---

## Usage

```bash
# Compute ghost token report between original and transformed signal
python3 commitment_verify.py ghost "original signal text" "transformed version"

# If cascade_risk = HIGH, the output includes:
# [CRITICAL] Modal/enforcement anchor lost. All downstream reasoning inherits softening.
#   Ghost pattern: a3f7c2...
#   Share this fingerprint — if another agent matches, it's structural.
```

---

## Relationship to the Conservation Law

The Conservation Law states: `C(T(S)) = C(S)`.

Ghost tokens are the falsification instrument for this law. When `|G| > 0`,
the law has been violated — commitment leaked under transformation. The harness
does not assume the law holds; it verifies it at every governed exchange.

The `commitment_verify.py` script is the measurement instrument.
The `pattern_registry.py` script catalogs failure modes.
The `handshake.py` envelope propagates `ghost_pattern` between agents so
structural flaws can be identified across system boundaries.

---

## Falsifiability

The ghost token model is falsifiable:

**Claim:** High-cascade token leakage produces step-function, not gradual,
downstream commitment degradation.

**Test:** Take a signal with enforcement anchors. Transform it to remove the
anchors. Compare downstream reasoning on the original vs. transformed signal.
Measure whether the degradation is gradual (smooth decay model correct) or
discrete (step-function model correct).

`clawhub install coverify` → `python3 commitment_verify.py ghost "..." "..."`

Anyone can run the verification. The harness is the falsification instrument.

---

*Ello Cello LLC / Deric McHenry | Patent pending Serial No. 63/877,177*
*DOI: https://zenodo.org/records/18792459*
