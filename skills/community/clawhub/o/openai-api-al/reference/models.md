# Reference — Models

OpenAI model families, cost/quality guidance, and which to use per task.

> ⚠️ Always pick the **cheapest model that works**. Escalate only when quality is demonstrably insufficient. Model names and pricing **change** — list current IDs with `openai_models`.

## Text generation (chat / responses)

| Model | Tier | Strengths | Use when |
|-------|------|-----------|----------|
| `gpt-4.1-nano` | nano | Cheapest, fast | Trivial classification, tiny transforms |
| `gpt-4o-mini` | mini (**default**) | Cheap, capable, multimodal | Most chat, summarization, extraction |
| `gpt-4.1-mini` | mini | Cheap, strong general | Default alternative |
| `gpt-4.1` | standard | High quality general | Better writing/analysis |
| `gpt-4o` | standard | Multimodal, strong | Vision + text, quality chat |
| `gpt-5` | frontier | Top capability | Only when nothing cheaper suffices |

## Reasoning models (o-series)

| Model | Tier | Use when |
|-------|------|----------|
| `o4-mini` | reasoning (cheap) | Hard multi-step logic/math at lower cost |
| `o3` | reasoning (premium) | The hardest reasoning tasks |

> Reasoning models consume hidden "thinking" tokens — watch `usage` and set `max_output_tokens`.

## Embeddings

| Model | Dimensions | Use when |
|-------|-----------|----------|
| `text-embedding-3-small` | 1536 | **Default.** RAG/search, cheapest |
| `text-embedding-3-large` | 3072 | When retrieval quality needs the boost |

Supports `dimensions` to truncate output (3-series). Never mix models/dims within one index.

## Images

| Model | Use when |
|-------|----------|
| `gpt-image-1` | Generate images from text |

## Moderation (free)

| Model | Use when |
|-------|----------|
| `omni-moderation-latest` | Screen text/multimodal input & output |

## Audio

| Model | Endpoint | Use when |
|-------|----------|----------|
| `gpt-4o-mini-tts` | `/audio/speech` | Text-to-speech |
| `whisper-1` | `/audio/transcriptions` | Speech-to-text |

## Quick task → model map

| Task | Model |
|------|-------|
| Chat / summarize / extract | `gpt-4o-mini` |
| Trivial classification | `gpt-4.1-nano` |
| Quality writing | `gpt-4.1` / `gpt-4o` |
| Hard reasoning | `o4-mini` → `o3` |
| Embeddings | `text-embedding-3-small` |
| Images | `gpt-image-1` |
| Moderation | `omni-moderation-latest` (free) |
| TTS | `gpt-4o-mini-tts` |
| Transcription | `whisper-1` |

> Verification needed: confirm current model IDs and pricing with <https://platform.openai.com/docs/api-reference>.
