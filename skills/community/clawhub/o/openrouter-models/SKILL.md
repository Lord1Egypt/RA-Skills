---
name: openrouter-models
description: 拉取并分析 OpenRouter 模型目录——涵盖 8 项定价（prompt / completion / cache_read / cache_write / web_search / reasoning / image / audio）、上下文长度及输入输出模态（text、image、file、audio、video）。适用于用户询问 OpenRouter 模型对比、"最便宜的支持 X 能力的模型"、"所有 Claude/GPT/Gemini 变体"、免费模型、模型价格对比、模型定价分析等场景。不适用于非 OpenRouter 聚合的通用 LLM 定价问题，也不用于生成或对话任务。
---

# OpenRouter Models Analyzer

Pulls the live model catalog from `https://openrouter.ai/api/v1/models`,
normalizes prices to **$ / 1M tokens**, and lets you filter / sort / compare
models across providers.

## Quick start

```bash
# 1. Fetch the catalog (no API key needed — endpoint is public)
python3 scripts/fetch_models.py
# -> writes models_raw.json next to the script

# 2. Analyze
python3 scripts/analyze.py --family anthropic/
python3 scripts/analyze.py --free --has-image
python3 scripts/analyze.py --has-cache --sort input_cache_read --limit 10
python3 scripts/analyze.py --has-image --min-ctx 1000000 --sort prompt --limit 20
```

The `analyze.py` script does not need network access — it works off the cached
`models_raw.json`. Re-run `fetch_models.py` to refresh.

**Tip:** Always run `fetch_models.py` first to ensure the data is current.

## What you get per model

- `id`, `name`, `context_length`
- `modality` (legacy string) plus `input_modalities` / `output_modalities` lists
- `tokenizer`
- 8 normalized prices in **$ / 1M tokens** (or $ / 1M calls for `web_search`):
  `prompt`, `completion`, `input_cache_read`, `input_cache_write`,
  `web_search`, `internal_reasoning`, `image`, `audio`

See `references/pricing_fields.md` for the full schema and unit gotchas
(notably that `web_search` is per call, not per token, and `-1` means
variable pricing on router models).

## Filter flags

| Flag | Effect |
|---|---|
| `--family PREFIX` | id starts with `PREFIX`, e.g. `anthropic/`, `openai/`, `qwen/` |
| `--keyword K` | case-insensitive substring match on id or name |
| `--min-ctx` / `--max-ctx` | context-length window |
| `--has-image` / `--has-audio` / `--has-video` / `--has-file` | input modality |
| `--outputs-image` | output modality contains `image` |
| `--free` | `prompt == 0 AND completion == 0` |
| `--has-cache` | `input_cache_read` is priced |
| `--has-reasoning-price` | `internal_reasoning` is priced |

## Sort keys

`id` (default), `prompt`, `completion`, `input_cache_read`,
`input_cache_write`, `web_search`, `internal_reasoning`, `ctx`.

Missing values sort to the end regardless of direction.

Use `--desc` to sort in descending order (e.g. most expensive first).

## Output formats

- Default: aligned text table with all 8 pricing columns
- `--json`: structured JSON output (ideal for programmatic consumption)
- `--stats`: print coverage statistics (how many models have each pricing field, modality breakdown)

## Typical analyses

```bash
# Cheapest cache_read among vision-capable 1M-context models
python3 scripts/analyze.py --has-image --min-ctx 1000000 \
    --has-cache --sort input_cache_read --limit 10

# All free models that take image input
python3 scripts/analyze.py --free --has-image

# Most expensive models (per prompt)
python3 scripts/analyze.py --sort prompt --desc --limit 15

# Reasoning-priced models
python3 scripts/analyze.py --has-reasoning-price

# Models with image output (image generators)
python3 scripts/analyze.py --outputs-image

# JSON output for programmatic use
python3 scripts/analyze.py --family anthropic/ --json

# Coverage statistics
python3 scripts/analyze.py --stats
```

## Provider cheat sheet

See `references/model_families.md` for the full list of provider prefixes
and naming conventions (`-thinking`, `-vl`, `:free`, etc.).

Common ones:
- `anthropic/`, `openai/`, `google/`, `x-ai/` — frontier
- `meta-llama/`, `deepseek/`, `qwen/`, `mistralai/`, `nvidia/`, `microsoft/`, `amazon/`
- `openrouter/auto`, `openrouter/fusion` — variable-price routers (`-1`)

## Notes & caveats

- `web_search` is per **call**, not per token — the script displays it as
  $/1M calls (i.e. the value is dollars per 1M invocations).
- `-1` for `prompt` / `completion` means variable pricing (router models).
  The script filters these out of numeric columns and renders `-`.
- Not all models expose every pricing field. Use `--stats` to see current
  coverage for each field.
- `modality` is the legacy compact string; the `input_modalities` /
  `output_modalities` lists are canonical.
- `top_provider.context_length` may be smaller than the model's own
  `context_length` for a specific provider endpoint.
