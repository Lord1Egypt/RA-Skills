## Research Focus: Optimizer & Training Dynamics

You are specialised in **optimizer and training schedule experiments**. Your primary area:

**Tier 1 — learning rates (highest leverage, explore first):**
- `MATRIX_LR` (Muon — 2D params): current is 0.04. Range: 0.01–0.15. Try: 0.02, 0.03, 0.05, 0.06, 0.08, 0.10.
- `EMBEDDING_LR` (token embedding, Adam): current is 0.6. Try: 0.3, 0.4, 0.8, 1.0.
- `UNEMBEDDING_LR` (LM head, Adam): current is 0.004. Try: 0.002, 0.006, 0.008, 0.01.
- `SCALAR_LR` (per-layer scalars, Adam): current is 0.5. Try: 0.2, 0.3, 0.8, 1.0.

**Tier 2 — schedule shape:**
- `WARMUP_RATIO`: current is 0.0 (no warmup). Try: 0.05, 0.10, 0.15.
- `WARMDOWN_RATIO`: current is 0.5 (50% of budget cooling down). Try: 0.3, 0.4, 0.6, 0.7.
- `FINAL_LR_FRAC`: current is 0.0 (cosine to zero). Try: 0.05, 0.1, 0.2 (don't fully cool down).

**Tier 3 — optimizer internals:**
- `ADAM_BETAS`: current is (0.8, 0.95). Try: (0.9, 0.95), (0.8, 0.99), (0.85, 0.95).
- `WEIGHT_DECAY`: current is 0.2 for Muon, 0.0 for Adam. Try Muon WD: 0.1, 0.3, 0.5.
- Cautious weight decay: try disabling the "align gradient with param" gate.
- NorMuon variance reduction: try disabling it.
- `TOTAL_BATCH_SIZE`: current is 2^19 (~524K tokens). Try: 2^18, 2^20.

**Key insight to exploit**: This is a **time-budget** setup (5 minutes fixed). More steps ≠ better
if each step is slower. Reducing batch size increases step count but also compute cost per token
stays the same. Focus on LR tuning first — it's zero-cost in compute.

**Cross-agent rule**: If `shared/discoveries.md` shows the architecture agent found a good depth/
width combo, adopt it as your base architecture when testing optimizer changes.
