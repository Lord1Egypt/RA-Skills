# Model Routing - MiniMax

Use this file when the user says "which MiniMax model?" or when the workflow is drifting because the platform surface is being treated as one undifferentiated API.

## Routing Order

1. Name the modality first:
- text
- speech
- video
- music
- MCP-assisted text workflow

2. Decide the optimization target:
- quality-first
- speed-first
- balanced
- compatibility-first

3. Pin the exact model family or service:
- `MiniMax-M2.5` for strongest current text quality when latency is acceptable
- `MiniMax-M2.5-highspeed` when the user needs faster text turnaround
- `MiniMax-M2.1` for balanced text generation and code-oriented work
- `MiniMax-M2.1-highspeed` for faster balanced text work
- `MiniMax-M2` as an older compatibility or fallback lane when the integration surface still expects it
- `speech-2.8-hd` when speech quality matters more than speed
- `speech-2.8-turbo` when faster speech delivery matters more than top-end quality
- `Hailuo 2.3` for motion-heavy video generation where timing and scene energy matter
- `Music 2.5` for music-first generation flows

## Practical Defaults

### Text
- Start with `MiniMax-M2.5` unless the user explicitly prioritizes lower latency.
- Use the `highspeed` tier for rapid tool loops, draft generation, or latency-sensitive UI calls.
- Verify live availability before hardcoding older families in production.

### Speech
- Use HD for final narration, premium demos, or voice-sensitive outputs.
- Use turbo for previews, iterative drafting, and low-latency checks.
- Align language, voice, and output format before tuning prompt style.

### Video and Music
- Treat these as queued jobs, not chat completions.
- Plan polling, timeout, and fetch logic before tuning prompts.
- Keep a clear record of reference assets, duration targets, and output URLs.

## Routing Questions That Matter

Ask only the questions that change the answer:
- Is this text, speech, video, music, or tool-assisted orchestration?
- Is the user optimizing for quality, speed, cost, or compatibility?
- Is the integration already locked to an Anthropic-compatible or OpenAI-compatible SDK?
- Does the user need a repeatable production recipe or a fast experiment?

## Common Mistakes

- Choosing a compatible interface first and only later picking the model.
- Using quality-first models in latency-critical loops without checking response budget.
- Treating video and music as if they will return like text.
- Forgetting that live model menus can change, which breaks stale pinned lists.
