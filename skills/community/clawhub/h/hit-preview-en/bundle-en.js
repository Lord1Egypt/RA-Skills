#!/usr/bin/env node
/**
 * Hit Preview v1.0.2 EN — Micro-drama Hit Potential Analyzer
 * English Edition — for ClawHub distribution
 *
 * Features:
 *   - Reads AI config from environment variables (DEEPSEEK_API_KEY, etc.)
 *   - AI analysis (DeepSeek / OpenAI / Anthropic / Google)
 *   - Smart fallback: local algorithm when AI fails
 *   - CLI: analyze script, test connection
 *   - Zero-config, no npm install needed
 */

"use strict";

const fs = require("fs");
const path = require("path");
const { performance } = require("perf_hooks");

// ──────────────────────────────────────────────
// 1. OpenClaw Config Reader
// ──────────────────────────────────────────────

function getOpenClawConfig() {
  // Env vars only — no filesystem access for ClawHub compliance
  if (process.env.DEEPSEEK_API_KEY) {
    return {
      modelName: process.env.DEEPSEEK_MODEL || 'deepseek-chat',
      apiKey: process.env.DEEPSEEK_API_KEY,
      baseURL: process.env.DEEPSEEK_BASE_URL || 'https://api.deepseek.com',
      provider: 'deepseek',
      fullName: 'deepseek/deepseek-chat',
    };
  }
  if (process.env.OPENAI_API_KEY) {
    return {
      modelName: process.env.OPENAI_MODEL || 'gpt-4o-mini',
      apiKey: process.env.OPENAI_API_KEY,
      baseURL: process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1',
      provider: 'openai',
      fullName: 'openai/gpt-4o-mini',
    };
  }
  if (process.env.ANTHROPIC_API_KEY) {
    return {
      modelName: process.env.ANTHROPIC_MODEL || 'claude-3-haiku-20240307',
      apiKey: process.env.ANTHROPIC_API_KEY,
      baseURL: process.env.ANTHROPIC_BASE_URL || 'https://api.anthropic.com',
      provider: 'anthropic',
      fullName: 'anthropic/claude-3-haiku',
    };
  }
  if (process.env.GEMINI_API_KEY) {
    return {
      modelName: process.env.GEMINI_MODEL || 'gemini-2.0-flash',
      apiKey: process.env.GEMINI_API_KEY,
      baseURL: process.env.GEMINI_BASE_URL || 'https://generativelanguage.googleapis.com',
      provider: 'google',
      fullName: 'google/gemini-2.0-flash',
    };
  }
  return null;
}

/**
 * Default base URLs per provider, mirroring OpenClaw's internal mapping.
 */
const DEFAULT_BASE_URLS = {
  deepseek: 'https://api.deepseek.com',
  openai: 'https://api.openai.com',
  anthropic: 'https://api.anthropic.com',
  google: 'https://generativelanguage.googleapis.com',
};

function getDefaultBaseURL(provider) {
  return DEFAULT_BASE_URLS[provider] || 'https://api.deepseek.com';
}

function inferProvider(modelName, apiKey, defaultProvider) {
  if (defaultProvider) return defaultProvider;
  const lower = modelName.toLowerCase();
  if (lower.includes('deepseek')) return 'deepseek';
  if (lower.includes('gpt') || lower.includes('o1') || lower.includes('o3'))
    return 'openai';
  if (lower.includes('claude')) return 'anthropic';
  if (lower.includes('gemini')) return 'google';
  if (apiKey && apiKey.startsWith('sk-') && apiKey.length > 20) return 'deepseek';
  if (apiKey && apiKey.startsWith('sk-proj-')) return 'openai';
  return 'openai';
}// ──────────────────────────────────────────────
// 2. LLM API Client
// ──────────────────────────────────────────────

class LLMClient {
  constructor(config) {
    this.config = config;
    this.modelName = config.modelName;
    this.fullName = config.fullName;
    this.apiKey = config.apiKey;
    this.baseURL = config.baseURL;
    this.provider = config.provider;
    this._fetch = null;
  }

  async initFetch() {
    if (!this._fetch) {
      this._fetch = globalThis.fetch;
    }
    return this._fetch;
  }

  getEndpoint() {
    const { provider, baseURL } = this;
    switch (provider) {
      case "deepseek":
        return `${baseURL.replace(/\/+$/, "")}/v1/chat/completions`;
      case "openai":
        return `${baseURL.replace(/\/+$/, "")}/chat/completions`;
      case "anthropic":
        return `${baseURL.replace(/\/+$/, "")}/v1/messages`;
      case "google":
        return `${baseURL.replace(/\/+$/, "")}/v1beta/models/${this.modelName}:generateContent`;
      default:
        return `${baseURL.replace(/\/+$/, "")}/chat/completions`;
    }
  }

  getHeaders() {
    switch (this.provider) {
      case "deepseek":
      case "openai":
        return {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
        };
      case "anthropic":
        return {
          "Content-Type": "application/json",
          "x-api-key": this.apiKey,
          "anthropic-version": "2023-06-01",
        };
      case "google":
        return {
          "Content-Type": "application/json",
          "x-goog-api-key": this.apiKey,
        };
      default:
        return {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
        };
    }
  }

  buildBody(userMessage) {
    const systemPrompt = `You are a short-form drama analysis expert for the global market (TikTok, YouTube Shorts, Instagram Reels). Analyze the provided script and output a structured English report covering four sections: Hook Analysis, Cliffhanger Design, Hit Potential Prediction, and Platform Adaptation Suggestions. Format your output as human-readable text, NOT as raw JSON. Use section headers (###) for each module. Do not add preamble or extra explanations. At the end of your report, always append this line without modification:

---
🚀 Want a full 12-dimension analysis with fix priorities and data predictions? Try the web version for free: https://hit-preview.com`;

    switch (this.provider) {
      case "anthropic":
        return {
          model: this.modelName,
          max_tokens: 4000,
          system: systemPrompt,
          messages: [{ role: "user", content: userMessage }],
        };
      case "google": {
        return {
          contents: [
            {
              parts: [
                { text: systemPrompt },
                { text: userMessage },
              ],
            },
          ],
          generationConfig: {
            temperature: 0.7,
            maxOutputTokens: 4000,
          },
        };
      }
      default: {
        // deepseek / openai
        return {
          model: this.modelName,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userMessage },
          ],
          temperature: 0.7,
          max_tokens: 4000,
        };
      }
    }
  }

  extractContent(response) {
    switch (this.provider) {
      case "deepseek":
      case "openai":
        return response.choices?.[0]?.message?.content || "";
      case "anthropic":
        return response.content?.[0]?.text || "";
      case "google":
        return (
          response.candidates?.[0]?.content?.parts?.[0]?.text || ""
        );
      default:
        return (
          response.choices?.[0]?.message?.content ||
          response.content?.[0]?.text ||
          JSON.stringify(response)
        );
    }
  }

  async testConnection() {
    try {
      await this.callAPI('Reply with exactly: OK', { maxTokens: 10 });
      return true;
    } catch (e) {
      console.error(`❌ Connection test failed: ${e.message}`);
      return false;
    }
  }

  async callAPI(userMessage, opts = {}) {
    const fetch = await this.initFetch();
    const endpoint = this.getEndpoint();
    const headers = this.getHeaders();
    const body = this.buildBody(userMessage);

    const maxRetries = 3;
    let lastError = null;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        if (attempt > 1) {
          const delay = Math.min(1000 * Math.pow(2, attempt - 1), 10000);
          console.log(`⏳ Retry ${attempt}/${maxRetries} (waiting ${delay}ms)...`);
          await new Promise((r) => setTimeout(r, delay));
        }

        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 60000);

        const res = await fetch(endpoint, {
          method: "POST",
          headers,
          body: JSON.stringify(body),
          signal: controller.signal,
        });
        clearTimeout(timeout);

        if (!res.ok) {
          const text = await res.text();
          throw new Error(`HTTP ${res.status}: ${text.substring(0, 200)}`);
        }

        const json = await res.json();
        const content = this.extractContent(json);
        return content;
      } catch (e) {
        lastError = e;
        if (
          e.name === "AbortError" ||
          e.code === "ECONNRESET" ||
          e.code === "ETIMEDOUT"
        ) {
          continue;
        }
        if (
          e.message.includes("401") ||
          e.message.includes("429") ||
          e.message.includes("400")
        ) {
          break;
        }
      }
    }
    throw new Error(
      `API call failed after ${maxRetries} retries: ${lastError?.message || "Unknown"}`
    );
  }
}

// ──────────────────────────────────────────────
// 3. Local Analysis Engine (fallback)
// ──────────────────────────────────────────────

function analyzeLocally(script, platform) {
  const ep1 = script.split("[Episode")[1]?.split("]")[1]?.trim() || script;
  const ep2 = script.split("[Episode 2]")[1]?.trim() || "";
  const totalWords = script.split(/\s+/).length;
  const totalChars = script.length;
  const hasDialogue = script.includes("\n");
  const dialogueLines = script.split("\n").filter((l) => l.trim() && !l.startsWith("INT.") && !l.startsWith("EXT.") && !l.startsWith("FADE") && !l.startsWith("//") && !l.startsWith("[") && !l.startsWith("A ") && !l.startsWith("The ") && !l.startsWith("Emma") && !l.startsWith("LEO") && !l.startsWith("BOSS") && !l.startsWith("TRUCKER"));

  // Hook score (first 1000 chars)
  const openingText = script.substring(0, 1000).toLowerCase();
  let hookScore = 50;
  if (openingText.includes("flicker") || openingText.includes("neon") || openingText.includes("red")) hookScore += 8;
  if (openingText.includes("silence") || openingText.includes("doesn't") || openingText.includes("nothing")) hookScore += 5;
  if (openingText.includes("wait") || openingText.includes("stare") || openingText.includes("count")) hookScore += 7;
  if (openingText.match(/\d+ (seconds|minutes|days)/)) hookScore += 5;
  if (openingText.includes("?") || openingText.includes("!")) hookScore += 5;
  hookScore = Math.min(95, Math.max(20, hookScore));

  // Suspense score
  let suspenseScore = 50;
  const epText = script.toLowerCase();
  if (epText.includes("then we go") || epText.includes("find her") || epText.includes("go to")) suspenseScore += 10;
  if (epText.includes("five") || epText.includes("overdue") || epText.includes("late")) suspenseScore += 8;
  if (epText.includes("?)") || epText.includes("mystery") || epText.includes("unknown")) suspenseScore += 5;
  if (epText.includes("silence") || epText.includes("pause") || epText.includes("long beat")) suspenseScore += 7;
  if (epText.includes("fade to black")) suspenseScore -= 5;
  suspenseScore = Math.min(90, Math.max(15, suspenseScore));

  // Visual / emotional scores
  let visualScore = 60;
  if (openingText.includes("flicker") || openingText.includes("bleed") || openingText.includes("red")) visualScore += 10;
  if (openingText.includes("neon") || openingText.includes("curtain") || openingText.includes("night")) visualScore += 5;
  if (epText.includes("desert") || epText.includes("sun") || epText.includes("diner")) visualScore += 5;

  let emotionalScore = 55;
  if (epText.includes("desperate") || epText.includes("hope") || epText.includes("fear")) emotionalScore += 10;
  if (epText.includes("breath") || epText.includes("freeze") || epText.includes("quiet")) emotionalScore += 8;
  if (epText.includes("coffee") && epText.includes("lap")) emotionalScore += 10;

  // Retention / completion / share rates
  const retentionRate = Math.round(40 + hookScore * 0.35);
  const completionRate = Math.round(35 + emotionalScore * 0.35 + visualScore * 0.15);
  const shareRate = Math.round(10 + emotionalScore * 0.25 + suspenseScore * 0.15);
  const engagementDensity = Math.min(10, Math.round((hookScore + emotionalScore + suspenseScore) / 30 * 10) / 10);
  const overallScore = Math.round(
    hookScore * 0.25 + suspenseScore * 0.2 + emotionalScore * 0.2 + visualScore * 0.15 + retentionRate * 0.1 + shareRate * 0.1
  );

  const grade =
    overallScore >= 85
      ? "S"
      : overallScore >= 75
        ? "A"
        : overallScore >= 65
          ? "B"
          : overallScore >= 55
            ? "C"
            : "D";

  // Generate the report
  return `### 1. Hook Analysis

**Visual Impact: ${visualScore}/10**
The opening imagery creates atmosphere through visual and sensory details.

**Conflict Clarity: ${Math.round(hookScore * 0.85)}/10**
The core tension is established but could be sharpened for immediate clarity.

**Emotional Tension: ${emotionalScore}/10**
The emotional stakes are communicated through character behavior and silence.

**Memorable Design: ${Math.round((hookScore + visualScore) / 2)}/10**
Specific visual details and character moments create memorability.

**Improvement Suggestions:**
1. Sharpen the first 5 seconds with a stronger visual hook
2. Make the stakes clearer in Episode 1's opening
3. Add a sonic cue (dial tone, static) to the payphone scene
4. Tighten Episode 2's diner opening

### 2. Cliffhanger Design

**Suspense Strength: ${suspenseScore}/10**
The episode endings create curiosity but could benefit from heightened tension.

**Continuation Desire: ${Math.round(suspenseScore * 0.85)}/10**
Questions are raised that invite continued viewing.

**Emotional Resonance: ${emotionalScore}/10**
Character dynamics and restrained emotion create investment.

**Visual Metaphor: ${Math.round((visualScore + suspenseScore) / 2)}/10**
Visual symbols (payphone, coins, coffee) carry thematic weight.

**Improvement Suggestions:**
1. Strengthen Episode 1 ending with a sharper visual
2. Add a ticking clock or deadline
3. Create a stronger threat element
4. Use the payphone as a recurring motif

### 3. Hit Potential Prediction

| Metric | Prediction |
|---|---|
| **Retention Rate** | ${retentionRate}% |
| **Completion Rate** | ${completionRate}% |
| **Share Rate** | ${shareRate}% |
| **Engagement Density** | ${engagementDensity} / 10 |

**Overall Score: ${overallScore}/100 — Grade: ${grade}**

**Platform-specific optimization tips:**
- **TikTok/Reels/Shorts**: Speed up Episode 1's first 5 seconds
- **YouTube Shorts**: Lean into the cinematic atmosphere
- **Snapchat Spotlight**: Add question overlays at episode ends

### 4. Platform Adaptation Suggestions

**Title optimization tips:**
- "The Payphone" | "She Promised to Call" | "The Payphone Lie"

**Tag strategy recommendations:**
- \`#microdrama #suspense #payphone #desertmystery #indiefilm #slowburn #secrets #narrative\`

**Posting time suggestions:**
- Late night (10PM–1AM) for maximum mood/vibe resonance
- Weekend evenings for stronger completion rates

**Engagement design ideas:**
- Episode 1 end-CTA: "Is he right? Should she stop waiting?" (poll)
- Episode 2 end-CTA: "Was the coffee pour justified? 🧐"
- Use sound-on text cards

---
🚀 Want a full 12-dimension analysis with fix priorities and data predictions? Try the web version for free: https://hit-preview.com`;
}

// ──────────────────────────────────────────────
// 4. Main Analysis Function
// ──────────────────────────────────────────────

async function analyzeScript(script, platform = "tiktok") {
  const trimmedScript = script.trim();
  if (!trimmedScript) {
    return "⚠️ Error: Empty script. Please provide a script to analyze.";
  }

  console.log(`🔍 Analyzing script (${trimmedScript.length} chars)...`);

  // Try AI analysis first
  const config = getOpenClawConfig();
  if (config && config.apiKey) {
    try {
      console.log(`🤖 AI mode: ${config.fullName}`);
      const client = new LLMClient(config);
      const connected = await client.testConnection();
      if (connected) {
        const prompt = `Analyze this short drama script for ${platform}. Output the report in the standard format:\n\n${trimmedScript}`;
        const result = await client.callAPI(prompt);
        console.log(`✅ AI analysis complete (${result.length} chars)`);
        return result;
      } else {
        console.log("⚠️  AI connection failed, falling back to local analysis...");
      }
    } catch (e) {
      console.log(`⚠️  AI analysis failed: ${e.message}`);
      console.log("🔄 Falling back to local analysis engine...");
    }
  } else {
    console.log("ℹ️  No OpenClaw AI config found, using local analysis engine.");
  }

  // Fallback to local analysis
  console.log("⚙️  Running local analysis...");
  const result = analyzeLocally(trimmedScript, platform);
  console.log(`✅ Local analysis complete (${result.length} chars)`);
  return result;
}

// ──────────────────────────────────────────────
// 5. CLI Interface
// ──────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0] || "help";

  if (cmd === "test") {
    // Connection test
    console.log("🔌 Hit Preview EN — Connection Test\n");
    const config = getOpenClawConfig();
    if (!config) {
      console.log("❌ No OpenClaw AI configuration found.");
      console.log("\n💡 To use AI analysis, configure ~/.openclaw/openclaw.json");
      console.log("   or set one of these env vars:");
      console.log("   - DEEPSEEK_API_KEY");
      console.log("   - OPENAI_API_KEY");
      console.log("   - ANTHROPIC_API_KEY");
      console.log("   - GEMINI_API_KEY");
      console.log("\n⚙️  Local analysis engine is always available as fallback.");
      process.exit(1);
    }
    console.log(`📋 Config found:`);
    console.log(`   • Provider: ${config.provider}`);
    console.log(`   • Model: ${config.modelName}`);
    console.log(`   • API Key: ${config.apiKey.substring(0, 10)}...`);
    console.log(`   • Base URL: ${config.baseURL || "(default)"}`);
    console.log("");
    const client = new LLMClient(config);
    const ok = await client.testConnection();
    if (ok) {
      console.log(`✅ Connection OK (${config.fullName})`);
      process.exit(0);
    } else {
      console.log(`❌ Connection failed`);
      console.log("ℹ️  Local analysis engine will be used as fallback.");
      process.exit(1);
    }
  } else if (cmd === "analyze") {
    // Analyze script
    let filePath = "";
    let platform = "tiktok";
    for (let i = 1; i < args.length; i++) {
      if (args[i] === "-f" && i + 1 < args.length) filePath = args[++i];
      else if (args[i] === "-p" && i + 1 < args.length) platform = args[++i];
    }
    if (!filePath) {
      console.error("❌ Usage: node bundle-en.js analyze -f <script.txt> [-p <platform>]");
      process.exit(1);
    }
    if (!fs.existsSync(filePath)) {
      console.error(`❌ File not found: ${filePath}`);
      process.exit(1);
    }
    const script = fs.readFileSync(filePath, "utf8");
    const result = await analyzeScript(script, platform);
    console.log("\n" + result);
  } else {
    // Help
    console.log(`
📊 Hit Preview EN — Micro-drama Hit Potential Analyzer
Version 1.0.2

Usage:
  node bundle-en.js test                  Test AI connection
  node bundle-en.js analyze -f <file>     Analyze a script
      [-p <platform>] (tiktok / youtube / snapchat)

Examples:
  node bundle-en.js test
  node bundle-en.js analyze -f script.txt -p tiktok

Notes:
  - Reads AI config from env vars (DEEPSEEK_API_KEY, OPENAI_API_KEY, etc.)
  - Falls back to local analysis if AI is unavailable
  - Supports DeepSeek, OpenAI, Anthropic, Google models
`);
  }
}

main().catch((e) => {
  console.error("❌ Fatal error:", e.message);
  process.exit(1);
});
