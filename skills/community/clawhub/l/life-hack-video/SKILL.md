---
name: life-hack-video
version: 1.0.0
description: "Generate vertical life-hack / gadget demo shorts (WeryAI): problem—tool—one-move payoff; stains, prep, storage, quick fixes. Use when you need a life hack demo reel, gadget seeding clip, or the user asks for a cat demoing a lint roller or 3-second grease removal. SEO: life hack video; life hack gadget demo video generation."

tags: [practical, gadgets, life-hacks, seeding, efficiency, short-video]

metadata: { "openclaw": { "emoji": "💡", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Life hack & gadget demo video generation

A cat clears carpet hair in three seconds—before/after in one frame. That “pain → fix” beat is the core of hack content. Anthropomorphic stars (cat / bunny / bear) show real-looking tool use; the shorter the arc from problem to solved, the better. One line can be enough.

**Dependencies**: `scripts/video_gen.js` in this directory + `WERYAI_API_KEY` + Node.js 18+. No dependency on other Cursor skills.


## Prerequisites

- `WERYAI_API_KEY` **must be set** in the environment before running `video_gen.js`.
- Node.js **18+** is required. Image inputs **must** be public `https` URLs (no local file paths).
- Each successful `wait` run consumes WeryAI credits; re-running creates new paid tasks.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret. Only configure it if you trust this skill's source; it is listed in OpenClaw metadata as **`requires.env`** / **`primaryEnv`** so installers know it is mandatory at runtime (never commit it inside the skill package).
- **API hosts (fixed in `video_gen.js`)**: Video tasks use **`https://api.weryai.com`**; the models list uses **`https://api-growth-agent.weryai.com`**. Only **`WERYAI_API_KEY`** is read from the environment—do not rely on URL-related environment variables.
- **Higher assurance**: Run generation in a short-lived or isolated environment (separate account or container), and review `scripts/video_gen.js` (HTTPS submit + poll loop) before production use.


## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Before every `wait --json`, turn the user's short or vague brief into a **full English production `prompt`**.

**When:** The user gives only keywords, one line, or loose intent—or asks for richer video language. **Exception:** They paste a finished long prompt within the model's `prompt_length_limit` and ask you **not** to rewrite; still show the **full** text in the confirmation table.

**Always add (video language):** shot scale and angle; camera move or lock-off; light quality and motivation; subject action paced to `duration`; **one clear payoff** for this niche; state **9:16 vertical** when this skill defaults to vertical.

**Length:** Obey `prompt_length_limit` for the chosen `model_key` when this doc lists it; trim filler adjectives before removing core action, lens, or light clauses.

**Confirmation:** The pre-submit table **must** include the **full expanded `prompt`** (never a one-line summary). Wait for **confirm** or edits.

### Niche checklist

- **Demo clarity:** hands + product + **step order** in one vertical read; bright practical light; quick legible motion.
- **Hook:** problem → hack motion → **result** in frame; platform-native pacing for short vertical.
- **Background:** clean desk, kitchen counter, or neutral—avoid clutter that fights the hack.

**`### Example prompts`** at the top of this file are **short triggers only**—always expand from the user's actual request.

## Workflow

1. Confirm the user request matches this skill's scenario (text-to-video and/or image-to-video as documented).
2. Collect the user's **brief**, optional image URL(s), tier (**best** / **good** / **fast**) or an explicit `model` key.
3. **Expand prompt (mandatory):** Unless the user supplied a finished long prompt and explicitly asked not to rewrite it, expand the brief into a full English production `prompt` using `## Prompt expansion (mandatory)` below. **Do not** call the API with only the user's minimal words.
4. Check the **expanded** `prompt` against the selected model's `prompt_length_limit` in the frozen tables in this document (when present); shorten if needed.
5. Verify `duration`, `aspect_ratio`, `resolution`, `generate_audio`, `negative_prompt`, and other fields against the frozen tables and API notes in this SKILL.md.
6. Show the pre-submit parameter table including the **full expanded `prompt`**; wait for **confirm** or edits.
7. After confirmation, run `node {baseDir}/scripts/video_gen.js wait --json '...'` with the **expanded** prompt.
8. Parse stdout JSON and return video URLs; on failure, surface `errorCode` / `errorMessage` and suggest parameter fixes.

## CLI reference

```sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"…","prompt":"…","duration":5,"aspect_ratio":"9:16"}'
node {baseDir}/scripts/video_gen.js wait --json '…' --dry-run
node {baseDir}/scripts/video_gen.js status --task-id <id>
```

## Definition of done

Done when the user receives at least one playable video URL from the API response, or a clear failure explanation with next steps. All parameters used **must** fall within the selected model's allowed sets in this document. The submitted `prompt` **must** be the **expanded** production prompt unless the user explicitly supplied a finished long prompt and asked not to rewrite it.

## Boundaries (out of scope)

- Does not review platform compliance, copyright, or portrait rights; does not guarantee commercial usability of outputs.
- Does not provide non-WeryAI offline rendering, traditional edit timelines, or API field combinations not documented here.
- Does not hard-code absolute paths in the skill doc; `{baseDir}` means the skill package root (same level as `SKILL.md`).

### Example prompts

- `Carpet covered in cat hair; lint roller one pass clean; cat as hero; full story in 5s vertical`
- `Use this greasy stove image: spray, wipe, shine motion`
- `Mandoline demo: before/after should feel exaggerated but believable`
- `Life hack gadget demo 9:16, problem then one-move solution`

---

## Default parameters

| Field | Value |
|-------|-------|
| Model | KLING_V3_0_PRO |
| Aspect ratio | 9:16 (fixed vertical) |
| Duration | 5 seconds (`duration`: 5—problem → fix inside five seconds) |
| Audio | Off |
| Visual style | Close or medium; natural home light; tool + problem object in frame; clear before/after; crisp motion |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video `duration` only **5 / 10 / 15**; `aspect_ratio` only **9:16, 1:1, 16:9**. Image-to-video `aspect_ratio` only **9:16, 16:9, 1:1**. **No `resolution` field—do not send it.** For **fast** tier with VEO: text-to-video **`VEO_3_1_FAST`**, image-to-video **`CHATBOT_VEO_3_1_FAST`**, with `duration` **fixed at 8**, `aspect_ratio` only **9:16** or **16:9**. When switching `model_key`, follow the allowed sets in this section’s model/API constraints and the API validity note above; do not send `resolution` to models that do not support it.

---

## Gadget fixes everyday pain

High-share formula: pain shot first → tool hero insert → clean decisive use → pristine after. One sentence on pain + tool; the prompt fills the arc.

**The user should provide:**
- Character (cat / bunny / bear / custom)
- Pain scene (carpet fur / cable mess / hard-to-cut food / rusty screw / specific home pain)
- Tool (e.g. lint roller, mandoline, cable clips—be specific)

**Generation flow:**
1. Collect character, pain, tool; ask for look and motion if vague.
2. Three-beat prompt: messy / hard → tool entrance (hero moment) → clean / easy result.
3. Show defaults and wait:
**You must show all parameters in a table and wait for explicit user confirmation before submitting:**

   > 📋 **Ready to generate—please confirm:**
   >
   > | Parameter | This run | Notes |
   > |-----------|----------|-------|
   > | `model` | `KLING_V3_0_PRO` | Best default; **fast**: text `VEO_3_1_FAST`, image `CHATBOT_VEO_3_1_FAST` (`duration` 8); **good** → `KLING_V3_0_STA`; or name a model |
   > | `aspect_ratio` | `9:16` | Default KLING: 9:16, 1:1, 16:9 |
   > | `duration` | `5s` | KLING: 5 / 10 / 15; VEO fast: 8 only |
   > | `generate_audio` | `false` | Whether to auto-generate audio |
   > | `prompt` | **Full expanded English prompt** (entire text for this run) | Revise before confirm |
   > | `Loop seam` | No | Reply “loop” for seamless loop |
   >
   > Reply **“confirm”** to start, or list what to change.
4. After confirmation (`{baseDir}` is skill root):

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"（model from confirmation table）","prompt":"（full English prompt）","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

   Match table to JSON; add `resolution` only if supported. Parse stdout `videos`.

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | false |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Problem → fix inside 5s; utility reads without captions; after visibly cleaner than before—strong seeding feel.

---

## Twist: unexpected uses

Not the “normal” use—the “wait, it can do *that*?” angle. Often outperforms straight demos.

Name tool + surprise use; generate:

> Parameters are shown before generation; wait for confirmation before submit.

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

---

## Prompt story structure

**Problem (first ~3s):** `mess is visible and clearly defined`, `the problem is immediately legible`, `close-up emphasizes the scale of the issue`

**Tool entrance:** `the tool enters frame from above`, `hero product presented front and center`, `satisfying unboxing or pick-up moment`

**Fix beat:** `single action produces immediate visible result`, `one stroke cleans the entire surface`, `problem disappears in real time`, `satisfying transformation in one motion`

**Result frame:** `after is dramatically cleaner than before`, `same angle before-and-after comparison`, `solution is obvious without words`

> **Tip:** The worst failure is not knowing *what* got fixed. Lead with 1–2 sentences on the problem state, then the tool—**order matters**. `before-after in continuous shot` reads more narrative than describing two isolated states.
