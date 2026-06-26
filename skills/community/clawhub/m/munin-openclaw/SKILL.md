---
name: "@kalera/munin-openclaw"
description: "Munin - The Free (or $1.6/mo) Persistent Memory for OpenClaw. Stop your agent from having Alzheimer's."
version: "1.0.1"
metadata:
  clawdbot:
    type: "plugin"
    permissions:
      env: ["MUNIN_BASE_URL", "MUNIN_API_KEY"]
---

# 🐦 Munin: Reliable Memory for Your OpenClaw Agent

Your agent forgets everything the moment you close the tab. You've seen the "pro" solutions—Mem0, Zep, LangMem—and you've seen their **$20/month** price tags. 

We think that's insane. 

**Munin** is the pragmatic alternative. It’s the "Reliable Friend" that sits on your agent’s shoulder and whispers: *"Hey, remember when pa Kal said he preferred Python over Node last week?"*

### 💰 Why Munin? (The "No-Brainer" Math)

| Feature | Mem0 / Zep | **Munin** |
| :--- | :--- | :--- |
| **Monthly Cost** | $19.00 - $249.00 | **Free** (or $1.60 Pro) |
| **MCP Support** | Mixed | **Native / First-class** |
| **Zero-Knowledge E2EE** | Optional / Complex | **Built-in (Client-side)** |
| **Bullshit Factor** | High (Enterprise-synergy) | **Zero (Developer-first)** |

**That’s a 10x - 150x price gap.** We aren't building "Enterprise Synergy Platforms". We're building a notebook for your AI.

---

## 🔒 Security & Privacy

**Trust Statement:**
Data stays where you tell it to stay. All data is encrypted locally (if E2EE is enabled) and isolated by your Context Core. We are completely blind to your plaintext.

**External Endpoints:**
Data is sent ONLY to your `MUNIN_BASE_URL`. We don't phone home. We don't sell your "memories" to train models.

## 💎 E2EE with GraphRAG (Elite Tier)

If your Munin project has **E2EE with GraphRAG** enabled, standard E2EE rules apply PLUS:
- You **MUST** generate a vector embedding of the plaintext content locally before encrypting.
- You **MUST** include the embedding array in the `store` payload: `{ "content": "encrypted...", "embedding": [0.1, -0.02, ...], "encryptionMeta": {...} }`.
- Munin will use this vector for zero-knowledge semantic search. It will reject the request if the embedding is missing.

---

## 🚀 Setup (Fast & Honest)

1. **Get your Munin key:** Grab a **free** cloud key at [munin.kalera.dev](https://munin.kalera.dev).
2. **Configure OpenClaw:** Add these to your `.env` or agent config:
   - `MUNIN_BASE_URL`: Where your Munin lives (e.g., `https://munin.kalera.dev`).
   - `MUNIN_API_KEY`: Your key to the kingdom.

*(Note: Provide your agent with the `Context Core ID` in its system prompt so it knows which project to use when making tool calls).*

3. **Profit:** Your agent now has long-term memory. No more repeating yourself.

---
*Built with ❤️ by Kalera for the OpenClaw Ecosystem.*