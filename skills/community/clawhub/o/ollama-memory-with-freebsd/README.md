# 🧠 OpenClaw Local Semantic Memory (Ollama)

[![ClawHub Skill](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.ai/djc00p/openclaw-ollama-memory) [![Agent Skill](https://img.shields.io/badge/Agent-Skill-blue)](#) [![Agent Memory](https://img.shields.io/badge/Agent-Memory-green)](#)

**Zero-cost, fully private, and offline-capable semantic search for OpenClaw.**

Traditional AI agents rely on cloud-based embedding APIs (like OpenAI or Google Gemini) to perform semantic searches through their memory. While powerful, these services introduce **latency, recurring costs, and privacy concerns** (sending your data to third-party servers).

The **OpenClaw Ollama Integration** replaces these cloud dependencies with a local, high-performance embedding pipeline. By leveraging **Ollama** and the **`nomic-embed-text`** model, you can transform OpenClaw into a completely private, offline-capable intelligence engine that runs entirely on your own hardware.

---

## 🏗 Architecture Overview

The data flow moves from your local files into a searchable vector space hosted by your local machine:

`[OpenClaw Episodic Memory] ➔ [Ollama (nomic-embed-text)] ➔ [Local Vector Search]`

| Feature | Cloud Embeddings (OpenAI/Gemini) | Local Embeddings (Ollama) |
| :--- | :--- | :--- |
| **Cost** | Per-token usage fees | **Free** (Hardware only) |
| **Privacy** | Data leaves your infrastructure | **100% Private** (Data stays local) |
| **Connectivity** | Requires Internet | **Fully Offline** |
| **Latency** | Network-dependent | **Low** (Local throughput) |

---

## 🚀 Implementation Guide

### 1. Prepare the Embedding Engine

First, ensure [Ollama](https://ollama.ai/) is installed on your host machine. You must pull the specific embedding model optimized for long-context retrieval.

```bash
# Download the lightweight, high-accuracy embedding model
ollama pull nomic-embed-text
```

**Verify the engine is active:**
Run a `curl` command to ensure the Ollama API is responsive and the model is visible in your local registry.

```bash
curl http://127.0.0.1:11434/api/tags
```

### 2. Configure OpenClaw

You must explicitly instruct the OpenClaw gateway to switch its provider from `openai` to `ollama`.

Edit your global configuration file: `~/.openclaw/openAI.json` (or your specific workspace config). Locate the `agents.defaults.memorySearch` block and apply the following structure:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text:latest",
        "remote": {
          "baseUrl": "http://127.0.0.1:11434"
        }
      }
    }
  }
}
```

> [!IMPORTANT]
> **The `baseUrl` Trap:** When configuring the `baseUrl`, **do not** add `/v1` to the end of the URL, and **do not** include a trailing slash.
>
> * ✅ `http://127.0.0.1:11434`
> * ❌ `http://127.0.0.1:11434/v1`
> * ❌ `http://127.0.0.1:11434/`

### 3. Apply Changes

For the new configuration to take effect, you must restart the OpenClaw gateway service.

```bash
openclaw gateway restart
```

---

## 🛠 Troubleshooting & Best Practices

### Common Pitfalls

* **Provider Mismatch**: OpenClaw does **not** auto-detect Ollma. If you leave the provider as `"openai"`, the system will attempt to send local requests to OpenAI’s servers and fail. Always ensure the `provider` is set to `"ollama"`.
* **Model Missing:** If you see errors regarding "model not found," ensure you have run `'ollama pull nomic-embed-text'`.
* **Port Conflicts:** Ensure no other service is occupying port `11434`.

### Why `nomic-embed-text`?

While you can use other models, `nomic-embed-text` is specifically recommended for OpenClaw because:

1. **Context Window:** It supports much larger context windows than standard small models.
2. **Efficiency:** At ~274MB, it is small enough to run alongside your main LLM without exhausting system RAM.
3. **Performance:** It was trained specifically for retrieval tasks, making it highly accurate for semantic search.

---

## 🔗 Related Documentation

* **[Configuration Reference](./references/config-reference.md)**: Advanced tuning for hybrid search and temporal decay.
* **[Troubleshooting Guide](./references/troubleshooting.md)**: Resolving connection and embedding errors.

---
**Original implementation by [@djc00p](https://github.com/djc00p)**
