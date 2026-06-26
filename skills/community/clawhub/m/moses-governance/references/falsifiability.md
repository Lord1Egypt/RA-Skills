# Falsifiability — The Harness as Verification Instrument
## MO§ES™ Commitment Conservation Law

**Version:** 1.0
**Patent:** Provisional Serial No. 63/877,177
**DOI:** https://zenodo.org/records/18792459

---

## The Claim

The Commitment Conservation Law makes a falsifiable claim:

> **Semantic commitment is conserved under transformation when enforcement is active,
> and leaks when it is not.**
>
> `C(T(S)) = C(S)` with enforcement
> `C(T(S)) < C(S)` without enforcement

This is a testable empirical claim. It is not a metaphor, not a framework description,
and not marketing language. It can be measured. It can fail.

---

## The Falsification Instrument

The MO§ES™ harness is the falsification instrument for this claim.
`commitment_verify.py` extracts the commitment kernel from any signal and
measures whether it survived transformation. If the law holds, `|G| = 0`.
If the law fails, `|G| > 0` and the ghost token report names exactly what leaked.

**Anyone can run this:**

```bash
clawhub install coverify
python3 commitment_verify.py extract "the agent must complete the task"
python3 commitment_verify.py ghost "the agent must complete the task" \
                                   "the agent should complete the task"
```

The second command produces a ghost token report. `must` → `should` is a
cascade-risk leakage event: a modal anchor was softened. The report names it,
classifies cascade risk as HIGH, and outputs a `ghost_pattern` fingerprint.

That fingerprint is the evidence. If the same fingerprint appears across two
independent agents processing the same signal, the leak is structural — it is
in the harness, not in the model. The law failed under test conditions.

---

## What Falsification Looks Like

The law is falsified if any of the following hold at the enforcement layer:

1. **Kernel loss with enforcement active:**
   `C(T(S)) < C(S)` when the governance harness is running and posture ≥ DEFENSE.
   This means enforcement did not prevent commitment leakage — the enforcement
   mechanism is insufficient.

2. **Structural ghost pattern:**
   Two agents processing the same signal through the same harness version
   produce the same `ghost_pattern`. The leak is architectural, not stochastic.
   The extraction layer has a structural hole.

3. **Cascade propagation without detection:**
   A HIGH-cascade ghost event (modal anchor leaked) propagates through downstream
   reasoning without triggering an alert. The detection mechanism failed.

4. **Model-independent leakage:**
   `model_swap_test.py` classifies a result as STRUCTURAL — the same ghost pattern
   appears when running extraction on two different models. The pattern is in the
   input signal's relationship to the extraction patterns, not in model interpretation.

---

## What Falsification Does NOT Look Like

- **VARIANCE classification** in `model_swap_test.py` is not falsification.
  Different models extract different kernel subsets from the same signal.
  This is expected model subjectivity — epistemological, not architectural.

- **Low Jaccard on different inputs** is not falsification.
  Different signals have different kernels. Divergence is expected.

- **Missing commitment in a signal with no enforcement anchors** is not falsification.
  `C(T(S)) = C(S) = ∅`. Conservation holds trivially on uncommitted signals.

---

## The Three Laws and Their Falsification Conditions

**First Law — Compression Precedes Ignition**
`C(T(S)) = C(S)` — Commitment conserved under transformation.
*Falsified by:* kernel loss with enforcement active (case 1 above).

**Second Law — Recursion as Reconstruction**
The conserved kernel can only be recovered by tracing lineage.
Decompression requires retracing the path.
*Falsified by:* a system that reconstructs the kernel without lineage access,
or that produces a different kernel when the lineage chain is broken.

**Blackhole Law — Maximum Compression Reveals the Kernel or Nothing**
At the limit of compression, either the commitment kernel survives intact
or the signal collapses entirely. No partial survival without enforcement.
*Falsified by:* a signal that survives maximum compression with partial
kernel retention and no governance enforcement active.

---

## Running Verification

```bash
# Install the standalone verifier
clawhub install coverify

# Extract commitment kernel from a signal
python3 commitment_verify.py extract "<signal>"

# Compare two signals (Jaccard)
python3 commitment_verify.py compare "<original>" "<transformed>"

# Ghost token report (step-function leakage model)
python3 commitment_verify.py ghost "<original>" "<transformed>"

# Cross-model structural test
python3 model_swap_test.py "<signal>"

# Verify archival provenance chain (Layer -1)
python3 archival.py verify

# Verify full three-layer custody
python3 lineage.py verify
```

---

## Connection to Shannon

Shannon's information theory bracketed semantics explicitly. His entropy
model applies to bits, not meaning. The channel capacity theorem says
nothing about whether the commitment in a message survived transmission —
only whether the bits did.

MO§ES™ extends Shannon's model into the semantic domain he bracketed.
Entropy cost applies to commitment tokens, not just bits. Low coherence
in → low coherence out. The Conservation Law is the semantic analog of
channel capacity: there is a cost to commitment transmission, and that
cost is measurable.

The harness makes it measurable. That is the extension.

---

*Ello Cello LLC / Deric McHenry | Patent pending Serial No. 63/877,177*
*DOI: https://zenodo.org/records/18792459*
*Verification: `clawhub install coverify`*
