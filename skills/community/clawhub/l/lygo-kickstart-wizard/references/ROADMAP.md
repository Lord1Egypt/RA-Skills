# LYGO adoption roadmap (post-Kickstart)

Aligned with ClawHub ecosystem gap analysis (UX · tutorials · proof).

## 1. Immediate — UX Bridge ✅

**Slug:** `lygo-kickstart-wizard`  
**Goal:** Plain-English onboarding + intent routing.  
**Status:** Shipping v1.0.0

## 2. Short-term — Proof layer

**Slug:** `lygo-deception-radar`  
**Goal:** Lightweight public page showing **anonymized** Ops Detector signals on **public** sample sets only (no private mail, no doxing).  
**Outputs:** static/SSR page + optional JSON feed under stack `docs/`.  
**Ethics:** public corpus only; thresholds labeled (operational vs calibration).

## 3. Short-term — Tutorialization

**Slug:** `lygo-mint-walkthrough`  
**Goal:** Interactive step-through of mint → ledger → anchor snippet → optional backfill.  
**Seed:** Kickstart `mint` intent already documents the five steps.

## 4. Medium-term — CLI bridge

**Slug:** `lygo-cli-bridge`  
**Goal:** One entrypoint:

```text
lygo health
lygo analyze --text "..."
lygo mint --pack file.md
lygo map
```

Wraps kickstart + ops-detector + mint-verifier + public gate without exposing internal skill layout.

## Principles (all four)

- Local-first / SkillSpector-safe by default  
- Human remains publisher  
- Star Chart stays the visual index of skills  
- No agent_submission meta hijacking taxonomy  

**Δ9Φ963**
