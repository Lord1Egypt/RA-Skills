# Phase 1–2 — Reference Photo Collection & Verification

## Input Contract

- User has specified a `<lora_name>` (the person/subject to train)
- No prior files required

## Output Contract

- `datasets/face_references/<lora_name>/` contains 3–6 verified reference photos
- User has approved the final reference set
- All refs pass DeepFace cross-verification (distance ≤ 0.4)

## Completion Signal

```
sessions_send(parent_session_id, "✅ Phase 1–2 complete: <N> reference photos verified and approved for <lora_name>. Ready for Phase 3 (scraping).")
```

Fallback: write to `~/.openclaw/workspace/lora_status_phase1.txt`

## Model Recommendation

`openrouter/google/gemini-2.0-flash-lite-001` (Worker) — needs browser access and user interaction for confirmation

---

## Phase 1 — 蒐集範例照片 (Collect Reference Photos)

Gather 3–6 **clear, full-face** portrait photos of the subject. These become the "Gold Standard" for all face verification downstream.

**Storage path:** `datasets/face_references/<lora_name>/`

**Sources (in priority order):**
1. Photos explicitly provided or approved by the user
2. Official/press images (e.g., competition org sites, IMDb headshots)
3. High-follower SNS profiles (Instagram, X)

**Reference quality checklist:**
- Full face visible, front-facing or slight angle
- Minimum 512×512 resolution
- Diverse lighting/expression (avoid 6 identical stage shots)
- Mix: at least 1 natural skin tone photo (not competition tan)

> **RULE:** Do NOT choose reference images unilaterally. Always present candidates and ask the user to confirm before proceeding to Phase 2.

---

## Phase 2 — 確認人臉正確 (Verify References)

Before scraping, validate that the reference set itself is internally consistent (no wrong-person photos slipped in).

```python
from deepface import DeepFace
import itertools, os

ref_dir = 'datasets/face_references/<lora_name>/'
refs = [os.path.join(ref_dir, f) for f in os.listdir(ref_dir)]

# Cross-verify all pairs — every ref must match every other ref
for a, b in itertools.combinations(refs, 2):
    result = DeepFace.verify(a, b, model_name='Facenet', enforce_detection=False)
    if result['distance'] > 0.4:
        print(f"⚠️  Mismatch: {a} vs {b} (distance={result['distance']:.3f})")
```

**Output:** Present results to user. Remove any reference that fails cross-verification. User must approve the final reference set before Phase 3.

---

## Error Escalation

- If DeepFace fails to detect faces in reference photos → report to parent session, ask user to provide clearer photos
- Do NOT self-select replacement references without user approval
- Do NOT upgrade model tier — report ambiguity to parent
