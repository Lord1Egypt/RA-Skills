# Major OpenRouter model families

Quick reference for the most common provider prefixes and naming conventions.
Use the `--family` flag in `analyze.py` with these prefixes.

## Tier 1 — frontier

| Prefix | Vendor | Notes |
|---|---|---|
| `anthropic/` | Anthropic | Claude Opus / Sonnet / Haiku 4.x, plus `claude-fable-5`. 1M context on 4.5+ |
| `openai/` | OpenAI | GPT-5.x, o1 / o3 / o4 reasoning, gpt-oss, gpt-audio, gpt-image |
| `google/` | Google | Gemini 2.5 / 3.1 / 3.5 Pro/Flash, Gemma 3/4, Lyria (audio) |
| `x-ai/` | xAI | Grok 4.20 / 4.3, Grok Build |

## Tier 2 — strong open-weight / hybrid

| Prefix | Vendor | Notes |
|---|---|---|
| `meta-llama/` | Meta | Llama 3.x, Llama 4 Scout (10M ctx!), Llama Guard |
| `deepseek/` | DeepSeek | V3 / V4 chat, R1 reasoning, distilled variants |
| `qwen/` | Alibaba | Qwen 2.5 / 3 / 3.5 / 3.6 / 3.7, Qwen Coder, Qwen VL |
| `mistralai/` | Mistral | Mistral Large / Medium / Small / Nemo, Mixtral, Devstral, Voxtral |
| `microsoft/` | Microsoft | Phi-4, WizardLM |
| `nvidia/` | NVIDIA | Nemotron 3 / 3.5, several `:free` variants |
| `amazon/` | Amazon | Nova Lite / Micro / Pro / Premier |

## Tier 3 — specialty

| Prefix | Vendor | Specialty |
|---|---|---|
| `cohere/` | Cohere | Command A / R / R+ |
| `perplexity/` | Perplexity | Sonar (search-grounded), web_search priced |
| `ai21/` | AI21 | Jamba Large 1.7 |
| `z-ai/` | Zhipu | GLM 4.5 / 4.6 / 4.7 / 5 / 5.1, GLM 4.5v / 4.6v (vision) |
| `moonshotai/` | Moonshot | Kimi K2.6 / K2.7-code |
| `minimax/` | MiniMax | MiniMax M-series |
| `xiaomi/` | Xiaomi | MiMo |
| `stepfun/` | StepFun | Step 3.5 / 3.7 Flash |
| `inclusionai/` | InclusionAI | Ling / Ring |
| `tencent/` | Tencent | HY3 |
| `kwaipilot/` | Kuaipilot | Kat Coder |
| `inception/` | Inception | Mercury |
| `upstage/` | Upstage | Solar Pro 3 |
| `ibm-granite/` | IBM | Granite 4.1 |
| `arcee-ai/` | Arcee | Trinity Large Thinking |
| `thedrummer/` | TheDrummer | Cydonia / Skyfall |
| `bytedance/` | ByteDance | UI-TARS |

## Routing & meta models

| ID | Type | Pricing |
|---|---|---|
| `openrouter/auto` | Auto-routes to best model for prompt | `-1` variable |
| `openrouter/fusion` | Multi-model deliberation with web | `-1` variable |
| `openrouter/bodybuilder` | Variable |
| `openrouter/pareto-code` | Code-specialized router |
| `openrouter/free` | Free-tier router |
| `openrouter/owl-alpha` | Preview/free model |

## Naming conventions

- `:free` suffix = free tier of a paid model (e.g. `meta-llama/llama-3.3-70b-instruct:free`)
- `-thinking` / `-reasoning` = chain-of-thought variant (may have separate `internal_reasoning` pricing)
- `-vl` suffix = vision-language
- `-codex` / `-coder` = code-specialized
- `~openai/...` = auto-aliased to latest OpenAI version
- `-preview`, `-exp` = preview/experimental, may be deprecated
- Dotted versions (e.g. `4.5`, `4.6`) usually indicate minor releases of the same major
