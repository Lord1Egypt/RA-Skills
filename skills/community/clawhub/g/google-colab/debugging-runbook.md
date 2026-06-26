# Debugging Runbook - Google Colab

## Layered Triage Order

1. **Runtime layer**
- runtime disconnected
- package install failures
- import errors

2. **Data layer**
- missing files
- schema mismatch
- null and type coercion issues

3. **Model layer**
- shape mismatches
- unstable training loops
- exploding or vanishing gradients

4. **Evaluation layer**
- metric mismatch
- stale artifacts
- wrong baseline comparisons

## Fast Incident Template

Use this log in `incidents.md`:

- Time:
- Layer:
- Symptom:
- Scope:
- Root cause:
- Fix applied:
- Verification result:

## Recovery Policy

- Prefer smallest possible rollback that restores a known good state.
- Preserve failed artifacts for diagnosis when safe.
- Document the exact fix path so failures are reproducible.
