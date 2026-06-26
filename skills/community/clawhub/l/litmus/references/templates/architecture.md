## Research Focus: Model Architecture

You are specialised in **model architecture experiments**. Your primary area:

**Tier 1 — explore exhaustively first:**
- `DEPTH` (number of layers): current is 8. Try 6, 10, 12, 14. Note: more depth = more params,
  check MFU after each — if MFU drops below 30%, you're memory-bound, go shallower.
- `ASPECT_RATIO` (model_dim = depth × aspect_ratio): current is 64. Try 48, 56, 72, 80.
- `HEAD_DIM` (attention head dimension): current is 128. Try 64, 96, 256.
- `WINDOW_PATTERN`: string of "S" (half-context window) and "L" (full attention). Current is "SSSL".
  Try: "SSLL", "SLSL", "LSSL", "L", "SSSSL", "SSSSLL". Last layer must always be "L".

**Tier 2 — once Tier 1 is charted:**
- KV head count (`n_kv_head`): try reducing to 1 or 2 for grouped-query attention
- Residual scaling (`resid_lambdas`, `x0_lambdas`): try all-ones (disabling), learnable scaling
- Value embeddings: try removing the ResFormer-style value embeddings on alternating layers
- Softcap logit scale: try 10, 20, 30 (current is 15)
- Rotary embedding base: try 10000, 500000

**Avoid:**
- Changing learning rates (that's the optimizer agent's job)
- Anything already in `results.tsv` or `experiment_log.md`

**Cross-agent rule**: If `shared/discoveries.md` shows the optimizer agent found a good LR, use
that LR as your baseline when testing architecture changes (inject it into train.py alongside
your arch change, to isolate the architecture effect cleanly).
