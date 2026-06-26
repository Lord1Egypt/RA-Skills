# Manusilized: The OpenClaw Supercharger

**Manusilized** is not just a skill; it's a comprehensive upgrade for your OpenClaw agent, bringing enterprise-grade reliability and a "Manus-like" silky-smooth experience to open-source models (like Qwen, GLM, DeepSeek).

## 🌟 Key Features

1. **Incremental Streaming (Silky Smooth Experience)**
   - No more staring at a blank screen while reasoning models think! Manusilized introduces real-time `text_delta` streaming for Ollama models.
   - You get a live typewriter effect, perfectly mirroring the behavior of closed-source giants.

2. **Markdown Tool-Call Fallback (The "Amnesia" Cure)**
   - Open-source models often struggle with native JSON Function Calling, outputting tool calls embedded within Markdown code blocks.
   - Manusilized includes a fault-tolerant adapter that automatically detects, extracts, and corrects these embedded tool calls, drastically improving success rates.

3. **Extended Reasoning Model Support (2026 Ready)**
   - Natively recognizes and optimizes for the latest generation of reasoning models: `qwen3`, `qwq`, `glm-5`, `kimi-k2.5`, `deepseek-v3`, `marco-o1`, and `skywork-o`.

## 🛠️ Installation & Setup

Since Manusilized modifies the core `agents` architecture of OpenClaw, it cannot be installed merely as a standard skill folder.

### Option 1: The Official PR (Recommended)
We have submitted these upgrades as a core PR to the OpenClaw repository.
👉 **[View and Upvote the PR on GitHub](https://github.com/openclaw/openclaw/pulls)**

### Option 2: Manual Patch
If you want to experience Manusilized immediately before the PR is merged, you can apply our patch directly to your OpenClaw installation:

1. Clone the OpenClaw repository.
2. Download the Manusilized patch files from our [GitHub repository](https://github.com/manusilized/manusilized).
3. Replace the corresponding files in `src/agents/` (`ollama-stream.ts` and `ollama-models.ts`).
4. Rebuild OpenClaw.

## 💡 Why Manusilized?

Our mission is to democratize the "perfect agent" experience. By bridging the gap between open-source models and enterprise frameworks, Manusilized ensures that anyone can run a top-tier AI agent locally or in the cloud without relying on expensive API keys.

---
*Created by Manus AI.*
