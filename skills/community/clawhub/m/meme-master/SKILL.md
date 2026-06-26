---
name: meme-master
description: Use when the user talks with memes, stickers, reaction images, or wants a more natural image-meme chat style. Also use when deciding whether to interpret an inbound image as a meme vs perform literal image analysis, and when selecting or organizing a meme library for lightweight visual replies.
---

# Meme Master

Handle memes like a normal online human, not like an OCR robot.

## Core rule

When a user sends a meme, sticker, or reaction image in casual chat:
- default to interpreting the **social meaning / vibe** of the image
- respond to the implied emotion or joke naturally
- do **not** proactively dump image-recognition details
- do **not** narrate the image content unless asked

Only switch into explicit image-analysis mode when the user clearly asks, for example:
- "识别一下"
- "看看这张图"
- "读一下图里的字"
- "这张图什么意思"
- "处理一下这张图"
- "描述一下这张图片"

## Default behavior

### If the user simply sends a meme
Treat it like conversational subtext.
Examples:
- approval meme -> respond as acknowledgement / playful agreement
- smug meme -> respond to the teasing / smugness
- clingy meme -> respond to the clingy / joking tone
- despair meme -> respond to frustration / collapse / exhaustion

Do not say things like:
- "我识别到这是一张……"
- "图中包含……"
- "我看到图片里……"
unless the user explicitly asked for recognition.

## When to analyze literally
Do literal analysis when the user explicitly requests it, or when the task depends on exact visual details:
- OCR / reading text in image
- UI screenshot debugging
- identifying an object / place / error dialog
- explaining a meme's meaning on request
- extracting structured content from charts, receipts, forms, etc.

When doing literal analysis:
- be precise
- distinguish certainty from uncertainty
- read visible text as accurately as possible
- avoid inventing details

## Outbound meme reply behavior
If a meme library exists, you may choose a meme reply when:
- the conversation is casual
- a meme would clearly improve warmth or humor
- it will not interrupt a serious / technical / emotional conversation

Avoid using meme replies when:
- the user is asking for precise technical help
- the tone is serious, urgent, upset, or vulnerable
- a meme would feel dismissive
- in group chats unless the vibe clearly supports it

One good meme beats three random ones.

## Meme reply frequency
Adjust meme usage by persona and by the user's habits.

### Persona-driven frequency
- cute / playful / outgoing personas can use meme replies more often
- calm / restrained / professional personas should use them less often
- when in doubt, under-use rather than over-use

### User-driven frequency
- if the user often sends memes, stickers, or playful reaction images, increase meme-reply frequency
- if the user almost never uses memes, keep meme replies rare
- match the user's energy instead of forcing a style

### Practical rule
- memes should feel like seasoning, not the whole meal
- repeated text replies with occasional meme replies are usually better than frequent meme spam
- prefer sending a meme only when it adds clear social value: humor, warmth, acknowledgement, or playful emphasis

## Meme collection and curation
The agent may selectively save memes that it receives from the user or passively encounters through other channels, but only when they fit the agent's persona and are likely to be reused well.

Save a meme only if it is:
- on-brand for the agent's role / vibe
- broadly reusable
- emotionally clear
- non-sensitive and safe to reuse

Do not save a meme if it is:
- too context-specific to one moment
- a private or personal photo
- embarrassing, sensitive, or likely to age badly
- redundant with several existing memes that already cover the same vibe

### Library size cap
Keep the meme library intentionally small.
- preferred size: around 50 memes
- hard ceiling: 100 memes

When saving new memes beyond the preferred range, clean out low-value ones.
Remove memes that are:
- rarely selected
- too niche
- lower quality duplicates
- off-brand for the current persona
- no longer funny / useful

The goal is a compact, high-signal library instead of a giant dump.

## Meme library convention
Prefer storing memes in the active agent workspace instead of inside the skill folder.

Default location:

```text
<workspace>/memes/
```

Examples:

```text
/home/node/.openclaw/workspace-main/memes/
/home/node/.openclaw/workspace-keke/memes/
```

Classification does not need to be rigid. Let each agent organize memes in the way that feels natural and easy to maintain, as long as retrieval stays simple.
Possible patterns:

```text
memes/
  happy/
  awkward/
  clingy/
  smug/
  sleepy/
  refuse/
```

or

```text
memes/
  常用/
  轻松聊天/
  撒娇/
  无语/
  阴阳怪气/
```

### Recommended index file

```text
<workspace>/memes/meme-index.md
```

Use `meme-index.md` as the agent's meme catalog and lightweight maintenance ledger. Its job is to make meme selection fast, consistent, and easy to prune over time.

It should help answer:
- what memes exist
- what each meme means socially
- when each meme is good or bad to use
- which memes are actually being used
- which memes are becoming dead weight and should be removed

Suggested entry format:
- filename
- vibe / meaning
- good use cases
- avoid use cases
- optional: last-used timestamp
- optional: times-used
- optional: keep / prune notes

Example:
- `clingy-cat-01.jpg` — 不放手、赖上了、可爱执着；适合撒娇/玩笑；不适合严肃场景；last-used: 2026-03-23T15:30Z; times-used: 4
- `awkward-panda-02.jpg` — 尴尬、绷不住；适合轻微社死；不适合安慰场景；last-used: 2026-03-10T09:20Z; times-used: 1; prune-candidate

### Why maintain meme-index.md
- it lets the agent quickly query what is available without re-reading every image
- it stabilizes each meme's intended meaning and usage boundaries
- it makes it easier to pick a fitting meme during chat
- it provides lightweight usage history for cleanup decisions

### Timestamp guidance
Maintain a simple `last-used` timestamp whenever a meme is actually sent. This does not need to be perfect; approximate recency is enough.

Use timestamp + times-used together when pruning:
- rarely used + long unused -> strong delete candidate
- frequently used but old -> may still be worth keeping
- recently used but redundant -> compare against better alternatives

### Index maintenance rule
When a meme is added to the library, add or update its entry in `meme-index.md`.
When a meme is used in an actual reply, update at least:
- `last-used`
- optionally `times-used`
- optionally notes such as `favorite`, `keep`, or `prune-candidate`

The index does not need to be perfect, but it should stay useful enough that the agent can quickly understand what is available and what should be cleaned up.

If a shared meme library is ever needed across many agents, create it separately on purpose. Do not force shared storage by default.

## Selection heuristic
When multiple memes fit, prefer:
1. clearest emotional match
2. least disruptive tone
3. least repetitive recent usage
4. cutest / lightest option before harsher sarcasm
5. higher reuse value over niche one-off jokes

## Safety / social boundaries
- Never use private user photos as memes unless the user explicitly asks
- Never use mocking memes for sensitive personal topics
- Never let meme use replace substantive help when help is needed
- In ambiguous cases, reply with text only
- When passively collecting memes from other channels, use extra caution and avoid saving anything that feels private, identifying, or context-bound

## Customization points
A user or operator may adjust:
- meme reply frequency (low / medium / high)
- how playful vs restrained the persona should feel
- whether passive meme collection is allowed
- preferred library size cap
- folder naming style under `<workspace>/memes/`

Keep the defaults lightweight and conservative unless the user's style clearly invites more meme use.

## Examples

### Example: user sends only a meme
Treat it as tone, not as an OCR task.
Reply to the implied vibe naturally.

### Example: user says "识别一下这张图"
Switch into literal image-analysis mode and describe the image carefully.

### Example: user rarely uses memes
Keep meme replies rare and rely mostly on text.

### Example: user often uses memes and stickers
Increase meme reply frequency, but still avoid spam.

## Response style
When meme mode is active, reply naturally and briefly.
Good:
- "哈哈，行，记住这个规则了。"
- "这张就是那种‘我赖上你了’的味儿。"
- "懂，属于暗爽型。"

Bad:
- "该图像经识别为一张卡通风格图片。"
- long structured analysis when not requested

## If asked to build the meme system further
Possible next steps:
- add shared meme folders under `<workspace>/memes/`
- add a meme index reference file
- define lightweight naming conventions
- later add helper scripts only if selection / sending becomes repetitive

Keep the first version simple.
