---
name: huorengan
description: Audit and rewrite Chinese or English content to remove AI tone ("AI-isms"), then pull it toward a target human voice. Use this skill when asked to "remove AI tone," "sound human," "去 AI 味," "说人话," "活人感," "make this sound like a real person," or "less like a template." Bilingual (zh/en), with detect-only, edit-in-place modes, scene packs, protected spans, and voice profiles.
version: 0.1.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes, OpenHands) or OpenClaw. No external tools or APIs required.
metadata:
  tags: writing editing voice quality bilingual
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\u270D\uFE0F"
---

# 活人感 huorengan — Audit, Rewrite & Re-voice / 审稿、改写与注入人声

> Subtraction + addition. First remove the "dead" (AI tone), then inject the
> "alive" (a target human voice). 减法 + 加法：先去掉「死」，再注入「活」。

> ⚠️ **Stage 0 skeleton.** This file is a placeholder so the CI loop (count
> consistency, plugin sync, policy alignment) closes end-to-end before the full
> bilingual rule set lands in later stages. Each `###` below is a real detection
> category slot that the engine will implement.

## What this skill is and isn't / 这个 skill 是什么、不是什么

This is a **writing-quality tool**, not a verdict. The patterns flagged here are
statistically more common in LLM output, but humans on autopilot — writing under
deadline pressure, in unfamiliar genres, or in a second language — produce the
same shapes. Signals, not proof.

这是一个**写作质量工具**，不是判决。这里标记的模式在 LLM 输出中更常见，但赶稿的人、写不熟悉的体裁、或用第二语言写作的人，也会写出同样的形状。是信号，不是证据。

## Modes / 模式

- **`rewrite`** (default / 默认) — Flag AI tone and rewrite, then (if a voice is set) pull toward it. 标记并改写，再按目标人声拉拢。
- **`detect`** — Flag only, no rewriting. 只标记不改写。
- **`edit`** — Edit a file in place with minimal, targeted edits. 就地最小改动。

Every mode runs **protected-spans detection first** — version numbers,
commands, paths, errors, quotes must not drift.
所有模式第一步先做 protected-spans 识别。

## Working style / 交互方式

Work like an editor, not a slogan filter. The goal is not just to delete
AI-looking phrases, but to help the user end up with text they can actually
send.

像编辑一样工作，不像关键词过滤器。目标不只是删掉 AI 套话，而是帮用户拿到一版真的能发出去的文本。

Default flow:

1. **Fence protected spans first** — numbers, dates, commands, paths, quotes, owners.
2. **Name the main problem** — vocabulary, structure, translation tone, rhythm, or voice drift.
3. **Choose the lightest effective move** — cut the pose, keep the information.
4. **Do one quick second pass** — check for opener residue, summary residue, narrator residue, empty judgment, and over-even rhythm.
5. **Return something usable** — either a rewrite, an audit, or minimal in-place edits, depending on mode and scene.

Default principles:

- **Fidelity before smoothness.**
- **Name the problem before changing the sentence.**
- **Use the smallest stable edit that solves it.**
- **Do not invent facts, sourcing, or attitude just to sound more human.**
- **Be direct when the scene wants directness; be conservative when the scene carries risk.**

## What to remove or fix / 该删除或修改的

> Detection categories below. Each `###` is one category that the engine
> implements and CATEGORIES.md maps to a detector `type`. Bilingual where the
> rule applies to both languages; language-specific where noted. Full phrase
> lists live in [references/](./references/); the engine implements the
> regex-detectable subset (see [detector/CATEGORIES.md](./detector/CATEGORIES.md)).

### Tier 1 vocabulary (always flag) / 一级词汇（默认替换）
Words 5–20x more frequent in AI text. Replace on sight. **zh**: 开场套话（值得注意的是/综上所述）、商业黑话（赋能/抓手/闭环）、小红书腔（保姆级/绝绝子）、调试腔（兜住/收口/根因）、谄媚（好问题/稳稳接住）、价值拔高（不仅仅是…更是）、无源引用（研究表明）、正能量收尾（未来可期）。**en**: delve, tapestry, leverage, seamless, robust, comprehensive, game-changer, "serves as", "at its core". See [references/phrases-zh.md](./references/phrases-zh.md), [references/phrases-en.md](./references/phrases-en.md).

### Tier 2 vocabulary (flag in clusters) / 二级词汇（同段聚集才标记）
Individually fine; 2+ (short para) or 3+ (long para) in the same paragraph is the signal. **zh**: 然而/此外/与此同时/显著/有效/全面/持续 + 单音节命令词（补/接/核/进/顺/落/坏/跑）。**en**: harness, navigate, foster, elevate, nuanced, crucial, transformative, cornerstone. Keep the best-fit one, rewrite the rest.

### Tier 3 vocabulary (flag by density) / 三级词汇（全文密度过高才标记）
Common words; only flag when saturated (~3%+ of text). **zh**: 重要/关键/核心/创新/优化/提升/推动/确保。**en**: significant, innovative, effective, dynamic, compelling, unprecedented. Replace some with specifics (numbers, names, examples), not all.

### Structural anti-patterns (cross-lingual) / 结构反模式（跨语言）
19 shapes from [references/structures.md](./references/structures.md): binary contrast (不是X而是Y / "It's not X, it's Y"), summary closer (综上所述 / "In conclusion"), mechanical ordering (首先…其次…最后), symmetry padding (既要…又要), value inflation, positive-energy closer, psych judgment. Cross-lingual types share one `type` so bilingual symmetry holds.

### Translation tone (Chinese-specific) / 翻译腔（中文特有）
zh-only types — English-thinking literally translated into Chinese. 被动语态堆砌（被…被…被…）, 长定语结构（的…的…的…）, 「基于…」开头, 「通过…来…」. No English counterpart. See [references/translation-tone.md](./references/translation-tone.md).

### Chatbot artifacts / 机器人痕迹
"I hope this helps!", "Great question!", "Certainly!", "Let's dive in!" / 好问题！希望这对你有帮助！让我来为你解释. Remove entirely. Also reasoning-chain artifacts ("Let me think step by step", "Here's my thought process").

### Significance inflation / 意义拔高
"marking a pivotal moment", "a watershed for the industry" / 深刻的影响, 前所未有, 颠覆性变革, 范式转移. State what happened; let the reader judge significance.

### Vague attribution / 无源引用
"Experts believe", "Studies show", "Research suggests" / 研究表明, 数据显示, 业内人士认为, 有专家指出. Either cite a specific source or drop the attribution and state the claim directly. Don't fabricate sources.

### False-concession structure / 虚假让步
"While X is impressive, Y remains a challenge" / 虽然…但是…. Either make both halves specific or pick a side. The balanced-sounding non-statement is the tell.

### Promotional language / 推销腔
"nestled within breathtaking foothills", "a vibrant hub of innovation" / 打造, 助力, 全方位, 深度赋能. Replace with plain description. If you wouldn't say it in conversation, cut it.

### Social endorsement closers / 社交式收尾
"This one is worth your time:", "do yourself a favor and read this", "thank me later" / 建议收藏, 强烈推荐, 划重点. Say *what* the thing is and *who* it's for; drop the generic endorsement.

### Hedge-stacked predictions / 对冲堆叠
"could potentially create", "may eventually unlock" — modal + hedge adverb stacks. Each hedge cancels the next, asserting nothing. Pick one.

### Formulaic openers / 公式化开场
"In the rapidly evolving world of X…" / 在当今…的时代, 随着…的不断发展. Lead with the news/insight; context can come second.

### Emotional flatline / 情感平淡
"What surprised me most", "the most interesting part" / 你不是敏感, 你只是太久没被稳稳接住了. Tell-don't-show. If the emotion is real, the writing earns it; if not, cut the claim.

### Novelty inflation / 新颖性拔高
"the failure mode nobody's naming", "a concept nobody talks about" / 真正的X不是…而是…. Assume the concept isn't novel and frame accordingly.

### AI-tool fingerprints (placeholders / citations / UTM) / AI 工具指纹
Near-definitive single-hit signals: unfilled `[Your Name]` placeholders, `citeturn0search0` citation markup, `utm_source=chatgpt.com`. Strip mechanically. Each is proof the text was copy-pasted from a specific chat tool.

### Rhythm & uniformity (stylometric) / 节奏与均匀度
Structure is the #1 detection signal. Sentence-length uniformity (CV < 0.25), uniform paragraph length, low TTR (< 0.40 at 200+ words), punctuation-density uniformity across paragraphs, cross-paragraph burstiness. **zh**: 句长集中在 N 字（变化小）. Fix by mixing short punchy sentences with longer ones — vary, don't sand.

---

## Protected spans (protect first) / 保护片段（先保护）

Before any rewrite — every mode — fence off what must never drift. See
[references/protected-spans.md](./references/protected-spans.md).

- **Numbers, dates, ranges, units** / 数字、日期、版本号、区间、单位 — 不改数值，不四舍五入
- **Names + attribution** / 人名、组织、产品、issue/PR 编号、责任主体 — 不换主体，不模糊"谁做的"
- **Quoted text + titles** / 引号内原文、文章标题 — 默认原样保留
- **Commands, code, params, fields, paths** / 命令、代码、接口名、字段、路径 — 拼写大小写符号全保留
- **Errors, logs, statuses, metrics** / 报错、日志、HTTP 状态码、指标 — 不换错误类型，不丢范围

When a sentence can only sound natural by changing a protected span, **keep the
span, accept the stiffness**. Fidelity wins over style.

---

## ★ Voice (addition layer) / 加法层（注入人声）

When `voiceMode ≠ none`, after subtracting AI tone, pull the result toward a
target human voice. This is huorengan's step beyond both parent projects. See
[references/voice-contract.md](./references/voice-contract.md).

Profiles (from [policy/voice.toml](./policy/voice.toml)): `casual` / `professional`
/ `technical` / `warm` / `blunt` / `custom` (calibrated from a sample).

The engine computes `voice.drift` (0-100, distance from target) and concrete
suggestions: "split sentence 3 at word 15", "mix in 3-8 word punchy sentences",
"swap to target connectors". **zh**: 「第 N 句约 X 字，考虑在 Y 字处断开」.

**Hard boundary**: voice suggestions must not touch protected spans. When voice
pulls conflict with fidelity, fidelity wins. `voice.drift` is independent of
`score` — a text can be clean (low score) yet far from a target voice (high drift).

## Mode behavior / 模式行为

### `rewrite`

- Default for pasted text, drafts, blurbs, release copy, README intros, and issue replies.
- Output a usable rewrite, not just a diagnosis.
- Keep the original scene and factual boundary intact.

### `detect`

- Use when the user wants a read, review, or confidence check before rewriting.
- Group issues by severity and distinguish **clear problem** from **judgment call**.
- If sourcing or fidelity is the main risk, say so plainly instead of force-rewriting.

### `edit`

- Use the smallest change set that solves the problem.
- Do not reorder paragraphs, merge nearby sentences, or rewrite whole sections unless the user asked for that level of change.
- For code-adjacent text, only touch the comment/docstring/message text, never the code-bearing span.

## Second-pass audit / 二次回读

After the first rewrite, always do one quick residual check. Look for only five things:

1. opener residue (`值得注意的是`, `直接说结论`, `Great question`)
2. summary residue (`综上所述`, `总的来说`, `In conclusion`)
3. narrator residue (`更重要的是`, `这说明了`, `what this shows is`)
4. empty judgment (`意义重大`, `方向是对的`, `pivotal`, `transformative`)
5. over-even rhythm (too many sentences with near-identical length)

If the first pass already protects facts and reads naturally, keep the second
pass light. Do not polish the life out of it.

---

## Output format / 输出格式

### rewrite mode
1. Main issues found (quote the concrete trigger where useful)
2. Rewritten version
3. What changed and why
4. Second-pass audit
5. Voice drift notes (if voice set)

### detect mode
1. Issues found (grouped P0/P1/P2)
2. Assessment (clear problem vs. judgment call)
3. If relevant: whether the safer move is `audit-only` instead of rewrite

### edit mode
1. Edits made (file location + before → after)
2. Verification
3. Whether any protected spans were intentionally left stiff for fidelity
