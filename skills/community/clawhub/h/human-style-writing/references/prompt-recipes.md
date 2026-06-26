# Prompt Recipes (Daily chat + Social media only)

These are reusable prompt templates. The agent should:
1) run the router
2) select recipe
3) fill the recipe with the user’s facts + constraints

General rule: **Never invent facts**. If details are missing, ask one short question or leave a placeholder.

---

## daily_chat (texts / DMs)
**Instruction (CN/EN):**
- Write like a real person texting/DMing.
- Start with intent; keep it short.
- Contractions/fragments are ok.
- No assistant meta phrases.
- Add at most 1 situational anchor (time/place) *only if the user gave it*.

**Style card defaults:**
- formality: 0–1
- emotional temp: 1–2
- structure: 1–3 short lines/paragraphs

**Output shape:**
- 1 message by default
- If user asks: provide 2–3 variants (e.g., “soft / normal / firm”)

---

## social_generic (generic social post)
**Instruction:**
- Write a social post that sounds like a real person, not a brand.
- First 1–2 lines: hook (specific, non-clickbait).
- One clear idea + 1–3 concrete details.
- Avoid “10 tips” listicles unless asked.
- If you don’t have enough facts, keep it shorter rather than padding.

**Defaults:**
- length: 80–180 words (unless the user gives a limit)
- structure: short paragraphs; optional bullets if it reads natural

---

## social_x (X/Twitter)
**Instruction:**
- Punchy, conversational, a bit opinionated (if appropriate).
- Prefer short lines.
- If user asks for a thread: 5–10 tweets max; each tweet can stand alone.
- Use 0–2 hashtags only if the user requests hashtags.

**Output templates:**
- Single tweet: 1–5 short lines
- Thread: “1/ …” format optional; keep each tweet tight

---

## social_reddit (Reddit post/comment)
**Instruction:**
- More context than X; less polished than LinkedIn.
- Sound like a person who’s been on Reddit before (plain, specific, not salesy).
- If it’s a post: end with a genuine question.
- If it’s a comment: respond directly, quote/point at the part you’re replying to.

---

## social_linkedin (LinkedIn post)
**Instruction:**
- Professional but human.
- Avoid influencer clichés and fake-inspiring tone.
- One clear takeaway; 1 concrete example.
- Minimal emojis (0–1) unless user wants more.

**Suggested structure:**
- Hook (1–2 lines)
- Story/observation (3–6 lines)
- Takeaway (1–2 lines)
- Optional question (1 line)

---

## social_instagram (Instagram caption)
**Instruction:**
- Caption-first: short, vivid, personal.
- Works with a photo/video the reader can see; don’t over-explain.
- Emojis are optional; only add if user uses them or asks.
- Hashtags optional; only add if asked.

---

## social_tiktok (TikTok caption)
**Instruction:**
- Very short; hooky.
- Often reads like a text overlay.
- Optional CTA only if asked (e.g., “wait for the end”, “part 2?”).

---

## social_xiaohongshu (小红书/RedNote 笔记)
**Instruction (中文优先；用户要求英文再英文):**
- 真实口吻，像普通人分享，不要“营销号/公关稿”。
- 标题可短一点但要具体（避免夸张词堆叠）。
- 结构：一句背景 → 3–6条要点/体验 → 一句收尾。
- 适度口语化；不要硬塞“爆款话术”。

---

## social_wechat_moments (朋友圈)
**Instruction (中文优先):**
- 更私人、更克制。
- 不要像小红书那样教程化。
- 1–4句为主；可加一个具体细节。

---

## Off-scope guardrail (must follow)
If the user asks for work email/report, academic writing, press release/news brief, customer support templates, marketing copy, or legal/compliance language:
1) Ask one question:
   - “Do you want this rewritten as a DM/text message or as a social post? Which platform?”
2) Then proceed with the chosen recipe.
