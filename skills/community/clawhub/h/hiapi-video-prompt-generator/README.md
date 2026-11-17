# Video Prompt Generator Skill

Turn briefs and sources into controlled, source-grounded video prompts that run on HiAPI Seedance 2.0 or HappyHorse 1.0.

**Video Prompt Generator • HiAPI Handoff • [HiAPI](https://www.hiapi.ai)**

> This skill itself does not need an API key. `HIAPI_API_KEY` is only required for the target render skill ([Seedance 2.0](https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill) or [HappyHorse 1.0](https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill)).

[HiAPI Docs](https://docs.hiapi.ai) · [All HiAPI Skills](https://github.com/HiAPIAI/hiapi-skills) · [Remote MCP](https://docs.hiapi.ai/for-ai/) · [Pricing](https://www.hiapi.ai/en/pricing) · [Get API Key](https://www.hiapi.ai/en/register)

Languages: [English](README.md) | [简体中文](README.zh-CN.md)

> **HiAPI Matrix:** 🎨 [Image Prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) · 🎬 [Video Prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts) · 🛠️ **Agent Skills (you are here)** · 🤖 [Remote MCP](https://docs.hiapi.ai/for-ai/) · 📖 [API Docs](https://docs.hiapi.ai)

---

> AI Agent? Skip the README and read [llms-install.md](llms-install.md). It contains installation steps and the agent contract for this skill.

---

## What Is This?

A prompt-engineering skill for OpenClaw / Claude Code / OpenCode / Codex-style agents. After installation, your agent can take a one-line idea, a product link, or a research topic and return a **directed video prompt** ready to paste into one of HiAPI's video skills.

This skill produces prompts. It does not call a video API by itself. The output is built to plug into:

| Target | When to use |
| --- | --- |
| [hiapi-seedance-2-0-video-skill](https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill) | Text-to-video and image-to-video, cinematic quality, 4–15 seconds |
| [hiapi-happyhorse-1-0-video-skill](https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill) | Fast text-to-video drafts |

A directed prompt specifies what appears, what moves, what is typed, what is heard, and what the model must not show. Every key fact in the source appears on screen, in narration, or as a labeled visual cue.

---

## Where This Fits

Use this skill when the brief is too short, the source has not been read closely, or the user has produced a vague prompt and expects a generic video back. If the user already has a final, scene-by-scene prompt, skip this skill and call the target video skill directly.

For a library of proven Seedance 2.0 prompts to anchor on, see [awesome-seedance-2-0-prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts).

---

## Install

### One Command (Recommended)

```bash
npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y
```

The installer auto-detects Codex (`~/.codex/skills`) and Claude Code (`~/.claude/skills`). To target a specific agent or directory:

```bash
npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --codex          # ~/.codex/skills only
npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --claude         # ~/.claude/skills only
npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --target=/path   # custom directory
AGENT_SKILLS_DIR=/path npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y
```

### OpenClaw

```bash
openclaw skills add https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill
```

### Manual Install (Any Agent)

```bash
git clone https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill.git
export AGENT_SKILLS_DIR="/path/to/your/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-video-prompt-generator "$AGENT_SKILLS_DIR/hiapi-video-prompt-generator"
```

### Agent Auto-Install Prompt

```text
Install the HiAPI Video Prompt Generator skill:

1. Run: npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y
   (auto-detects Codex / Claude Code skill directories)
2. Read SKILL.md for the output contract.
3. After this skill returns a prompt, run it through one of:
   - https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill
   - https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill
```

---

## How To Use

Talk directly to your AI agent:

> Use `$hiapi-video-prompt-generator` to turn https://github.com/HiAPIAI/hiapi-skills into a 5-second product intro.

> Use the HiAPI Video Prompt Generator to plan a 9:16 social short about why agent skills beat one-shot prompts.

> Use `$hiapi-video-prompt-generator` to plan an 8-second image-to-video from `outputs/product.png`, soft camera, studio lighting.

This skill returns a structured prompt with scene-by-scene direction and a ready-to-paste command for the target HiAPI skill.

---

## Output Contract

Every skill run returns these sections, in order:

1. **Video Type** — product demo, teaching short, social short, explainer, pitch, historical, or visual concept.
2. **Target Model** — `hiapi-seedance-2-0-video` or `hiapi-happyhorse-1-0-video`, with one reason.
3. **Duration And Aspect** — picked from the chosen target's allowed list. Seedance: any integer from `4` to `15` seconds + `--ratio` ∈ `16:9|9:16|1:1|4:3|3:4|21:9|adaptive`. HappyHorse: any integer from `3` to `15` s + `--size` ∈ `16:9|9:16|1:1|4:3|3:4`. The output names the right flag.
4. **Core Objective** — single sentence the viewer should remember.
5. **Source Extraction Summary** — 5–10 bullets. Real facts are tagged `[source]`; only staging choices (camera, layout, lighting, transition copy) may be tagged `[creative assumption]`. Guesses are never tagged as sources.
6. **Narrative Through-Line** — one-sentence arc.
7. **Scene Prompts** — time, visual, on-screen text, action/camera, narration, transition.
8. **Required Screen Text** — every exact quoted string.
9. **Motion And Camera Control** — dominant and ambient motions.
10. **Style Requirements** — color, lighting, typography, mood.
11. **Negative Constraints** — what the model must not show.
12. **Final Copy-Ready Prompt** — a compact block to paste into `--prompt`; must keep scene order with time cues (e.g. `[0–1.2s]`), all Required Screen Text strings verbatim, dominant motions, and at least one Negative Constraint.
13. **Handoff Command** — one `cd` line into the installed target skill directory, then the exact `node scripts/...` line with all parameters filled (Seedance uses `--ratio`, HappyHorse uses `--size`).

See [`SKILL.md`](SKILL.md) for the full agent contract and [`references/`](references/) for the patterns and source-extraction guidance.

---

## Defaults The Skill Enforces

- **Duration**: defaults to `5` seconds. This skill never produces a `30`-second plan, because HiAPI's video models do not run that length.
- **Aspect**: `16:9` for demos and explainers, `9:16` for social shorts.
- **Image-to-video**: only on Seedance 2.0. The starting image is passed as `--first-frame-url`. HappyHorse 1.0 is text-to-video only.
- **Model-specific parameters** — this skill constrains the handoff to the chosen target's actual API:

| Model | Durations (`--seconds`) | Resolutions | Aspect flag |
| --- | --- | --- | --- |
| Seedance 2.0 | any integer from `4` to `15` | `480p`, `720p`, `1080p` | `--ratio` ∈ `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, `adaptive` |
| HappyHorse 1.0 | any integer from `3` to `15` | `720p`, `1080p` | `--size` ∈ `16:9`, `9:16`, `1:1`, `4:3`, `3:4` |

If the user asks for an unsupported duration or ratio, this skill offers the closest supported value and notes the change in the output.

### Why 5s Instead Of The Upstream 30s Default

This skill is inspired by the upstream `video-prompt-director`, which defaults to 30-second prompts for HyperFrames-style generators. HiAPI's video models output single clips up to 15 seconds. Defaulting to `5` keeps the prompt **directly runnable** against Seedance 2.0 or HappyHorse 1.0 without the user having to remember to compress the plan. Longer pieces are still supported up to `15` seconds where the target model allows it.

---

## File Structure

```text
.
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── LICENSE
├── package.json
├── agents/
│   └── openai.yaml
├── references/
│   ├── prompt-patterns.md
│   ├── source-extraction.md
│   └── hiapi-handoff.md
├── scripts/
│   └── install.mjs
└── llms-install.md
```

---

## FAQ

| Question | Answer |
| --- | --- |
| Does this skill call the HiAPI API directly? | No. It produces prompts. Pair it with a HiAPI video skill to render. |
| Do I need `HIAPI_API_KEY` to use this skill? | No. This skill runs offline. The key is only needed for the target render skill. |
| Why does it default to 5 seconds and not 30? | HiAPI's video models do not support 30-second outputs. Seedance supports integer durations from 4 to 15 seconds; HappyHorse supports 3/5/8/10/15. |
| Can it pick the target model for me? | Yes. If you do not name one, it defaults to Seedance 2.0 for image-to-video and cinematic work, HappyHorse 1.0 for fast text-only drafts. |
| What if my brief lacks facts? | This skill only labels **staging choices** (camera, layout, lighting) as `[creative assumption]`. Missing facts become a question for you, not an invented claim. |
| What if I provide a URL? | This skill extracts facts from the source first, then writes the prompt. See `references/source-extraction.md`. |

---

## Compatibility

| Agent | Install Method |
| --- | --- |
| Codex | `npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --codex` |
| Claude Code | `npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --claude` |
| OpenClaw | `openclaw skills add https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill` |
| OpenCode | `AGENT_SKILLS_DIR=~/.opencode/skills npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill -y` |
| Cursor / other | `npx -y github:HiAPIAI/hiapi-video-prompt-generator-skill --target=/your/skills/dir` |

---

## License

MIT

---

[HiAPI](https://www.hiapi.ai) — One API, all AI models
