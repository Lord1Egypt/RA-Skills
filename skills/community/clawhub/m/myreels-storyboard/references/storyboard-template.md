# Storyboard Template & Format Specification

## CSV File Format

File: `storyboard.csv`, UTF-8 encoding

Bundled assets:
- `assets/storyboard-template.csv` - starter storyboard sheet with the current schema
- `assets/characters-template.csv` - starter character sheet for three-view turnaround planning
- `assets/relationships-template.csv` - starter relationship matrix for recurring character pairs

### Language Policy

- Keep CSV headers in English for schema stability
- Keep IDs and stable codes in machine-friendly form: `character_id`, `relationship_id`, `shot_id`, `scene_code`
- Make user-facing cell values follow the user's language across all three CSVs
- Keep AI-facing prompt fields in English: `single_image_turnaround_prompt`, `negative_prompt`, `front_view_prompt`, `side_view_prompt`, `back_view_prompt`, `character_tags`, `prompt_hint`, `visual_prompt`
- If a downstream system later requires normalized English enums, generate a separate export copy instead of replacing the review sheet

Recommended export files:
- `01-characters/exports/characters.program-en.csv`
- `02-relationships/exports/relationships.program-en.csv`
- `03-storyboard/exports/storyboard.program-en.csv`

## Character Design CSV

Use `characters.csv` to lock the base reference for each character before shot generation.

### Character CSV Schema

```text
character_id,name,story_role,relation_to_main,age,gender,ethnicity,hair,eyes,face,build,outfit,accessories,personality,reference_model,single_image_turnaround_prompt,negative_prompt,front_view_prompt,side_view_prompt,back_view_prompt,character_tags
```

### Character CSV Example

```text
C001,尤纪,主角,本人,25,女,亚洲,短白发,红色眼睛,右眉疤痕,偏瘦结实,黑色战术背心,机械左臂,冷静果断,nano-banana2,"A young Asian woman warrior, character turnaround sheet, three-view diagram, one image, same character, exact same character shown three times, full-body front view, side view, back view, aligned left to right, same scale, consistent outfit, consistent hairstyle, neutral standing pose, white background, studio lighting, design reference board, front view: short white hair, red eyes, scar on right eyebrow, black tactical vest, side view: athletic silhouette and mechanical left arm placement, back view: cropped white hair shape and back armor details, high quality, 16:9","extra characters, duplicate character, three different characters, inconsistent outfit, inconsistent hairstyle, dynamic action pose, cropped body, close-up portrait, busy background, dramatic camera, perspective distortion, missing side view, missing back view, text, watermark","Front view of the same character showing red eyes, scar on right eyebrow, black tactical vest, neutral standing pose, readable costume details","Side profile of the same character showing athletic silhouette and mechanical left arm placement, readable silhouette","Back view of the same character showing cropped white hair shape and tactical vest back details, clear back design","short white hair, red eyes, scar on right eyebrow, black tactical vest, mechanical left arm"
```

### Character Field Reference

| Field | Description | Example |
|-------|-------------|---------|
| `character_id` | Character identifier | C001 |
| `name` | Character name in the user's language when appropriate | 尤纪 |
| `story_role` | Role in the story, localized for the user | 主角 |
| `relation_to_main` | Relationship to the protagonist, localized for the user | 本人 / 对立 / 盟友 / 恋爱 |
| `age` | Approximate age | 25 |
| `gender` | Gender in the user's language when the review sheet is localized | 女 |
| `ethnicity` | Ethnicity for appearance control in the user's language when localized | 亚洲 |
| `hair` | Hairstyle and color in the user's language | 短白发 |
| `eyes` | Eye description in the user's language | 红色眼睛 |
| `face` | Distinctive facial feature in the user's language | 右眉疤痕 |
| `build` | Body type / silhouette in the user's language | 偏瘦结实 |
| `outfit` | Main clothing in the user's language | 黑色战术背心 |
| `accessories` | Important props / accessories in the user's language | 机械左臂 |
| `personality` | Reusable character traits in the user's language | 冷静果断 |
| `reference_model` | Base model for turnaround generation | nano-banana2 |
| `single_image_turnaround_prompt` | Main one-sheet three-view prompt in English | front/side/back in one image |
| `negative_prompt` | Layout and consistency suppression terms in English | no extra characters, no cropped body |
| `front_view_prompt` | Front-view prompt fragment in English | front pose description |
| `side_view_prompt` | Side-view prompt fragment in English | side profile description |
| `back_view_prompt` | Back-view prompt fragment in English | back detail description |
| `character_tags` | Reusable prompt injection tags in English | short white hair, red eyes, scar |

## Storyboard CSV

Use `storyboard.csv` for shot-by-shot planning and downstream generation status.

### Storyboard CSV Schema

```text
shot_id,scene_code,shot_type,camera_angle,movement,duration,description,visual_prompt,action,dialogue,emotion,sound_fx,notes,difficulty,image_url,video_url,status
```

### Storyboard CSV Example

```text
S01-01,SCENE-01,远景,平视,固定,4秒,"女主初次出场，站在废弃殖民地入口观察四周","SCENE-01: alien colony base at dusk, two moons visible, abandoned buildings, red dust atmosphere, cinematic, high resolution, dramatic lighting","主角来到殖民地入口并观察周围","",钩子,环境风声,开场建立场景,简单,"","",待确认
S01-02,SCENE-01,中景,仰视,推近,2秒,"女主向前一步，警惕地抬头观察","SCENE-01: young woman with short white hair, red eyes, wearing black tactical vest, entering frame, cinematic, high resolution, shallow depth of field","主角谨慎向前推进","",紧张,碎石脚步声,角色登场强化,简单,"","",待确认
```

### Storyboard Field Reference

| Field | Description | Example |
|-------|-------------|---------|
| `shot_id` | Scene + shot number | S01-01 |
| `scene_code` | Scene identifier for consistency | SCENE-01 |
| `shot_type` | Shot size in the user's language | 远景 / 中景 / 特写 |
| `camera_angle` | Camera angle in the user's language | 平视 / 仰视 |
| `movement` | Camera movement in the user's language | 固定 / 推近 / 平移 |
| `duration` | Estimated seconds in the user's language style | 3秒 / 5秒 |
| `description` | User-language summary, not for AI | 中文/日文/英文 分镜描述 |
| `visual_prompt` | English prompt for AI generation | Full prompt with scene and character tags |
| `action` | Character or camera action in the user's language | 主角拔出武器 |
| `dialogue` | Dialogue or voiceover in the user's language | "你逃不掉。" |
| `emotion` | Target emotion in the user's language | 钩子 / 紧张 / 高潮 |
| `sound_fx` | Sound or music cue in the user's language | 枪声 / 悬疑音乐 |
| `notes` | Additional notes in the user's language | 需要特效 / 注意安全区 |
| `difficulty` | Generation complexity in the user's language | 简单 / 中等 / 复杂 |
| `image_url` | Generated image URL from downstream tool | https://... |
| `video_url` | Generated video URL from downstream tool | https://... |
| `status` | Workflow status in the user's language | 待确认 / 已确认 / 生成中 / 已完成 |

### Description Field

- Match the user's input language
- Keep it short and readable
- Use it for human review only
- Do not rely on it for generation; `visual_prompt` is the AI-facing field

## Relationship Matrix CSV

Use `relationships.csv` to lock recurring interactions before building multi-character shots.
If 3 or more recurring characters matter on screen, represent all meaningful recurring pairs rather than only protagonist-centered pairs.

### Relationship CSV Schema

```text
relationship_id,character_a_id,character_a_name,character_b_id,character_b_name,relationship_type,visual_relation,emotional_relation,blocking_pattern,interaction_pattern,prompt_hint
```

### Relationship CSV Example

```text
R001,C001,尤纪,C002,肯,对立,对峙剪影,敌意与压迫感,"面对面站位，保留清晰对抗轴线","正面对峙，战术压迫，镜像式站位","same scene, opposing stances, visual tension between both characters, face-to-face blocking, hostile emotional pressure"
R002,C001,尤纪,C003,侦察犬一号,盟友,并肩协作剪影,信任与互相支援,"协作站位，前后景层次清晰，便于阅读团队关系","并肩移动，协同动作，彼此支援","same scene, cooperative blocking, readable teamwork silhouette, supportive emotional tone"
R003,C002,肯,C003,侦察犬一号,对立,猎人与守卫式剪影,互不信任与压迫感,"错位游走距离，捕猎者与守卫者的对抗间距","绕行试探，威胁评估，防御性拦截","same scene, tense spacing between rival fighter and scout robot dog, defensive guard posture, hostile pressure"
```

### Relationship Field Reference

| Field | Description | Example |
|-------|-------------|---------|
| `relationship_id` | Relationship identifier | R001 |
| `character_a_id` | Primary character ID | C001 |
| `character_a_name` | Primary character name in the user's language | 尤纪 |
| `character_b_id` | Secondary character ID | C002 |
| `character_b_name` | Secondary character name in the user's language | 肯 |
| `relationship_type` | Narrative relationship in the user's language | 对立 / 盟友 / 恋爱 |
| `visual_relation` | Reusable visual relation in the user's language | 对峙剪影 |
| `emotional_relation` | Reusable emotional dynamic in the user's language | 敌意与压迫感 |
| `blocking_pattern` | Reusable staging instruction in the user's language | 面对面站位 |
| `interaction_pattern` | Reusable staging pattern in the user's language | 正面对峙，战术压迫 |
| `prompt_hint` | Prompt-ready hint for shot generation in English | same scene, opposing stances, visual tension |

## Platform-Specific Output

### Feishu (feishu_bitable)

Create table with fields above. Use:
- Single select for `shot_type`, `camera_angle`, `movement`, `emotion`, `difficulty`, `status`
- Text for most fields
- URL type for `image_url`, `video_url`

Recommended character table fields:
- Basic profile columns from `characters.csv`
- `reference_model` as single select or text
- Long text for `single_image_turnaround_prompt` and `negative_prompt`
- Long text for per-view prompts and `character_tags`

### Telegram

Option 1: formatted text table

```text
🟢 S01-01 | 远景 | 平视 | 4秒 | 钩子
📍 SCENE-01：废弃殖民地入口，黄昏
📝 主角来到入口并观察周围
```

Option 2: CSV attachment

### Other Platforms

Default to CSV attachment

## Visual Prompt Template

```text
[Scene Code]: [Environment description]
[Subject]: [Character description with tags]
[Action]: [Specific action]
[Lighting]: [Time and quality]
[Camera]: [Shot type and movement]
[Quality]: [cinematic, 8k or high resolution, dynamic lighting]
[Style]: [Additional style tags]
```

### Example

```text
SCENE-01: abandoned human colony, red dust atmosphere, ruined buildings, two moons
A young woman with short white hair, red eyes, scar on right eyebrow, black tactical vest, standing at entrance
Hero surveys the area with suspicion
Orange dusk lighting, dramatic shadows
Medium shot, slow dolly in
cinematic, high resolution, shallow depth of field, dynamic lighting
```

## OpenClaw-Native Drafting

Primary usage:
- Let the skill use the current OpenClaw default LLM to understand the story and draft `characters.csv`, `relationships.csv`, and `storyboard.csv`
- Do not require the end user to configure an extra LLM just to use this skill
- Start from the bundled CSV templates and let OpenClaw fill them directly during the conversation
- Do not route core drafting through the removed `scripts/generate_storyboard.py` helper

Recommended workflow:
1. Open `assets/characters-template.csv`, `assets/relationships-template.csv`, and `assets/storyboard-template.csv` as starter schemas.
2. Draft `characters.csv` first and approve the main turnaround sheet prompts.
3. Build `relationships.csv` as a pairwise matrix for recurring character pairs that actually matter on screen.
4. Draft `storyboard.csv`, selecting only the active character pair/group for each shot beat.
5. Confirm the CSVs with the user before sending them downstream to `myreels-api`.

Authoring rules:
- Be conservative when inferring cast. Do not invent an `opponent`, `love_interest`, or extra companion unless the story actually supports it.
- Keep the review CSVs readable in the user's language; do not force English for human-facing fields
- Preserve concrete story details in `visual_prompt` even when the user writes in Chinese or Japanese; translate specifics to English instead of replacing them with generic filler.
- Keep `description` and `action` specific to each shot. Avoid repetitive rows that only restate `Hook`, `Conflict`, or other abstract phase labels.
- Use `relationship_type`, `visual_relation`, `emotional_relation`, and `blocking_pattern` to keep recurring pair shots consistent.
- In 3+ character stories, relationship guidance should be beat-aware and pair-aware, not protagonist-only.

## Project Workspace Layout

When the skill writes files for an actual user project, create a dedicated project root in the current working directory or the user-specified destination.

Recommended default root:

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

Management rules:
- Do not save generated user project files back into the skill package itself
- Create the project root before the first draft file is written
- Save working files under `drafts/`
- After user confirmation, freeze a copy under `approved/`
- Save character turnaround images under `01-characters/generated-images/raw/`
- Copy user-approved character turnaround images into `01-characters/generated-images/approved/`
- Save storyboard shot images under `04-generation/storyboard-images/raw/`
- Save storyboard videos under `04-generation/videos/raw/`
- Copy user-approved storyboard media into the matching `approved/` media folder
- Save the exact generation request payload into `requests/`
- Save task polling snapshots and task IDs into `tasks/`
- Save generation metadata into `metadata/`, including model, mode, aspect ratio, seed if available, source asset refs, timestamps, and returned URLs
- Keep request / task / metadata filenames aligned with the output artifact version
- Record major confirmation decisions in `05-review/review-log.md`
- Summarize the final approved artifact set in `06-delivery/manifest.md`

### Reproducibility Notes

For stable reruns, keep sidecar records for each generated artifact:

```text
character-C001-turnaround.v1.request.json
character-C001-turnaround.v1.task.json
character-C001-turnaround.v1.meta.json
shot-S01-01.v2.request.json
shot-S01-01.v2.task.json
shot-S01-01.v2.meta.json
video-S01-01.v1.request.json
video-S01-01.v1.task.json
video-S01-01.v1.meta.json
```

Recommended metadata fields:
- `artifact_id`
- `artifact_type`
- `source_csv`
- `model`
- `mode`
- `prompt`
- `negative_prompt`
- `aspect_ratio`
- `duration`
- `seed`
- `source_images`
- `task_id`
- `created_at`
- `completed_at`
- `output_urls`
- `local_output_paths`

Rerun rule:
- Before rerunning, load the latest request, task, and metadata sidecars for that artifact.
- Reuse the latest approved settings unless the user explicitly asks to change them.
- If any material generation parameter changes, write a new version instead of mutating the old record.

## Shot Rhythm Reference

| Duration | Typical Shot Count | Per-Shot Average |
|----------|-------------------|------------------|
| 30s | 8-10 shots | 3-4s |
| 60s | 15-20 shots | 3-4s |
| 120s | 30-40 shots | 3-4s |

## Quality Checklist Per Shot

Before marking as `done`:

- [ ] Character matches design (`character_tags`)
- [ ] Scene matches `scene_code`
- [ ] Lighting direction is consistent
- [ ] Motion is physically plausible
- [ ] Safe zones are respected for vertical crops
- [ ] Emotion matches intended feeling
- [ ] Duration is appropriate for the shot content
