# OpenClaw NovelAI Free

An intentionally restricted OpenClaw Skill for NovelAI workflows that must stay within **zero NovelAI Image Anlas**.

This variant keeps story writing, prompt planning, account queries, cost estimation, tag suggestions, and local records. It allows a new image only when the active account and the current cost-estimation tool explicitly prove that the exact request costs `0 Anlas`.

It blocks image-to-image, ordinary inpainting, Vibe Transfer, Precise Reference, Director tools, Enhance, dedicated upscaling, batches, and any paid fallback.

After the first successful zero-Anlas verification, the same conversation may reuse the verified billing profile indefinitely while billing-affecting parameters remain unchanged. Transient failures may be retried sequentially up to three times after the initial attempt with identical parameters; billing, account, parameter, and ambiguous processing failures are not retried automatically.

## Important distinction

Zero Anlas is not zero usage:

- Opus V5 free images consume the separate V5 Usage Limit;
- text generation through a third-party OpenClaw provider may have its own price;
- network, hosting, or other model costs are outside this Skill.

## Files

- `SKILL.md` — the enforceable orchestration policy;
- `README.zh-CN.md` — Chinese overview;
- `docs/COSTS-AND-QUOTAS.md` — English cost boundary;
- `docs/费用与额度说明.md` — Chinese cost boundary;
- `LICENSE` — license for standalone distribution.

The advanced Skill remains in the parent project. This variant is a separate package and should not replace it silently.
