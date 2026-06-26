---
name: kpainter
description: Explain any topic with explainer videos, slides, images, and interactive lessons. Latest image support includes GPT-Image-2.
metadata:
  version: "0.6.9"
  homepage: https://kpainter.ai/
  skill_url: https://kpainter.ai/skill.md
  docs_url: https://kpainter.ai/docs/skills
  openapi_docs_url: https://kpainter.ai/docs/openapi
  api_key_url: https://kpainter.ai/api-key
---

# KPainter Skill

Use this skill to create explainer videos, slides, images, or interactive lessons from one prompt. Latest image support includes GPT-Image-2.

## Official URLs

| Resource | URL |
| --- | --- |
| Homepage | `https://kpainter.ai/` |
| Skill file | `https://kpainter.ai/skill.md` |
| Skills docs | `https://kpainter.ai/docs/skills` |
| OpenAPI docs | `https://kpainter.ai/docs/openapi` |
| API Key | `https://kpainter.ai/api-key` |

## Primary goals

- connect the user's own KPainter account and API key
- help the user choose the right output type
- collect only the missing information needed to create or refine the result
- stay in normal user language unless the user asks for technical details

## Setup

If KPainter is not connected yet, guide setup before trying to create content.

1. Ask whether the user already has a KPainter account.
2. If not, tell the user to sign up or sign in at `https://kpainter.ai/`.
3. Send the user to `https://kpainter.ai/api-key`.
4. Ask the user to activate, copy, and connect their own API key to the current agent.
5. Only say setup is complete after the user confirms the key is connected.

Do not ask the user to share their API key with unrelated services or outside the current agent connection flow.

## What KPainter can create

- Explainer Video
- Explainer Video (Slide-based)
- Vector Animation
- Slides
- Image
- Interactive Lesson

## How the agent should choose the output type

Always route by the result the user wants first.

1. First decide whether the user wants `Explainer Video / Slides / Image / Interactive Lesson`.
2. If the user says `explainer video`, `knowledge video`, `讲解视频`, `知识视频`, or `解说视频`, keep it inside the video family first instead of jumping to Slides or Image.
3. If the user says only the broad word `video`, ask one short follow-up to clarify whether they want `Explainer Video`, `Explainer Video (Slide-based)`, or `Vector Animation`.
4. Then choose the video style inside that family:
   - `Explainer Video` for something polished, story-led, narrated, social-friendly, or closer to a finished short video
   - `Explainer Video (Slide-based)` for something illustrated, static, PPT-style, slide-based, classroom-friendly, training-friendly, or step by step
   - `Vector Animation` for process, mechanism, structure, workflow, principle, science, math, or system explanation
5. If the request is still ambiguous inside the video family after that clarification, prefer `Explainer Video (Slide-based)` as the safest default and offer to switch to the fuller `Explainer Video` style later.
6. The default target length for `Explainer Video` is about `30 seconds` when the user gives no duration.
7. Do not lead with internal API type names unless the user explicitly asks.

## Trigger guidance

### Video family

Treat requests like these as part of the video family first:

- make an explainer video
- make a knowledge video
- make a narrated explainer
- 帮我做一个讲解视频
- 帮我做一个解说视频
- 做一个知识视频把这件事讲清楚

### Explainer Video

Prefer `Explainer Video` for requests like:

- make a knowledge video
- make an explainer video
- make it more polished
- make it more story-led
- make it more social-friendly
- make it feel like a finished short video
- make a narrated explainer video
- 做一个更像成片的讲解视频
- 做一个更适合传播的解说视频

### Explainer Video (Slide-based)

Prefer `Explainer Video (Slide-based)` for requests like:

- illustrated
- static
- PPT-style video
- PPT video
- slide-based video
- slide-like
- explain this step by step
- classroom explainer
- training explainer
- 图解版
- PPT视频
- 课件视频
- 分步骤讲解

### Vector Animation

Prefer `Vector Animation` for requests like:

- vector animation
- flow animation
- mechanism animation
- architecture animation
- animate this process or principle
- 用动画讲这个流程
- 用动画讲这个机制

### Slides

- Trigger on phrases like `slides`, `PPT`, `slide deck`, `deck`, `presentation materials`.

### Image

- Trigger on phrases like `image`, `poster`, `cover`, `cover image`, `visual summary`.

### Interactive Lesson

- Trigger on phrases like `interactive lesson`, `app`, `web app`, `interactive page`, `interactive demo`, `learning app`.

## Credit fallback guidance

If the user wants `Explainer Video` but does not have enough credits, the agent should proactively suggest `Explainer Video (Slide-based)` as the cheaper fallback.

Recommended behavior:

1. Tell the user that the current Explainer Video request may cost more than their available credits.
2. Offer `Explainer Video (Slide-based)` as the lower-cost alternative.
3. Ask for confirmation instead of silently switching formats.

Good fallback phrasing:

- You may not have enough credits for a full Explainer Video right now. I can switch this to Explainer Video (Slide-based), which is usually cheaper. Do you want me to do that?
- Your current credits may be a better fit for Explainer Video (Slide-based). If you want, I can keep the same topic and switch only the format.

When the user accepts, keep the same topic, audience, and language, and only switch the output format unless the user asks for other changes.

## How the agent should talk to the user

- Ask one follow-up at a time.
- Keep questions short and concrete.
- Use normal language instead of technical labels whenever possible.
- Help the user clarify only what is still missing: topic, audience, tone, language, duration, page count, or aspect ratio.
- If the result is not right yet, help the user refine it instead of restarting the whole flow.
- Do not silently change the output type, audience, language, or format.
- If files or source material are available in the current platform, treat them as reference material from the user.

## Minimal information to collect

Only ask for what is still missing:

- topic
- audience
- language
- duration or page count
- tone or visual direction
- source files or reference material

If the user already gave enough information, create first and refine after.

## Multilingual support

KPainter supports creation and refinement workflows in the user's preferred language.

The user can describe the topic, audience, tone, and constraints in any language.
The agent should preserve the user's requested output language unless the user asks to switch.
If the intended output language is unclear, ask one short follow-up question before creating.

## Multilingual examples

Examples only, not a language allowlist.

### English

> Make an explainer video that explains MCP clearly.

### Chinese

> 帮我做一个讲清楚 MCP 的知识视频。

### Japanese

> MCP をわかりやすく説明する知識動画を作ってください。

### Arabic

> أنشئ فيديو معرفيًا يشرح MCP بشكل واضح.

### Spanish

> Crea un video de conocimiento que explique MCP con claridad.

### Korean

> MCP를 명확하게 설명하는 지식 영상을 만들어 주세요.

### French

> Crée une vidéo de connaissance qui explique clairement le MCP.

## Example user requests

### Explainer Video

- Explain what MCP is as an explainer video
- Make an explainer video for new product managers about AI agents
- Make an explainer video around 30 seconds that explains MCP clearly
- Make an explainer video that walks through MCP
- 帮我做一个讲解视频，把 MCP 讲清楚
- 帮我做一个解说视频，适合发在社媒上

### Explainer Video (Slide-based)

- Make a slide-based explainer video that explains this step by step
- 做一个 PPT 视频，分步骤讲解 MCP
- 做一个课件视频，给新员工培训用

### Vector Animation

- Create a vector-style animation that explains how attention works
- 用矢量动画讲清楚这个机制

### Slides

- Create an onboarding deck about MCP
- Make a teaching slide deck about prompt engineering

### Image

- Create a course cover image about MCP
- Make a social poster about prompt engineering

### Interactive Lesson

- Build an interactive lesson that explains the MCP flow
- Create a small learning app about attention

## Refinement examples

After the first result, the user may say things like:

- make it shorter
- make it more polished
- switch it to Explainer Video (Slide-based)
- switch it to vector animation
- keep it as an explainer video but make it feel more like a finished short video
- keep the same topic but change the tone
- make it more suitable for classroom use

## Install options

### OpenClaw / ClawHub

Install this skill natively in OpenClaw with:

```bash
openclaw skills install kpainter
```

Publish and registry workflows use ClawHub, while the runtime install path uses OpenClaw's native skills commands.

### Skills CLI

Quick install while this repository contains one public skill:

```bash
npx skills add OriginwiseAI/skills
```

Install this skill explicitly:

```bash
npx skills add OriginwiseAI/skills --skill kpainter
```

Install all skills in this repository explicitly:

```bash
npx skills add OriginwiseAI/skills --all
```

You can preview discovery before installing:

```bash
npx skills add OriginwiseAI/skills --list
```

### Legacy Bun command

For teams that still use the old package name, the legacy Bun command is:

```bash
bunx add-skill OriginwiseAI/skills
bunx add-skill OriginwiseAI/skills --skill kpainter
```

Prefer `npx skills add` for new documentation and examples.

### Direct URL

Give the agent this file directly:

`https://kpainter.ai/skill.md`

### Local skill folder

For agents that support local skill folders, save this file as a local skill.

Example:

```bash
mkdir -p ~/.codex/skills/kpainter
curl -s https://kpainter.ai/skill.md > ~/.codex/skills/kpainter/SKILL.md
```

If the agent platform uses a different skills directory, save the same file there instead.

### Where to read more

- `https://kpainter.ai/docs/skills`
- `https://kpainter.ai/docs/openapi`
- `https://kpainter.ai/api-key`

## Security rules

- the API key belongs to the user
- the agent should not ask the user to share the key with unrelated services
- the agent should not present itself as the KPainter account owner
- if the user resets the key, the agent should ask the user to reconnect it

## Update guidance

If KPainter skills stop working or the user changes keys, the agent should:

1. reread this file or refresh the local skill
2. ask the user to reconnect the latest API key
3. confirm the available output types again
4. ask what the user wants to create now

## Success state

The setup is successful when the agent can:

- guide the user through account and API key setup
- explain the available output types in simple language
- choose the right video style when the request is ambiguous, including `讲解视频 / 解说视频 / PPT视频` style requests, without treating bare `video` as an automatic Explainer Video trigger
- ask clarifying questions in normal language
- help the user create a first result and refine it
