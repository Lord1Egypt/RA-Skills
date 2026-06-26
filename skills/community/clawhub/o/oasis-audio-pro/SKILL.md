---
name: "oasis-audio-pro"
description: "Oasis Audio Pro is an AI audio narration generator that transforms your current state of mind, content you want to digest, or recent life events into a personalized audio with BGM. It supports Chinese & English, 9 reference modes (Soul Healing, Daily Briefing, Knowledge Deep Dive, Content Digest, Bedtime Radio, Language Learning, Conversation Extension, Topic Tracker, Study Buddy), and custom audio profiles when no template fits. Use this skill when the user asks to make audio, generate a podcast, turn notes or long content into audio, or when an audio version would add value. This skill includes local Python scripts that read ~/.qclaw or ~/.openclaw session/memory files for personalization — all processing is local and read-only. Only the final composed text prompt is sent to the xplai.ai API (https://eagle-api.xplai.ai); raw conversation history, session files, and USER.md are not transmitted. If the AI judges that the final prompt may be sensitive, the skill shows a sanitized preview and requires a second explicit confirmation before any API request."
metadata:
  openclaw:
    emoji: "🎧"
    requires:
      bin:
        - python3
---

# Oasis Audio Pro Instructions
This skill provides **AI audio narration generation** using xplai.ai service.

AI audio narration generation via xplai.ai with local-only context processing and sensitive-preview confirmation. No user API key required. Includes local Python scripts; a visitor JWT token is obtained automatically on first use and persisted in `~/.oasis_audio/oasis_config.json`.

Official website: [www.xplai.ai](https://www.xplai.ai/)

When calling this skill, ALWAYS spawn a subagent to poll for results. After calling `xplai_gen_audio.py`, wait 210 seconds before the first status check, then poll with `xplai_status.py` once every 60 seconds, maximum 10 checks. Stop polling when status becomes `v_succ` or `v_fail`. Report the final result automatically.

## Execution Policy

**When the user explicitly asks to generate audio, proceed directly with the full generation pipeline, infer all necessary parameters (mode, tone, depth, voice) from conversation context and user profile.**

**First-use authorization:** Before the first real send, `xplai_gen_audio.py` prints a one-time authorization notice and requires `--acknowledge-consent` to persist the user's approval locally. The notice should clearly explain, in calm and gentle language, that the skill may read `~/.qclaw/...` or `~/.openclaw/...` local history to produce personalized audio. However, only the composed prompt is sent to `https://eagle-api.xplai.ai`, and that any detected sensitive information will be blocked until the user explicitly confirms.

**Sensitive information protection:** The calling AI should make its own conservative judgment about whether the composed prompt may contain sensitive information. If the composed text is sensitive, show the sanitized preview text to the user first, pause for explicit confirmation, and do not send anything until the user confirms. Use `./xplai_gen_audio.py --dry-run ...` to preview manually, or rely on the built-in sensitive preview shown by `xplai_gen_audio.py`. Only resume with `./xplai_gen_audio.py --allow-sensitive ...` after the user explicitly confirms.

Only ask the user a question outside this sensitive-content checkpoint if critical information is truly unresolvable from context (e.g., the request is entirely ambiguous with no conversation history available).

## User Need Inference

**The user's actual need always takes priority over predefined modes.** Before generating audio, infer the user's true need along 3 dimensions:

1. **What do they actually want to hear?** — Infer the deeper need beyond the literal request. Use conversation context to find the real motivation.
    | User says | Literal reading | Deeper need |
    |-----------|----------------|-------------|
    | "最近好焦虑" | Anti-anxiety content | Something that addresses their specific anxiety source (found in context), not generic meditation |
    | "帮我做个关于咖啡的音频" | Coffee knowledge | Calibrated to what they already know (beginner vs. expert, found in context) |
2. **What tone fits their current state?** — High-stress → warm/slow. Curiosity → engaging/detailed. Boredom → surprising. Excitement → match energy. Post-achievement → celebratory then reflective.
3. **What depth and duration fit?** — Calibrate by cognition level (new vs. deep prior knowledge), available attention (late night → shorter, weekend → longer), and repetition tolerance (don't repeat what they already know).

**Custom Mode:** When no predefined mode fits, create a custom audio profile: name it descriptively (e.g., "赶完DDL后的温柔复盘"), define content structure based on inferred need, and set voice/pacing to match.

For the 9 predefined audio modes (Soul Healing, Daily Briefing, Knowledge Deep Dive, Content Digest, Bedtime Radio, Language Learning, Conversation Extension, Topic Tracker, Study Buddy), read `audio_modes.md` for triggers, durations, and suggestions.

---

## Personalized Context Collection

Read conversation history to personalize audio. If any step yields no results, skip to text preparation without personalization — do NOT fabricate context.

### Step 0: Detect Source Tool

Auto-detect by checking which default roots have files: `~/.qclaw/`, `~/.openclaw/` → pick the one with the most recently modified session file. If none exist, skip personalization.

### Step 1: Scene Classification

Classify into exactly ONE scene type:

| Scene | When to Apply | Search Action | Days |
|-------|---------------|---------------|------|
| `event` | Specific event (finished DDL, got promoted) | Full story extraction | 3 |
| `emotion_only` | Mood without event ("感觉很丧") | High-emotion fragments | 3 |
| `future` | Upcoming plans/worries ("明天面试") | Preparation context | 7 |
| `long_term` | Ongoing state ("一直加班") | Recurring topics | 30 |
| `interest` | Hobby/knowledge topic ("咖啡豆科普") | Cognition level check | 14 |
| `functional` | Pure utility (white noise, pomodoro) | **SKIP** | — |
| `no_context` | No personal angle / first interaction | **SKIP** | — |
| `sensitive` | Health, finances, relationships, legal | Emotion tone ONLY, never quote specifics | 3 |
| `weekly_review` | Recap of past week | Multi-topic extraction | 7 |

### Step 2: Keyword Fan-out

Generate keywords in 3 layers: **Direct** (core topic) → **Behavior** (related actions) → **Emotion** (emotional signals). Combine into comma-separated string.

### Step 3: Call Context Collector

```bash
python3 context_collector.py --source-tool <tool> --keywords "<kw1,kw2,...>" --days <N> --max-results 20
```

Output: JSON with `fragments`, `daily_memories`, and `user_profile` (structured fields: `name`, `mbti`, `interests`, `notes`).

**Error handling:** If script fails, skip personalization and generate generic audio. Do NOT retry or debug during generation.

### Step 4: Fine-filter Results

Apply semantic filtering by scene type. Discard irrelevant matches. Keep the 3-5 most relevant fragments.

| Scene | What to Extract |
|-------|----------------|
| `event` | Event → Process → Emotion arc → Current state |
| `emotion_only` | Emotional background themes |
| `future` | Preparation activities, specific worries |
| `long_term` | Recurring topics → "daily portrait" |
| `interest` | Prior knowledge → depth level |
| `sensitive` | Emotional tone ONLY — **NEVER** quote specifics |
| `weekly_review` | Topics → Progress → Emotional highlights → Patterns |

### Step 5: Compose Personalization Summary

Compress into **~300-500 character** summary. Read naturally, focus on tailored details, never feel surveillance-like. If nothing matched, proceed without personalization.

---

## Text Architecture

After context collection, compose a structured Audio Brief covering 7 layers: **Content Structure, Voice & Delivery, Voice Selection, Personalization Anchors, Emotional Arc, Content Enrichment, Format & Pacing**. Then distill into the final prompt. Read `text_architecture.md` for the full 7-layer framework, prompt structure, role design, and example prompt.

### Voice Selection (Layer 3)

Pick exactly one `voice_id` based on the tone category, then choose the male or female variant based on the user's preference and content's gender lean.

| Category | Traits | Male voice_id | Female voice_id |
|---|---|---|---|
| 知识探索型 | 清晰、克制、理性、高信息密度、分析感 | `Chinese (Mandarin)_Male_Announcer` | `danya_xuejie` |
| 温暖陪伴型 | 柔和、治愈、温润、亲密、低存在感、深夜氛围 | `Chinese (Mandarin)_Warm_Bestie` | `Chinese (Mandarin)_Sincere_Adult` |
| 犀利观点型 | 果断、有力度、观点锋利、节奏感强、精英感 | `male-qn-jingying-jingpin` | `voice_female_Logic_Quartz` |
| 故事叙事型 | 画面感、沉浸式、有层次感、叙述者视角 | `Chinese (Mandarin)_Humorous_Elder` | `Chinese (Mandarin)_Wise_Women` |
| 轻松漫谈型 | 自然、轻快、元气、随意、朋友间聊天感 | `Chinese (Mandarin)_Gentleman` | `female-chengshu` |

Heuristics:
- warm-empathetic → 温暖陪伴型
- steady-authoritative → 知识探索型
- light-humorous / casual → 轻松漫谈型
- storytelling / narrative → 故事叙事型
- sharp opinion / hot take → 犀利观点型

If user's memory `reference` points at a specific style, pick the closest category. If gender lean is unclear from context, default to the male variant.

### Calling the Tool

```bash
./xplai_gen_audio.py --voice-id "<voice_id>" "<composed prompt>"
```

Keep prompt under **800 characters** (Chinese) or **1200 words** (English). For `weekly_review`, up to 1000 characters.

---

## Available Commands

### 1. Generate Audio — `xplai_gen_audio.py`

```bash
./xplai_gen_audio.py [--voice-id <voice_id>] [--dry-run] [--audit] [--acknowledge-consent] [--allow-sensitive] <text>
```

- `text` — Composed prompt text
- `--voice-id` — Voice selection (see `text_architecture.md` Layer 3)
- `--dry-run` — Preview sanitized prompt without sending to API
- `--audit` — Write the final sent prompt and request outcome to local `audit.log` (off by default)
- `--acknowledge-consent` — Persist the first-use authorization notice locally and continue
- `--allow-sensitive` — Only use after the user explicitly confirms that the detected sensitive content preview may be sent

Output: Audio ID for status polling. Format: MP3, single-narrator monologue with BGM, 8-20 min, ~4-5 min generation time.

### 2. Collect Context — `context_collector.py`

```bash
python3 context_collector.py --source-tool <qclaw|openclaw> --keywords "kw1,kw2" --days <N> --max-results 20
```

Output: JSON with `fragments`, `daily_memories`, `user_profile` (structured fields only).

### 3. Query Status — `xplai_status.py`

```bash
./xplai_status.py <audio_id>
```

- `init` - Request just submitted
- `q_proc` - Content is being processed
- `q_succ` - Content processing completed
- `q_fail` - Content processing failed
- `v_proc` - Audio is in generation queue
- `v_succ` - Audio generated successfully
- `v_fail` - Audio generation failed

> **Note:** Status codes use the `v_` prefix because xplai's API uses "video" nomenclature internally for all media types, including audio-only content.

---

## Data Privacy & Security

### Data Accessed

This skill reads **local conversation history** from the default OpenClaw/QClaw roots (`~/.qclaw/`, `~/.openclaw/`) via `context_collector.py`. At runtime it looks inside the built-in subpaths `agents/main/sessions`, `workspace/memory`, and `workspace/USER.md` when they exist. These are default lookup paths rather than required user config. **All data access is local and read-only** — no source files are modified, created, or deleted.

**Why conversation history?** The skill searches recent conversations for keywords related to the user's audio request, extracting emotional tone, topics, and context. This enables personalized audio — e.g., referencing a stressful week the user had, rather than generating generic content. Only 3-5 short fragments are selected; the rest are discarded in memory.

**Why USER.md?** The user profile provides the user's preferred name (to address them personally in the audio), personality type (to match tone), and interests (to enrich content with cross-domain connections). If USER.md is absent, the skill proceeds without personalization.

### Data Flow

1. **Local processing only**: `context_collector.py` runs entirely on your machine. Conversation fragments are searched, filtered, and summarized locally.
2. **What is sent externally**: Only the **composed text prompt** (a short summary inferred from local data — not raw conversation text) is sent to the xplai.ai API for audio generation. The prompt contains inferred themes, tones, and personalization anchors. Because the prompt is derived from local context, it may indirectly reflect personal details; the built-in heuristic redaction and the sensitive-preview confirmation step reduce this risk.
3. **What is NOT sent**: Raw conversation history, session files, USER.md content, file paths, timestamps, or verbatim personal identifiers are not transmitted. The heuristic redaction and scene-classification rules are designed to prevent PII from reaching the composed prompt.

### Third-Party Services

| Service | Purpose | Data Sent | Endpoint |
|---------|---------|-----------|----------|
| [xplai.ai](https://www.xplai.ai/) | Audio generation | Composed text prompt only (max ~1000 chars) | HTTPS API |

No other external services, analytics, or telemetry are used.

### Data Retention

- **Local**: Source conversations are not modified. On first use, the skill writes `~/.oasis_audio/oasis_config.json` containing a visitor JWT token and consent flag — these persist across sessions. By default this skill does **not** write `audit.log`; if `--audit` is explicitly enabled, `xplai_gen_audio.py` may append the outbound prompt and request outcome to local `audit.log` for traceability. If sensitive content is detected, the user must first review the preview text and explicitly confirm before either logging or sending. All other intermediate results (fragments, summaries) exist only in memory during execution.
- **Remote**: Audio files generated by xplai.ai are subject to [xplai.ai's retention policy](https://www.xplai.ai/). This skill does not control remote data retention.

### First-Use Notice

On the first real send, `xplai_gen_audio.py` should present a one-time authorization note before continuing. Recommended wording:

> 在真正发出第一条请求之前，先把边界说清楚！为了让这段音频更贴近你，我会看看你存在openclaw/qclaw的会话记录、memory 和 `USER.md`哦。但是，我不会改任何东西，只会把整理好的请求文本（不超过1000字）发送到xplai音视频平台（`https://eagle-api.xplai.ai`）；生成完成后，你也可以在 xplai 网页在线查看结果～ \n 如果系统判断有敏感信息，我会先给你看脱敏后的预览，等你点确认再发出去～ \n 若你接受这条边界，我们现在就为你生成专属音频啦！后续不会再反复询问这个权限请求～

### Permissions

- **File system**: Read-only access to OpenClaw-ecosystem session directories and USER.md. Writes the following local files on first use: `~/.oasis_audio/oasis_config.json` (visitor JWT token + consent flag); optionally `audit.log` in the skill directory when `--audit` is enabled.
- **Network**: HTTPS requests to xplai.ai only (`https://eagle-api.xplai.ai`). A visitor JWT token is obtained automatically via the xplai login endpoint on first use; no user-supplied API key or account is required.
- **No external credentials required from the user**: Users do not need to provide any API keys, passwords, or secrets. The skill self-provisions a visitor token on your behalf and stores it locally.

### Sensitive Content Handling

For conversations classified as `sensitive` (health, finances, relationships, legal), the skill extracts **emotional tone only** — specific details are never quoted, summarized, or included in the audio prompt. See the "Scene Classification" section for details.

`xplai_gen_audio.py` also performs heuristic checks before sending or logging. In addition, the calling AI should proactively judge whether the content may be sensitive based on context, even if no heuristic rule fires. Treat the prompt as sensitive if it appears to contain:

- credentials or auth material
- email addresses, phone numbers, government IDs, account/card numbers, or wallet addresses
- first-person medical, financial, or legal details
- explicit addresses, or similar personal identifiers

If any of those checks trigger, or if the AI judges there is a meaningful chance that the content is sensitive, stop, show the preview text to the user, and confirm with the user before using `--allow-sensitive`. Even after confirmation, hard secrets such as tokens, passwords, private keys, and similar credential material must still be redacted before transmission or audit logging. Writing to `audit.log` still requires the separate `--audit` flag.
