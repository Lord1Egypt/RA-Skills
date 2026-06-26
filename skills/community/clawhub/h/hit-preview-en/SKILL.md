---
name: hit-preview
version: 1.0.2
description: Hit Preview EN - English edition. Micro-drama hit potential analyzer for TikTok, YouTube Shorts, Instagram Reels. Analyzes scripts with AI (reads your OpenClaw config) or falls back to local analysis engine. Outputs clean English reports with 4 modules: Hook Analysis, Cliffhanger Design, Hit Potential Prediction, Platform Adaptation Suggestions.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - node
    install:
      - kind: script
        path: setup.sh
        silent: false
---

# Hit Preview v1.0.0 — English Edition

## 📊 **Report Format (4 Modules)**

### 1. **Hook Analysis**
- Visual Impact score + analysis
- Conflict Clarity score + analysis
- Emotional Tension score + analysis
- Memorable Design score + analysis
- Specific improvement suggestions (3-5 items)

### 2. **Cliffhanger Design**
- Suspense Strength score + analysis
- Continuation Desire score + analysis
- Emotional Resonance score + analysis
- Visual Metaphor score + analysis
- Improvement suggestions (3-5 items)

### 3. **Hit Potential Prediction**
- Retention Rate prediction (0-100%)
- Completion Rate prediction (0-100%)
- Share Rate prediction (0-100%)
- Engagement Density score (0-10)
- Overall Score (0-100) + Grade (S/A/B/C/D)
- Platform-specific optimization tips

### 4. **Platform Adaptation Suggestions**
- Title optimization tips
- Tag strategy recommendations
- Posting time suggestions
- Engagement design ideas

### Footer (every report)
```
---
🚀 Want a full 12-dimension analysis with fix priorities and data predictions? Try the web version for free: https://hit-preview.com
```

## 🚀 **Highlights**

### ✅ **Auto AI — Zero Config**
- **Reads OpenClaw config** automatically (env vars (DEEPSEEK_API_KEY, etc.))
- **Uses your current AI model** (DeepSeek / OpenAI / Anthropic / Google)
- **No .env file needed** — just run it

### ✅ **Smart Fallback**
- **AI unavailable?** Falls back to local analysis engine
- **API key missing?** No problem, still works
- **Network down?** Local engine handles it
- **Always usable** — never leaves you without a report

### ✅ **Works Everywhere**
- **Node.js >= 18** — no npm install, no build step
- **Single file** — one bundle, everything included
- **Pre-built** — download and run immediately

## 🛠️ **Usage**

### In OpenClaw
```
@Tianshu Analyze this script with Hit Preview EN: [Paste script]
```

### As CLI
```bash
# Test AI connection
./run-hit-preview-en.sh test

# Analyze a script
./run-hit-preview-en.sh analyze -f script.txt -p tiktok

# Direct (no script):
node bundle-en.js analyze -f script.txt -p tiktok
```

**Supported platforms**: tiktok, youtube, snapchat (default: tiktok)

## 📋 **Requirements**
- **Runtime**: Node.js >= 18
- **AI analysis** (optional, auto-detected): OpenClaw config
- **No install**: no `npm install`, no TypeScript compilation, no build step

## ⚙️ **How It Works**

1. **Auto-detect**: Reads env vars for AI config (~/.openclaw/openclaw.json)
2. **AI mode**: Uses your configured model for full-depth analysis
3. **Fallback**: If AI fails (no config, bad key, network), falls back to local algorithm
4. **Report**: Always outputs the standard 4-module English report

## 🔧 **Configuring OpenClaw for AI**

If you haven't set up OpenClaw yet, create `~/.openclaw/openclaw.json`:

```json
{
  "default_provider": "deepseek",
  "providers": {
    "deepseek": {
      "apiKey": "sk-your-key-here",
      "model": "deepseek-chat"
    }
  }
}
```

Or set environment variables:
```bash
export DEEPSEEK_API_KEY="sk-your-key-here"
```

## ⚠️ **Notes**
- This is a **quick-scan version** (4 modules). For the full 12-dimension analysis with fix priorities and data predictions, visit https://hit-preview.com
- AI mode uses your configured model; local mode uses text-feature algorithms
- Real-world performance depends on acting, editing, and platform algorithms

---

**Version**: v1.0.1 EN  
**Release**: 2026-05-03  
**Footer**: 🚀 Want a full 12-dimension analysis with fix priorities and data predictions? Try the web version for free: https://hit-preview.com  
**Note**: All prompts and outputs are in English.
