# End-to-End Latency Analysis

## Latency Breakdown

```
User speaks                              0s
├─ 小爱 speech recognition           +1-2s
├─ Conversation API update            +0.5s
├─ MiGPT polling detection            +0.5s  (checkInterval=500ms)
├─ "嗯" interrupt TTS via MIoT        +1.5s  (MIoT doAction roundtrip)
│   └─ 小爱 interrupted              ≈3-4s from user speech
├─ LLM API call                       +2-5s  (model dependent)
└─ Response TTS via MIoT              +1.5s  (MIoT doAction roundtrip)
    └─ User hears answer             ≈6-10s from user speech
```

## Optimization Levers

| Lever | Impact | How |
|-------|--------|-----|
| **LLM model choice** | High (2-30s) | Use fastest model; test with `curl` before deploying |
| **checkInterval** | Low (0-0.5s) | 500ms is good; below 500ms has diminishing returns |
| **System prompt length** | Medium (0.5-2s) | Shorter prompt = fewer tokens = faster response |
| **max_tokens** | Low-Medium | Limit response length to reduce generation time |
| **Local LLM (Ollama)** | High | Eliminates network latency; requires GPU |

## LLM Benchmarks (阿里云百炼 Coding Plan)

Tested with simple Chinese Q&A, `max_tokens=30`:

| Model | Latency | Status |
|-------|---------|--------|
| kimi-k2.5 | 2.5s | ✅ Recommended |
| qwen3-coder-plus | 2.8s | ✅ Good |
| MiniMax-M2.5 | 3.2s | ✅ Acceptable |
| glm-4.7 | 5.5s | ⚠️ Slow |
| glm-5 | 6.9s | ❌ Too slow |
| qwen3.5-plus | 30s+ | ❌ Timeout |

## Architectural Limitations

1. **Minimum ~6s latency** — Inherent to the polling architecture (ASR → API → poll → LLM → TTS)
2. **Native 小爱 always speaks first** — Can only be interrupted after detection, not prevented (unless disabled in 小爱 App)
3. **Token expiry** — Injected MIoT tokens expire; requires periodic re-authentication
