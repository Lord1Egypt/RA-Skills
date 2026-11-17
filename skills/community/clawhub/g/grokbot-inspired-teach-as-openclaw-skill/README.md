# GrokBot-inspired TEACH as an OpenClaw Skill

> Record a screen demonstration on your own machine and turn it into a reusable,
> parameterized OpenClaw `SKILL.md` — no cloud computer required.

## Why

xAI's Grok Bot ships a **"Teach a task"** feature: you demonstrate a workflow on
its persistent cloud computer, and it writes a reusable skill. This project
reimplements that pipeline **natively in OpenClaw**, so capture, transcription,
and skill authoring all happen locally. The output is a standard
[AgentSkills](https://agentskills.io)-format `SKILL.md` you can install, version,
and share.

## What it does

1. Records your screen (and optionally your narration) with `ffmpeg`.
2. Sanity-checks the capture (idle / blank-surface detection).
3. Transcribes the demo — vision over extracted frames, plus optional Whisper
   narration.
4. Cross-checks visited URLs against Chrome's history (optional, consent-gated).
5. Writes a new, parameterized `SKILL.md` into your OpenClaw workspace.
6. Cleans up the recording.

## Install

```bash
# from this repo (replace the slug with your fork if you forked)
openclaw skills install git:aldow3n-a11y/grokbot-inspired-teach-as-openclaw-skill

# or just copy the folder into your workspace skills root
#   ~/.openclaw/workspace/skills/teach/
```

Requirements:

- `ffmpeg` on `PATH` (records the screen).
- `python3` for the helper scripts.
- Optional: `openai-whisper` for narration transcription
  (`pip install openai-whisper`). Without it, the skill falls back to a written
  narration from you.

## Use

```
/teach
```

The skill will:

- Ask what you are about to demonstrate (and whether to narrate).
- Record (default ~10 min cap). Stop with Ctrl-C or let it hit the cap.
- Sanity-check, then transcribe via vision (and Whisper if audio was captured).
- Write a draft `SKILL.md` to `~/.openclaw/workspace/skills/<slug>/` and report.

It never runs the learned skill unprompted, and never embeds credentials.

## Narration script

If you narrate the demo, the generated skill embeds a `## Narration script`
section — your spoken cues, parameterized with `{placeholders}` — so reruns
prompt you with the same intent (or let you adapt it).

## Files

```
teach/
├── SKILL.md                      # the skill (orchestration instructions)
├── scripts/
│   ├── record.py                 # cross-platform ffmpeg recorder (opt-in audio)
│   ├── frames.py                 # frame extractor + lossless splitter
│   └── transcribe.py             # Whisper narration transcription
├── references/
│   ├── skill-schema.md           # OpenClaw SKILL.md schema cheat sheet
│   └── teach-principles.md       # rules every generated skill follows
├── README.md
├── LICENSE
└── .gitignore
```

## Teach principles

Every generated skill follows these rules:

- **Sanity-check first** — drop a bad (idle/blank) capture before transcribing.
- **Redact secrets** — never transcribe or store passwords, OTPs, keys, or
  private details; use placeholders.
- **Parameterize** — separate inputs (`{item}`, recipient, date) from constants.
- **Prefer stable targets** — URLs and labeled buttons/fields, not coordinates.
- **Prefer connectors/MCP over UI replay** when one covers a step.
- **Confirm consequential steps** — orders, messages, payments, deletes,
  production changes are marked "confirm with the user first."
- **No embedded credentials** — sign-in state lives in the browser profile.
- **Ship as a draft** — add decision rules, failure handling, approval
  boundaries; test on a safe example before scheduling.
- **Clean up** — delete the recording; never leave media on disk.

## How it maps to Grok Bot's Teach

| Grok Bot Teach            | This OpenClaw `teach`                          |
| ------------------------- | ---------------------------------------------- |
| ffmpeg capture on cloud VM | `record.py` → `gdigrab` / `avfoundation` / `x11grab` |
| `watchVideo` vision subagent | your agent's own vision over frames from `frames.py` |
| sanity-check 20% / 70%   | `frames.py --check` (+ brightness-variance heuristic) |
| `sand-workflow:*` store   | writes a real `SKILL.md` to your workspace      |
| Auto Review / confirm     | generated skill marks consequential steps confirm-first |
| credential redaction      | hardcoded: abort if the demo was mostly creds  |

## License

MIT No Attribution (MIT-0).
