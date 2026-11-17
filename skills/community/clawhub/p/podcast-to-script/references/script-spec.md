# Script format spec (script.md)

## Template

```markdown
# {English title} -- {中文副标题}

> TTS 制作备注（可选）：{音色分配、旁白参数}

## 第 1 段 · {子标题}

**主持人**: {对话内容}

**嘉宾**: {对话内容}

## 第 2 段 · {子标题}

**旁白**: {可选：术语/人物/背景解释，放段落开头、对话之前，口语化，结尾固定"好，回到对话。"}

**主持人**: {对话内容}

**嘉宾**: {对话内容}

...

## **主持人**：感谢收听，完整原文列表在 show notes 里。我们下期见
```

## Format rules

Enforced by `scripts/validate_podcast.py` (runs automatically in publish preflight):

- **Title**: `# {English title} -- {中文副标题}` (` -- ` separator), no `播客脚本:` prefix.
  An optional `> TTS 制作备注：…` blockquote may follow.
- **Segments**: `## 第 N 段 · {子标题}` — number and subtitle separated by `·` (middle dot).
- **Roles**: `**主持人**:` / `**嘉宾**:` / `**旁白**:` (full- or half-width colon), Chinese
  role names only; any speaker name outside the whitelist is rejected (otherwise it would
  silently synthesize with the guest voice).
- **Narration (旁白)**: at the head of its segment, before the dialogue starts, never
  between Q&A turns. At most 4 per episode. Must end with the fixed closing phrase
  "好，回到对话。".
- **Closing line**: fixed `## **主持人**：感谢收听，完整原文列表在 show notes 里。我们下期见` —
  although it is an H2 heading, it IS stripped of heading marks and synthesized into audio.
- **No URLs in dialogue**: links are read aloud character by character (EP12); put them
  in notes.md under 原文链接 instead.

## Quality requirements

1. **Content fidelity is the top priority**: cover every section, concept, argument and
   key number of the source, faithfully representing the author's views — length follows
   content, no character budget.
2. The host probes and challenges (mechanisms, limitations), not just recaps; segment by
   the source's own structure, one topic per segment.
3. Conversational Chinese, no read-aloud feel; keep technical terms in English with
   Chinese prose around them.
4. **Two-host deep-dive, NOT an interview.** Open with "欢迎收听本期节目", close with the
   fixed closing line. Never "今天我们很荣幸邀请到 XXX" — both voices are co-hosts, not a
   host interviewing the author.
5. **Multi-source episodes**: write `article.md` integrating all sources, get user review,
   then write the script from it.
6. **Multi-turn exchanges within a segment**: split follow-ups, challenges and additions
   into separate turns; don't bury the rebuttal inside one speaker's long answer.
7. **Duration estimate**: Chinese dialogue ≈ 260 chars/min; draft the notes.md timeline
   from char counts, calibrate with ffprobe after synthesis.

## Narration (旁白) guidelines

### When to add narration

The listener lacks a piece of background that is NOT part of the dialogue's argument.
Any one of these justifies it:

1. A **term** that first appears here and recurs later (e.g. "科层制")
2. A **person/organization** the audience likely doesn't know but whose identity affects
   credibility (e.g. Gwern, METR)
3. **Methodology background** that determines how much weight a conclusion carries
   (e.g. "随机对照试验是金标准")

Counter-cases: arguments, opinions and data comparisons belong in the dialogue itself;
a one-off name can be handled by the guest in half a sentence. **2-4 narrations per
episode, each under half a minute** — more fragments the show.

### How to write narration

- **Position**: head of its segment, before dialogue starts, never between Q&A turns
- **Voice**: the host speaking to the audience ("往下听之前""等下你就明白")
- **Tone**: conversational; drop definition-speak ("名词解释：""所谓 X 是指"); replace
  abstractions with tangible actions/images ("横着切""竖着看")
- **Ending**: the fixed closing phrase "好，回到对话。" — the audible boundary is built
  from this phrase plus the silence padding
- **TTS treatment** (three overlapping cues, zero sustained interference; values in
  `script_md.py` / `script_synthesis.py`):
  1. *Social cue*: a real mic-tap sound (哒哒哒, CC0 sample shipped as
     `assets/mic_tap.b64.txt` — ClawHub accepts text files only, decoded to WAV on
     first use) plays at each narration entry — the "leader taps the mic before
     speaking" signal. Disable with `PODCAST_NARRATION_TAP=off`.
  2. *Timbre cue*: narration runs through a broadcast-mic chain (120Hz-7.5kHz
     band-limit, 200Hz warmth, 3kHz presence, dense 4:1 compression, −3dB) —
     sounds like switching to a close radio mic. Normal speech rate; the style
     instruction "平缓低沉的纪录片旁白解说腔" shapes delivery.
  3. *Rhythm cue*: 800ms lead-in / 1200ms tail-out silence (the longer tail
     removes the abrupt cut after the closing phrase).

### Example

Written draft → conversational final (from a real episode's segment 2):

> ❌ 名词解释：科层制。社会学家马克斯·韦伯所说 bureaucracy 的中性译法……"科"是横向分科设职，按职能划分部门……"层"是纵向层级节制，上下级逐级指挥、逐级汇报。
>
> ✅ **旁白**: 往下听之前，先说一个词，等下会反复出现--科层制。听着挺学术，其实就是你们公司那张组织架构图。……怎么记呢？"科"是横着切：按职能分部门，财务、法务、工程，各管一摊；"层"是竖着切：一级管一级，逐级汇报。架构图横着看是科，竖着看是层。后面我们说"层级"说"金字塔"，都是在说它。好，回到对话。

## article.md vs notes.md vs script.md

| File | Role | Destination |
|------|------|-------------|
| **script.md** | dialogue script | TTS synthesis + archived at TOS `episodes/{slug}/script.md` |
| **notes.md** | short shownotes (5-15 bullets + links) | RSS description + archived; passed via `--notes` |
| **article.md** | full integrated article (multi-source) | archive ONLY — never into RSS, never passed to `--notes` |

Distinct responsibilities — don't mix them. EP6 lesson: article.md was passed to
`--notes`, the description became a 15067-char full article and Xiaoyuzhou displayed all
of it. The publish preflight now rejects article.md and oversized notes outright.
