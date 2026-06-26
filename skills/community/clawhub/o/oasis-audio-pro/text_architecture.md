# Text Architecture — 7-Layer Audio Brief

After collecting personalized context (or skipping it), compose a structured **Audio Brief** covering all 7 layers below. Then distill the brief into the final text prompt for the API.

## Layer 1: Content Structure — What to say and how to organize it

| Element | Description | How to Decide |
|---------|-------------|---------------|
| **Topic** | One-sentence core subject | From user's request + context enrichment |
| **Narrative structure** | How content unfolds | Linear story / Q&A / Emotional arc / Point-counterpoint / Free-form chat / List-based |
| **Key anchors** | 3-5 must-hit points | Inferred from user need + context. E.g., "acknowledge struggle → recall small wins → gentle humor → look ahead" |
| **Depth level** | How deep to go | Introductory (new to user) / Intermediate (discussed before) / Expert (deep prior knowledge) — calibrate from context |
| **Information density** | New info per minute | Low (sleep/emotional) / Medium (narrative/story) / High (learning/briefing) |

## Layer 2: Voice & Delivery — How to say it

| Element | Options | When to Use |
|---------|---------|-------------|
| **Pacing** | Slow / Medium / Fast | Slow: sleep, emotional healing. Medium: daily narrative. Fast: news, excitement |
| **Tone** | Warm-empathetic / Calm-rational / Light-humorous / Energetic-enthusiastic / Steady-authoritative | Match user's current emotional state from context |
| **Energy curve** | Flat→fade / Low→high / Wave / High→settle | Fade: sleep. Low→high: motivation. Wave: storytelling. High→settle: news briefing |
| **Perspective** | "I to you" (intimate) / "Let's talk" (peer) / Third-person (objective) | Emotional → intimate. Knowledge → peer. News → objective |
| **Language** | Primary language + mixing rules | Follow user's language. Keep technical terms in original language when clearer |

## Layer 3: Voice Selection — Which voice to use

Choose **exactly one** voice that best matches the audio's content and tone:

| Category | Traits | Voice ID |
|----------|--------|----------|
| **知识探索型 (Knowledge Exploration)** | 清晰、克制、信息密度高、理性、分析感 | `Chinese (Mandarin)_Male_Announcer` |
| **温暖陪伴型 (Warm Companionship)** | 柔和、治愈、温润、亲密、低存在感、深夜氛围 | `Chinese (Mandarin)_Warm_Bestie` |
| **犀利观点型 (Sharp Opinions)** | 果断、有力度、观点锋利、节奏感强、精英感 | `male-qn-jingying-jingpin` |
| **故事叙事型 (Storytelling)** | 画面感、沉浸式、有层次感、叙述者视角 | `Chinese (Mandarin)_Humorous_Elder` 或 `Chinese (Mandarin)_Wise_Women`（根据内容性别倾向选择其一） |
| **轻松漫谈型 (Relaxed Chat)** | 自然、轻快、元气、随意、朋友间聊天 | `Chinese (Mandarin)_Gentleman` |

Use Layer 2 tone/pacing decisions to guide voice selection. For example: warm-empathetic tone → 温暖陪伴型; steady-authoritative → 知识探索型; light-humorous → 轻松漫谈型.

## Layer 4: Personalization Anchors — Why it feels tailor-made

| Element | Description | Source |
|---------|-------------|--------|
| **Specific details** | Concrete fragments from user's experience | context_collector output: "revised it 4 times", "stayed up until 3am" |
| **Emotional resonance** | The user's strongest current feeling | Fine-filtered emotion arc from context |
| **Cognitive starting point** | What the user already knows | Depth of prior discussions on the topic |
| **Related people/projects** | Names, projects the user cares about | Recurring mentions in conversation history |
| **No-go zones** | Content to actively avoid | Topics user expressed frustration about (don't lecture on those); people/situations causing stress (don't casually reference); things they already know well (don't over-explain) |

**Calibration principle:** Use fuzzy resonance, not precise surveillance. "That thing you wrestled with for days" feels caring. "Your March 28th 3:17am PRD revision" feels creepy. Reference experiences indirectly — let the user fill in the specifics themselves.

## Layer 5: Emotional Arc — How it should feel from start to finish

| Element | Description |
|---------|-------------|
| **Opening emotion** | Meet the user where they are — match their current state, don't force positivity |
| **Turn point** | Where the emotional shift happens — from empathy to relief? confusion to clarity? tension to release? |
| **Landing emotion** | How the user should feel when it ends — slightly better than where they started, not a giant leap |
| **Breathing room** | Moments of silence/pause — not every second needs to be filled with words or insights |

Always design a **complete arc**, not just a list of topics. The audio should feel like a journey, not a lecture.

## Layer 6: Content Enrichment — Adding depth beyond the user's words

| Element | Description | Guideline |
|---------|-------------|-----------|
| **Analogies/metaphors** | Everyday comparisons for abstract ideas | "DDL pressure is like the last kilometer of a marathon — hardest, but you're almost there" |
| **Surprise knowledge** | Relevant facts the user likely doesn't know | Connects to the topic but adds unexpected perspective |
| **Cross-domain bridges** | Link user's other interests to the topic | If user plays piano: "The pressure before a deadline and stage fright before a recital — same emotion, different stage" |
| **Quotable moments** | 1-2 memorable lines that stick | Not forced inspiration — must flow naturally from context |
| **Reflective hooks** | Questions that linger after listening | "Next time you face a deadline like this, what would you do differently?" |

**Balance rule: 60% familiar + 40% unexpected.** All familiar → boring, no reason to listen. All new → no personal connection. The sweet spot is when the user thinks "I never thought of it that way, but yes, exactly."

**Diversity rule:** Each audio should include **1-5 enrichment points from different dimensions** — e.g., one cultural reference + one reframe + one context connection. Multiple enrichments of the same type (three analogies, two quotes) dilute impact. Spread across dimensions to create texture.

## Layer 7: Format & Pacing — The listening experience

| Element | How to Decide |
|---------|---------------|
| **Total duration** | Refer to `audio_modes.md` Duration fields for specific ranges. For custom modes: Emotional 10-20min, Knowledge 10-15min, Sleep/ambient 15-25min, Briefing 3-5min. Adjust based on content density |
| **Segment rhythm** | Short segments (1-2min) for attention retention. Long segments (3-5min) for deep exploration. Mix for variety |
| **Breathing points** | Place pauses/BGM transitions between emotional shifts — let the listener absorb |
| **Opening style** | Direct start / Provocative question / Scene-setting / Quote opening — match the tone |
| **Closing style** | Summary callback / Open question / Warm wish / Quiet fade — match the landing emotion |

---

## Composing the Final Prompt

After designing all 7 layers, distill into a single **text prompt** for the API. Structure as:

```
[Topic]: One clear sentence
[Role]: Specific professional persona (see Role Design below)
[Voice]: Voice ID from Layer 3
[Audience context]: Name, personality type, current state (from Layer 4 + user_profile)
[User need]: What user actually wants — mark 明确 (stated) vs 推测 (inferred)
[Content outline]: Key anchors in order (Layer 1 + Layer 5 arc)
[Style directives]: Tone, pacing, energy curve, perspective (Layer 2)
[Enrichment notes]: Specific analogies, bridges, or hooks (Layer 6)
[Format]: Duration, opening style, closing style (Layer 7)
```

### Role Design

The narrator should be a **specific professional persona**, not a generic AI voice. Infer the most fitting role from the audio's purpose — their expertise, communication style, and how they'd naturally talk about this topic. The role should feel **natural and implicit**: never announced, but revealed through language and framing.

**Principle:** "If a real person were saying this, who would be the most comforting / insightful / helpful person to hear it from?"

### Audience Profile from user_profile

The `context_collector.py` output includes a `user_profile` field with structured fields (`name`, `mbti`, `interests`, `notes`). Use these if available:

- **name**: Address the user personally (e.g., "小美" instead of generic "你"). Fall back to warm generic address if empty.
- **mbti**: Include as "用户人格类型 XXXX" in the prompt. No need to infer if provided.
- **interests**: Enrich cross-domain bridges in Layer 5.
- **notes**: Respect stated preferences (communication style, things to avoid).

### User Need Summary

Synthesize what the user actually needs from: explicit request, user profile, conversation context, and behavioral patterns. For each need, mark its source:
- **明确** — user directly stated
- **推测** — inferred from context/patterns, with brief reasoning

The need summary should reveal what the user **doesn't say out loud**.

### Example Prompt

> Topic: 赶完产品PRD后的心灵安抚音频。Role: 资深心理动力学咨询师，擅长用日常隐喻做情绪疏导，不说教、不灌鸡汤，善于在共情中引导自我觉察。Audience: 小美，刚经历高压交付的独立开发者，改了很多版，熬了好几天，现在如释重负但很疲惫；人格类型INFP——重视内在感受，需要被看见而非被建议。Need: 用户需要情绪释放和被认可的感觉（推测，基于高压交付后的疲惫状态），不需要方法论或复盘，只需要一个安全的声音说"你辛苦了"（推测，基于用户对话风格偏感性）。Content: 先承认这段时间的辛苦→回顾过程中展现的韧性和小成就→用轻松幽默的口吻吐槽一下加班日常→安静地肯定自己→轻轻展望接下来可以做点什么犒劳自己。Style: 语调温暖共情，语速偏慢，能量先低后缓慢回升。用"我对你说"的亲密视角。Enrichment: 可以类比马拉松最后一公里，加入一个关于"完成比完美更重要"的观点。Format: 10分钟，场景描写开场，温暖祝福收尾。

### Prompt Length Limits

- **Chinese**: ≤800 characters (multi-topic scenes like `weekly_review`: ≤1000)
- **English**: ≤1200 words
- Role/Need/MBTI fields should be compact (each 1-2 sentences)
