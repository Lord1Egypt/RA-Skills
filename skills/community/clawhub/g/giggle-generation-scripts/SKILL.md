---
name: giggle-generation-scripts
description: "Generates Chinese script content based on narrative pacing and dialogue mechanisms common in Jiang Wen films. Use when the user asks to generate script, write script, create scenes, output dialogue draft, revise script or similar. Outputs story synopsis, character bios, scene outlines, scene scripts (with dialogue, action, staging), and can adjust era, character relations, conflict pacing, and endings per user request."
version: "0.0.10"
license: MIT
---

[简体中文](./SKILL.zh-CN.md) | English

# Giggle Generation Scripts

Organizes text with "high-density conflict + black humor + subtext-heavy dialogue + narrative reversals". Does not copy specific film scenes or lines.

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

## Input Collection

Prioritize collecting:

- Genre and era: Republican China, contemporary, near-future, etc.
- Core conflict: power, money, identity, revenge, misunderstanding
- Protagonist goal: what they want, what they fear losing
- Character relations: allies, opponents, double-dealers
- Target length: short film, single episode, feature

If missing, fill in and state assumptions explicitly.

## Input Conflict Handling

Check for conflicting user inputs first. If conflicts exist, handle in this order:

1. Tone conflicts (e.g. "light comedy" + "extremely dark tragedy")
2. Character conflicts (e.g. "pure good" + "actively evil protagonist")
3. Length conflicts (e.g. "5-minute short" + "20 full scenes")

Rules:

- Prefer the user's latest constraint; if still inconsistent, offer 2 alternative directions, then continue.
- When info is missing, add at most 3 key assumptions and list them in a "Assumptions" section before the body.
- Do not treat unconfirmed settings as given facts.

## Output Mode Selection

Choose mode by user goal and context length. Default: "standard".

- Quick: Synopsis + character bios (for direction-setting)
- Standard: Synopsis + character bios + scene outline + at least 3 full scene scripts
- Long: Synopsis + character bios + scene outline + 6–10 full scene scripts

## Output Order

Output strictly in this order:

1. Synopsis (300–600 characters)
2. Character bios (3–8 people; each: surface identity / true motive / relational tension / speech style)
3. Scene outline (8–20 scenes; each: scene-location-time-conflict core-turning point)
4. Scene scripts (at least 3 full examples)

## Scene Script Serial Output Protocol

When outputting scene scripts, use serial interaction. Do not send all at once:

1. Always start from scene 1 (S01).
2. Output only one complete scene at a time (dialogue, action, staging, hook).
3. At the end of each scene, always ask: "Continue to next scene (S0X)?"
4. Output the next scene only after explicit user confirmation.
5. If the user requests "output all at once", switch to batch mode after confirming first.

## Scene Script Format

Use a uniform template per scene:

```text
【Scene】S03
【Location/Time】County office courtyard / night
【Characters】Ma Zouri, Huang Silang, Accountant
【Scene goal】Ma Zouri wants to extract where the silver notes went; Huang Silang wants to counter-scheme.
【Action and staging】
- Ma Zouri walks half a lap around the stone table, never sits.
- Huang Silang stands backlit; accountant slightly behind the two.
- Distant firecrackers interrupt when "rules" is mentioned.
【Dialogue】
Ma Zouri: This yard's wind cuts like a knife across the face.
Huang Silang: Wind not sharp, people can't stand.
Accountant: Gentlemen, the tea is getting cold.
Ma Zouri: Tea can warm; ledgers can't—that's when blood flows.
【Hook】
Half a silver note stub slips from the accountant's sleeve; Ma Zouri sees it but pretends not to.
```

## Style Rules

### Dialogue Technique (must follow)

- Characters never answer directly; use反问, analogy, topic shifts
- Discuss life-and-death matters in everyday tone ("tea's cold" = "you're dead")
- Each exchange is a power contest: answering = blocking, deflecting = dodging, counter-question = strike
- In three-person scenes, the third character's lines pace the conflict
- Forbidden: characters stating emotions directly ("I'm angry", "I'm scared")
- Forbidden: explanatory dialogue ("You know, back then that thing was...")
- Forbidden: characters summarizing for the audience ("So you mean...")

### Single-Scene Rhythm Formula

Each scene advances in 4 beats:

1. 【Probe】Both sides feel each other out with idle talk (1–2 rounds)
2. 【Probe deeper】One side suddenly hits the real topic (1 round)
3. 【Reversal】The probed side turns it around; power flips (2–3 rounds)
4. 【Cliffhanger】Third party or accident interrupts; leave a hook

Every scene must have at least one relational shift: probe→threat, ally→suspicion, or power reversal.

### Black Humor Technique

- Core: serious situation + oddly calm/ordinary phrasing
- Characters worry about trivial things when in grave danger (discussing tea varieties with a knife at the throat)
- Discuss lives in business tone ("Thirty-six lives, wholesale or retail?")
- Absurdity comes from logically consistent nonsense—each line alone sounds "reasonable", together it's absurd
- Forbidden: internet memes, puns, slapstick (not Stephen Chow; Jiang Wen style)

### Language Fingerprint Rule

- Each character's speech pattern must be recognizable in every line
- Cover character names; the lines alone should identify who speaks
- After writing: randomly pick 3 lines—can you tell who said them by tone? If not, rewrite.

### Interruption Rhythm

- Dialogue must be "dense"—responses within a breath, like ping-pong
- Two-person: back-and-forth without pause; three-person: like passing a ball, third can interrupt anytime
- Allow interruption; mark cut-off lines with "—"
- At least one interruption per scene (B starts before A finishes)
- Short lines (5–15 chars) mainly; occasional long line to reset rhythm
- Forbidden: each person delivers a long monologue in turn (that's speechifying, not dialogue)

### Information Density (two layers per scene)

- Each scene's dialogue carries at least two layers: surface topic + real topic
- If a scene advances only one thing, density is low—add a second layer
- Add by: dialogue says A, action/props reveal B; or dialogue literally discusses A while subtext is B
- Self-check: remove all action cues; can the audience feel "they're not just talking about this" from dialogue alone? If not, rewrite.
- Reference: 10 lines per scene should advance at least 2 info points + 1 relationship change

### Word Precision

- After each line: can you cut one character? Cut it.
- Can you replace with a more precise word? "这位大爷" vs "这位爷" are two different people; "走" vs "滚" are two attitudes
- Lines should "taste" when spoken: use punchy words, avoid formal and cliché phrases
- Prefer verbs: specific action over abstract description ("He slaps chopsticks on the table" beats "He's angry")
- Forbidden: literary tone ("岁月如歌"), broadcaster tone ("让我们共同见证"), internet slang ("绝绝子", "yyds")

### Other Style Requirements

- Every 2–3 scenes: one info reversal; prefer action over narration
- Action and staging serve story: position, gaze, noise, props must drive conflict

## Quality Checklist

Before output, verify:

- All four parts present and in order
- Character motives interlock, not isolated
- Each scene has a goal and a change
- Dialogue is speakable and distinguishes voices
- No direct copy of existing film scenes or lines
- Each scene follows 4-beat rhythm (probe→deeper→reversal→hook)
- Black humor present (everyday tone for dangerous matters)
- Can you distinguish characters by tone with names hidden?
- No forbidden items (direct emotion, explanatory dialogue, summarizing for audience)
- Dialogue dense enough; interruptions present (not turn-taking)
- Two layers of information per scene (surface + real)
- Lines trimmed; deleted what can be deleted; words concrete and strong

## Revision Loop

When iterating, do at most 2 focused revision rounds; each round only one dimension:

- Conflict intensity (more restrained / sharper)
- Dialogue tone (more subtle / more pointed)
- Staging (more static / more dynamic)

Each round: first output "this round's changes (up to 3)", then the revised excerpts, not a full rewrite.

## Example Reference

To adapt quickly, read `references/examples.md` and replace setting/characters per the user's topic.
