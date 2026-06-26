---
name: myreels-storyboard
description: |
  Professional storyboard design tool for short drama/video production.
  Activates when user mentions: script, storyboard, story board, shot design, video production planning, short drama.
  Workflow: story → character design → storyboard design → CSV/table confirmation → guide user to myreels-api for image/video generation.
  This skill focuses on storyboard design and content planning; actual image/video generation requires myreels-api skill.
---

# MyReels Storyboard Design Tool

## Integration with myreels-api

```
myreels-storyboard (storyboard design)
       ↓ generates storyboard CSV
myreels-api (image/video generation) ← user must install this skill first
```

**Important**: This skill handles storyboard design. After completion, guide the user to use `myreels-api` skill for actual image and video generation.

## Complete Workflow

```
1. Story Input → User provides plot outline
2. Story Understanding → Use the active OpenClaw default LLM to understand plot, roles, relationships, and visual beats
3. Character Design → Design characters with a single-image three-view turnaround sheet (front/side/back)
4. Shot Breakdown → Generate structured shots
5. User Confirmation → Output CSV + platform table
6. Image Generation → Guide user to myreels-api
7. Video Creation → Guide user to myreels-api (optional)
```

## Step 1: Collect User Requirements

Collect the following information:

| Question | Options |
|----------|---------|
| Story content | Plot outline or full script |
| Video style | cinematic / anime / 3d cartoon / realistic |
| Duration | e.g., 60 seconds, 2 minutes |
| Shot count | e.g., 10-15 shots |
| Aspect ratio | 16:9 / 9:16 / 1:1 (vertical = 9:16) |
| Has dialogue | Yes / No |

After collecting inputs:
- Use the current OpenClaw session's default LLM to understand the story semantically
- Infer core roles, recurring relationships, and phase-by-phase visual beats from the user's actual plot, not only from surface keywords
- Do not ask the user to configure an extra LLM just to use this skill
- Do not rely on a bundled local storyboard script for core planning; OpenClaw should draft the CSVs directly
- The old helper `scripts/generate_storyboard.py` is deprecated and should not be referenced in this workflow

## Step 2: Character Design (Important!)

**Before shot design, establish character consistency using a three-view character sheet (三视图).**

Default rule:
- Treat character design as a `single-image turnaround sheet`, not as a poster
- The first-pass deliverable should show the same character's `front view`, `side view`, and `back view` on one canvas
- Keep outfit, body shape, hairstyle, and accessories identical across all three views
- Use full-body neutral standing pose and a plain background unless the user asks otherwise
- Recommend `nano-banana2` first for generating the base three-view character sheet
- Prefer a `character-first` workflow: approve the character sheet and tags first, then generate storyboard shots with those tags injected

### Character Design Fields

| Field | Description |
|-------|-------------|
| `character_name` | Character name |
| `story_role` | Role in story, e.g. protagonist / opponent / companion |
| `relation_to_main` | Relationship to the main character, e.g. self / conflict / ally / romance |
| `appearance` | Physical description (hair, eyes, face, build) |
| `outfit` | Clothing and accessories |
| `personality` | Key personality traits |
| `reference_model` | Base model for the first turnaround sheet, default `nano-banana2` |
| `single_image_turnaround_prompt` | Main English prompt for one-sheet front/side/back generation |
| `front_view` | English description for front view |
| `side_view` | English description for side view |
| `back_view` | English description for back view |
| `character_tags` | Consistency tags for AI prompts (e.g., "short hair, left face mole, red earrings") |
| `negative_prompt` | Terms to suppress poster-like, inconsistent, or cropped outputs |

### Three-View Diagram Output

Generate character descriptions for AI image generation. The output should be structured for a single image containing all three views:

```
CHARACTER: [Name]
STORY_ROLE: [protagonist / opponent / companion / love_interest]
RELATION_TO_MAIN: [self / conflict / ally / romance]
TAGS: [Consistency tags for prompt injection]
REFERENCE_MODEL: [Usually nano-banana2 for the first three-view sheet]
SINGLE_IMAGE_TURNAROUND_PROMPT: [English prompt explicitly requesting one image with front / side / back full-body views]
NEGATIVE_PROMPT: [English suppression terms for layout drift]

FRONT: A [age] [ethnicity] [gender] with [hair], [eyes], [build], wearing [outfit], neutral standing pose
SIDE: Same character from side profile showing [distinctive feature / silhouette / accessory placement]
BACK: Same character from behind showing [hairstyle back shape / outfit back detail / asymmetry]
```

Prompt rule:
- The `single_image_turnaround_prompt` must front-load the layout requirement: `one image`, `same character`, `front view`, `side view`, `back view`, `aligned left to right`
- Do not output three unrelated portrait prompts as the default character design result
- Only add expression sheets, weapons, or alternate outfits after the base three-view sheet is approved

### Character Consistency

For each character, build a **character tag library** that will be reused in all shot prompts:

```
# Example character tags
"短发女孩, 左脸有痣, 红色耳钉, 黑色皮夹克"
→ "short hair, beauty mark on left cheek, red earrings, black leather jacket"
```

### Character-First Mode

Recommended operating mode:
- Generate `characters.csv` first
- Generate `relationships.csv` for recurring character pairs
- Lock the main character's `single_image_turnaround_prompt`, `negative_prompt`, and `character_tags`
- Only define extra character rows when the story actually implies them; do not invent an `opponent`, `love_interest`, or `companion` just because the genre suggests one
- Reuse the approved `character_tags` in every `visual_prompt`
- Treat the first approved character row as the anchor for downstream storyboard drafts
- In multi-character stories, inject only the characters relevant to each shot phase instead of dumping everyone into every prompt
- Build `relationships.csv` as a pairwise matrix for all recurring character pairs, not only protagonist-centered pairs
- Reuse `relationship_type` and `prompt_hint` when designing confrontation, ally, or romance shots
- Also use `visual_relation`, `emotional_relation`, and `blocking_pattern` to keep staging and mood consistent across repeated pair shots
- Let `relationship_type` bias the default shot language: conflict leans toward low-angle / confrontational framing, ally toward cooperative full shots, romance toward closer eye-level coverage
- Let `theme` bias the baseline shot rhythm too: action leans kinetic, romance leans intimate, thriller leans uneasy, sci-fi leans scale/discovery
- In scenes with 3+ recurring characters, choose the active pair/group per shot based on the current beat; do not force every established relationship into every shot

Default OpenClaw behavior:
- The skill should use the active OpenClaw default LLM to draft `characters.csv`, `relationships.csv`, and `storyboard.csv`
- The CSVs should reflect narrative understanding, not just mechanical keyword expansion
- Keep CSV column names stable in English, but make user-facing cell values follow the user's language whenever possible
- Keep AI-facing prompt fields in English for cross-model portability: `single_image_turnaround_prompt`, `negative_prompt`, `front_view_prompt`, `side_view_prompt`, `back_view_prompt`, `character_tags`, `prompt_hint`, and `visual_prompt`
- Keep IDs and machine-oriented codes stable: `character_id`, `relationship_id`, `shot_id`, `scene_code`
- `visual_prompt` should preserve concrete story specifics from the user's outline in English, including names, props, locations, and beat-specific actions
- `description` and `action` should vary shot by shot; avoid repetitive generic phase labels when a more specific beat description is available
- For mixed-language input, keep `description` in the dominant user language; if no dominant language is clear, follow the user's most recent instruction language
- If a downstream automation flow later needs normalized English enum values, create a secondary English export instead of replacing the user-facing review CSV

## Step 3: Generate Storyboard

### Shot Structure

Each shot includes these fields:

| Field | Description |
|-------|-------------|
| `shot_id` | Scene + Shot number (e.g., S01-01) |
| `shot_type` | Shot size |
| `camera_angle` | Camera angle |
| `movement` | Camera movement |
| `duration` | Estimated seconds (2-5s typical) |
| `description` | **User language description** - brief summary in user's input language (Chinese/Japanese/English). NOT used for AI generation. |
| `visual_prompt` | English prompt for AI image generation |
| `action` | Character action description |
| `dialogue` | Dialogue/voiceover (optional) |
| `emotion` | Target audience emotion |
| `sound_fx` | Sound effects / music cues (optional) |
| `notes` | Additional notes |
| `difficulty` | 🟢 simple / 🟡 medium / 🔴 complex |
| `image_url` | Generated image URL from downstream tool (optional) |
| `video_url` | Generated video URL from downstream tool (optional) |
| `status` | Workflow status in the user's language for review CSVs; normalize in the English export if needed |

### Shot Type Reference

| Type | Chinese | Use Case |
|------|---------|----------|
| Extreme Close-up / ECU | 大特写 | Key detail, extreme emotion |
| Close-up / CU | 特写 | Face, key object |
| Medium Close-up / MCU | 中近景 | Dialogue, slight conflict |
| Medium / MS | 中景 | Conversation, interaction |
| Full Shot / FS | 全景 | Full body, relationship |
| Wide / WS | 远景 | Environment, establishing |

### Camera Angles & Psychology

| Angle | Emotion Implication |
|-------|---------------------|
| Eye-level | Neutral, objective |
| Low-angle (仰视) | Power, authority, threat |
| High-angle (俯视) | Vulnerability, submission |
| Dutch | Unease, tension, chaos |
| POV | Subjective, immersion |
| Tilted | Unstable, danger |

### Camera Movement

- Fixed / Static
- Dolly In (推近) / Dolly Out (拉远)
- Pan (摇镜) / Tilt (倾斜)
- Follow / Tracking (跟拍)
- Orbit (环绕) / Crane (升降)
- Handheld (手持) / Breath-like (呼吸感)

### Shot Difficulty Grading

| Grade | Icon | Description |
|-------|------|-------------|
| Simple | 🟢 | Fixed camera, single subject, no complex interaction |
| Medium | 🟡 | Light camera movement, dual subject, simple effects |
| Complex | 🔴 | Fast motion, multiple subjects, complex choreography, special lighting/particles |

### Emotion Mapping

Each shot must specify target emotion:

| Emotion | Key | Description |
|---------|-----|-------------|
| Hook | 钩子 | Attention grab |
| Tension | 紧张 | Building suspense |
| Conflict | 冲突 | Confrontation |
| Sweet | 甜宠 | Romance, warmth |
| Twist | 反转 | Surprise |
| Climax | 高潮 | Peak emotional moment |
| Release | 释然 | Resolution |

## Step 4: AI Prompt Engineering

### Prompt Structure

```
[Subject] + [Action] + [Environment] + [Lighting] + [Quality] + [Style] + [Camera]
```

Prompt design rule for this skill:
- `single_image_turnaround_prompt` should use layout-first language for `nano-banana2`
- `visual_prompt` should carry `theme` + `phase` cues so action / romance / thriller / sci-fi drafts do not collapse into the same generic shot language

### Required Quality Tags

Always include:
- `cinematic`
- `8k` or `high resolution`
- `shallow depth of field` or `bokeh`
- `dynamic lighting`

### Control Tags

If needed, add:
- `no text` / `no watermark` / `no distorted face`
- `solo` / `two-shot` / `crowd`

### Character Consistency in Prompts

Always inject character tags from Step 2:

```
# Before
"A woman fighting aliens"

# After (with character tags)
"A young woman with short hair, beauty mark on left cheek, red leather jacket fighting aliens, cinematic, 8k..."
```

### Scene Consistency

Use scene code +固化环境描述:

```
SCENE-A: "abandoned colony base, red dust, two moons, ruins"
# All shots in SCENE-A reference this environment
```

## Step 5: Output Confirmation

### Multi-Platform Output

**Feishu**: Use feishu_bitable for online editing
**Telegram**: Formatted text table or CSV attachment
**Other**: Default to CSV

### Storyboard Table Fields

```
shot_id, scene_code, shot_type, camera_angle, movement, duration, description, visual_prompt, action, dialogue, emotion, sound_fx, notes, difficulty, image_url, video_url, status
```

**Note**:
- The CSV headers stay in English for schema stability
- Human-facing values in all three CSVs should follow the user's language
- The `visual_prompt` field is always in English for AI image generation
- If automation needs English enums such as `shot_type`, `camera_angle`, `movement`, `emotion`, `difficulty`, or `status`, write a separate English export copy instead of mutating the review CSV

## Step 5A: Project Workspace Management

When this skill writes files, it should automatically create a project workspace in the user's current working directory or requested output directory.

Default root pattern:

```text
storyboard-projects/YYYYMMDD-project-slug/
```

Recommended structure:

```text
storyboard-projects/YYYYMMDD-project-slug/
├── 00-brief/
│   ├── story-brief.md
│   └── user-notes.md
├── 01-characters/
│   ├── drafts/
│   │   ├── characters.v1.draft.csv
│   │   └── character-design.v1.draft.md
│   ├── approved/
│   │   ├── characters.approved.csv
│   │   └── character-design.approved.md
│   ├── exports/
│   │   └── characters.program-en.csv
│   └── generated-images/
│       ├── raw/
│       ├── approved/
│       ├── requests/
│       ├── tasks/
│       └── metadata/
├── 02-relationships/
│   ├── drafts/
│   │   └── relationships.v1.draft.csv
│   ├── approved/
│       └── relationships.approved.csv
│   └── exports/
│       └── relationships.program-en.csv
├── 03-storyboard/
│   ├── drafts/
│   │   ├── storyboard.v1.draft.csv
│   │   └── storyboard-notes.v1.draft.md
│   ├── approved/
│       ├── storyboard.approved.csv
│       └── storyboard-notes.approved.md
│   └── exports/
│       └── storyboard.program-en.csv
├── 04-generation/
│   ├── storyboard-images/
│   │   ├── raw/
│   │   └── approved/
│   │   ├── requests/
│   │   ├── tasks/
│   │   └── metadata/
│   └── videos/
│       ├── raw/
│       ├── approved/
│       ├── requests/
│       ├── tasks/
│       └── metadata/
├── 05-review/
│   └── review-log.md
└── 06-delivery/
    └── manifest.md
```

Workspace rules:
- Do not write user project artifacts back into the skill definition folder itself
- Create the project root before saving the first CSV, markdown note, image, or video
- Save editable drafts under `drafts/`
- After user confirmation, freeze a copy under the matching `approved/` folder instead of overwriting history
- Save character three-view turnaround images under `01-characters/generated-images/raw/`
- Move or copy user-confirmed character reference images into `01-characters/generated-images/approved/`
- Save storyboard shot images under `04-generation/storyboard-images/raw/`
- Save storyboard videos under `04-generation/videos/raw/`
- Move or copy user-confirmed storyboard media into the matching `approved/` media folder
- For every myreels-api generation, save the exact request payload under `requests/`
- Save task lookup snapshots and task IDs under `tasks/`
- Save response metadata under `metadata/`, including model name, mode, aspect ratio, seed if available, source image references, created time, and returned URLs
- Keep request / task / metadata filenames aligned with the output artifact name so reruns can reuse the same context
- Record major review decisions in `05-review/review-log.md`
- Summarize the final approved artifact set in `06-delivery/manifest.md`

Versioning rules:
- Use file names like `characters.v1.draft.csv`, `storyboard.v2.draft.csv`, `images-shot-S01-01.v1.png`
- Use `*.approved.*` for frozen user-confirmed files
- When revising an approved artifact, create a new draft version instead of mutating the approved snapshot
- Put normalized program-facing CSV exports in `exports/` with names such as `storyboard.program-en.csv` and `relationships.program-en.csv`
- Use aligned sidecar records such as `character-C001-turnaround.v1.request.json`, `character-C001-turnaround.v1.task.json`, `character-C001-turnaround.v1.meta.json`
- Use the same pattern for storyboard shots and videos, for example `shot-S01-01.v2.request.json` and `shot-S01-01.v2.meta.json`
- If the user already provided a target directory, follow it and only apply this structure inside that location

Re-run stability rules:
- Before re-running a generation, read the latest matching request, task snapshot, and metadata files first
- Reuse the last approved prompt, model, aspect ratio, and source asset references unless the user explicitly asks to change them
- If the rerun changes any material parameter such as model, prompt, aspect ratio, seed, duration, or source image, write a new versioned request file instead of overwriting the old one
- In `review-log.md`, note why the rerun happened and what changed relative to the previous attempt

## Step 6: Guide to myreels-api

### Guidance Message (Image Generation)

```
Storyboard confirmed. Now use `myreels-api` skill for image generation.

Recommended workflow:
1. Generate one single-image character turnaround sheet first (front/side/back on one canvas)
2. Prefer `nano-banana2` for the base three-view character sheet, then generate key storyboard shots using: nano-banana2 / seedream 5.0 / kling v3 image
3. Verify character consistency across all shots
4. Confirm images before video generation

Say: "Use myreels-api to generate storyboard images"
```

### Guidance Message (Video Generation)

```
Images confirmed. Now use `myreels-api` skill for video.

Recommended models (image to video):
- Kling O3 / Kling V3 (general video)
- Seedance 1.5 Pro SE (high quality)
- Wan 2.6 i2v / Hailuo-2.3 (quick preview)

Note: For complex shots (🔴), consider longer duration or multiple takes.

Say: "Use myreels-api to convert these images to video"
```

## Step 7: Quality Control Checklist

For each shot, verify:

- [ ] Character matches design (outfit, hair, facial features)
- [ ] Lighting direction consistent with scene light source
- [ ] Motion trajectory physically possible (no clipping, floating)
- [ ] Shot type serves narrative rhythm
- [ ] Safe zone reserved (vertical: top/bottom 20% no key elements for subtitles)
- [ ] Emotion matches intended audience feeling

## Output Files

- `characters.csv` - Character design data
- `relationships.csv` - Relationship matrix for recurring characters
- `storyboard.csv` - Complete storyboard
- `assets/characters-template.csv` - Character CSV starter template
- `assets/relationships-template.csv` - Relationship CSV starter template
- `assets/storyboard-template.csv` - Storyboard CSV starter template
- Character reference images (via myreels-api)
- Storyboard image URLs (via myreels-api)
- Project review notes and approved snapshots under the project workspace
- Request payloads, task snapshots, and response metadata for reproducible reruns

## Notes

- `visual_prompt` must be in **English** with quality tags
- User can input in Chinese / Japanese / English
- In the three CSVs, user-facing values should follow the user's language; only AI-facing prompt fields stay in English
- If the workflow needs machine-friendly English enums, generate a separate `*.program-en.csv` export instead of changing the review CSV
- Each shot: 2-5 seconds recommended
- Always establish character design before shot breakdown
- Use difficulty grading to manage AI generation expectations
- In OpenClaw, this skill should primarily rely on the active session model for story understanding and CSV drafting
- Do not require users to provide extra LLM credentials just to use this skill in OpenClaw
- No local storyboard-generation script is required; draft the CSVs natively in OpenClaw
- Automatically create a project workspace so drafts, approvals, images, videos, and markdown notes remain organized
- Persist generation requests and metadata so image/video reruns can stay stable
- See references/ for detailed guides
