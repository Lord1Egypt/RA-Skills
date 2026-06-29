# 📄 `03_cross_harness.py`

**Path:** `/mnt/Morgana/skills/morgana-anti-infinite-loop-v2-en/examples/03_cross_harness.py`  
**Size:** 2,260 bytes / 66 lines  
**Hash:** `802255547a31bca3`  
**Generated:** 2026-06-09T01:00:46.594964+00:00

## 📝 Module Docstring

```
🌀 Example 3: Cross-harness adapters (Claude, OpenAI, LangChain, AutoGen, Hermes, custom).

The guard exposes a uniform interface regardless of the LLM harness you use.
```

## 📦 Imports (2)

```python
import anti_loop.AntiLoop
import anti_loop.adapters.CrossHarnessAdapters
```

## 🏛️ Classes (5)

### `FakeAnthropicResponse`
> Mimics: anthropic.Anthropic().messages.create(...)

### `FakeOpenAIResponse`
> Mimics: openai.OpenAI().chat.completions.create(...)

### `MyCustomResponse`

### `Choice`

### `Message`

## ⚡ Functions (1)

### `def main():`
