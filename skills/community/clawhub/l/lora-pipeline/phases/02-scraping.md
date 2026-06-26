# Phase 3 — Dataset Scraping

## Input Contract

- `datasets/face_references/<lora_name>/` exists with 3–6 user-approved reference photos
- Phase 1–2 complete (references verified)

## Output Contract

- `datasets/<lora_name>_raw/` contains 30–80 raw candidate images
- Images sourced from multiple diverse angles/scenarios

## Completion Signal

```
sessions_send(parent_session_id, "✅ Phase 3 complete: <N> raw images collected for <lora_name> in datasets/<lora_name>_raw/. Ready for Phase 4 (verify & clean).")
```

Fallback: write to `~/.openclaw/workspace/lora_status_phase3.txt`

## Model Recommendation

`openrouter/google/gemini-2.0-flash-lite-001` (Worker) — needs browser access, JavaScript execution, and face-feature-guided judgment

---

## Phase 3 — 依照人臉特徵蒐集 Datasets (Scrape Datasets)

Scrape images using the confirmed reference face as a filtering guide. Aim for 30–80 raw candidates (will be trimmed in Phase 4).

### Source Priority

| Source | Method | Notes |
|--------|--------|-------|
| NPC News Online | Replace `/thumb/` → `/large/` in URL | Best quality for competition athletes |
| IMDb | Strip `._V1_...` from image URL | Good for actors/celebrities |
| Instagram mirrors | Imginn / Picuki (bypass login) | SNS lifestyle shots |
| Pinterest | JS eval to filter `736x` URLs | Quick bulk collection |

### Pinterest Browser Snippet
```javascript
const images = Array.from(document.querySelectorAll('img'));
return images.map(img => ({alt: img.alt, src: img.src}))
             .filter(img => img.src.includes('736x'))
             .slice(0, 30);
```

### NPC News High-Res Pattern
```
Thumb: https://npcnewsonline.com/.../thumb/img001.jpg
Large: https://npcnewsonline.com/.../large/img001.jpg
```

### Diversity Targets (collect with variety in mind)
- Competition stage (front/back/side pose)
- Training / gym
- Lifestyle / clothed (target ≥30% of final dataset)
- Different skin tones (competition tan vs. natural)

**Save raw downloads to:** `datasets/<lora_name>_raw/`

---

## Error Escalation

- If sources return no usable images → report to parent session with list of attempted sources
- Do NOT send images to cloud APIs for face matching — use visual judgment only at this stage
- Do NOT upgrade model tier — report to parent if stuck
