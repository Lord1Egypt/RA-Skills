# Character Design Reference

## Three-View Character Sheet (三视图)

Character design should establish consistent visual elements for AI prompt injection.

This skill should treat the character sheet as a design board, not as a hero illustration.
When the user asks for "角色生图", "角色设计", "人物设定", or "角色参考图", default to a single-image three-view turnaround sheet unless the user explicitly asks for another format.

Default output for character generation:
- Generate one image containing the same character's `front view`, `side view`, and `back view`
- Use a clean character-sheet / turnaround layout, not three unrelated images
- Keep the same outfit, body proportions, hairstyle, and accessories across all three views
- Use full-body standing pose, neutral expression, and simple background unless the user asks otherwise
- Prefer `nano-banana2` as the first-choice model for three-view character sheets
- Prefer orthographic / product-sheet / design-approval language over cinematic illustration language
- Treat this as the canonical character reference image that downstream storyboard prompts should follow

### Standard Fields

| Field | Description |
|-------|-------------|
| `name` | Character name |
| `story_role` | Role in the story, e.g. protagonist / opponent / companion |
| `relation_to_main` | Relationship to the protagonist, e.g. self / conflict / ally / romance |
| `age` | Approximate age |
| `gender` | Gender |
| `ethnicity` | Ethnicity (for diversity in generation) |
| `hair` | Hairstyle, color, length |
| `eyes` | Eye color, shape |
| `face` | Distinctive facial features (mole, scar, etc.) |
| `build` | Body type, height impression |
| `outfit` | Typical clothing |
| `accessories` | Jewelry, glasses, weapons, etc. |
| `personality` | Key personality traits |
| `reference_model` | Recommended base model for the turnaround sheet, usually `nano-banana2` |

### Target Layout

Use a single-sheet composition like this:

```
┌──────────────────────────────────────────────────────────────┐
│ CHARACTER SHEET / TURNAROUND                                │
│                                                              │
│   FRONT VIEW        SIDE VIEW         BACK VIEW              │
│   full body         full body         full body              │
│   same scale        same scale        same scale             │
│   neutral pose      neutral pose      neutral pose           │
│   clean bg          clean bg          clean bg               │
└──────────────────────────────────────────────────────────────┘
```

### Composition Rules

When writing prompts for character generation, prefer these constraints:

1. One canvas, three full-body views of the same character
2. Front, side profile, and back arranged left-to-right
3. Same camera distance and scale in all three views
4. Neutral standing pose with arms relaxed unless costume details require otherwise
5. Plain light background, studio lighting, minimal shadows
6. No action scene, no dramatic composition, no environment storytelling
7. No extra characters, no duplicate random poses, no cropped limbs
8. Prioritize readable silhouette and costume structure over mood or atmosphere
9. If the costume has asymmetrical details, make sure they remain consistent in all views
10. If the user does not ask for expression sheets or costume variants, do not add them in the first pass

### Default Skill Output

When the skill prepares character design output, provide these four blocks:

1. `character_tags`
2. `single_image_turnaround_prompt`
3. `view_notes` for `front`, `side`, `back`
4. `negative_prompt`

Suggested structure:

```text
CHARACTER: [Name]
STORY_ROLE: [protagonist / opponent / companion / love_interest]
RELATION_TO_MAIN: [self / conflict / ally / romance]
REFERENCE_MODEL: [Usually nano-banana2]
CHARACTER_TAGS: [distinctive reusable tags]
SINGLE_IMAGE_TURNAROUND_PROMPT: [English prompt that explicitly asks for one image with front/side/back views]
VIEW_NOTES:
- FRONT: [key readable details from the front]
- SIDE: [key silhouette / profile / side accessories]
- BACK: [hair back shape / costume back details]
NEGATIVE_PROMPT: [consistency and layout suppression terms]
```

### Prompt Structure For Character Sheets

Use English for the actual generation prompt:

```text
Character turnaround sheet, one image with three full-body views of the same character, front view, side view, back view, aligned left to right, consistent proportions, same outfit, same hairstyle, neutral standing pose, clean white background, studio lighting
```

Add the character-specific details after the structure:

```text
Character turnaround sheet, one image with three full-body views of the same character, front view, side view, back view, aligned left to right, consistent proportions, same outfit, same hairstyle, neutral standing pose, clean white background, studio lighting. A young woman, short black hair, sharp eyes, pale skin, slim athletic build, wearing a black leather jacket, dark fitted pants, black boots, silver hoop earring on left ear.
```

For stronger control, append a layout-locking suffix:

```text
design reference board, model sheet, character approval sheet, orthographic feel, exact same character shown three times, not three different people, no action pose, no cinematic scene
```

### Recommended Prompt Keywords

Useful keywords:
- `character sheet`
- `turnaround sheet`
- `three-view character design`
- `front view side view back view`
- `full body`
- `same character`
- `consistent design`
- `orthographic feel`
- `clean background`
- `studio lighting`

Avoid or explicitly suppress:
- `strong action pose`
- `dynamic camera`
- `cinematic scene`
- `crowd`
- `multiple characters`
- `cropped`
- `close-up`
- `busy background`

### Suggested Negative Prompt

```text
extra characters, duplicate character, inconsistent outfit, inconsistent hairstyle, dynamic action pose, cropped body, close-up portrait, busy background, weapon swing, dramatic perspective, extreme foreshortening, text, watermark
```

Stronger fallback negative prompt:

```text
three different characters, mixed costume details, inconsistent face, inconsistent hair length, missing back view, missing side view, dramatic camera angle, perspective distortion, kneeling pose, seated pose, hand covering outfit, props blocking body, split panels with different scenes
```

### Prompt Template

```text
[STYLE], character turnaround sheet, one image with three full-body views of the same character, front view, side view, back view, aligned left to right, same scale, consistent proportions, same outfit, same hairstyle, neutral standing pose, clean background, studio lighting, [CHARACTER DETAILS], [OPTIONAL QUALITY TAGS]
```

Example:

```text
semi-realistic anime style, character turnaround sheet, one image with three full-body views of the same character, front view, side view, back view, aligned left to right, same scale, consistent proportions, same outfit, same hairstyle, neutral standing pose, clean light-gray background, soft studio lighting, a 25-year-old Asian woman with short white hair, red eyes, scar on right eyebrow, athletic build, black tactical vest, dark cargo pants, mechanical left arm, black combat boots, high detail
```

### Practical nano-banana2 Pattern

Empirical note:
- `nano-banana2` responds well to concise subject-first phrasing such as `A stunningly beautiful Asian woman warrior three-view diagram`
- The keyword `three-view diagram` can work as a strong layout anchor
- Explicit `front view: ... side view: ... back view: ...` clauses are effective for injecting per-view details
- A wide aspect ratio such as `16:9` can help the model place the three views on one sheet
- `cinematic, high quality` can be kept as suffix quality tags, but they should come after the three-view layout instruction

Recommended nano-banana2 prompt shape:

```text
[SUBJECT], three-view diagram, white background, front view: [front details], side view: [side details], back view: [back details], high quality, 16:9
```

Suggested strengthened version for consistency-heavy tasks:

```text
[SUBJECT], character turnaround sheet, three-view diagram, one image, same character, exact same character shown three times, full-body front view, side view, back view, aligned left to right, same scale, consistent outfit, consistent hairstyle, neutral standing pose, white background, studio lighting, design reference board, front view: [front details], side view: [side details], back view: [back details], high quality, 16:9
```

Practical guidance:
- For warrior / fighter characters, a mild `battle-ready` stance may still work if the silhouette is readable
- Do not let weapons, flowing hair, or cape shapes block the body contour in side/back view
- If consistency matters more than style, switch `battle-ready pose` back to `neutral standing pose`
- If `cinematic` causes poster drift, remove it before changing the three-view structure

### Recommended Chinese Instruction Layer

If the surrounding workflow is written in Chinese, you can still keep the generation prompt in English and add a Chinese instruction note for clarity:

```text
默认输出角色三视图设定稿：一张图内同时包含正面、侧面、背面，三个人物必须是同一角色，保持服装、发型、体型、配饰一致，站姿中性，纯净背景，不要剧情感海报。
```

This helps prevent the skill from drifting into "角色海报" mode.

### Fallback Rule

If the model outputs only one pose or produces three inconsistent figures, retry with stronger layout language:

```text
single image character sheet, exact same character shown three times for design reference only, front side back views, full body, same costume, same proportions, neutral pose, no action, plain background
```

If needed, also add:
- `for model sheet reference`
- `for character design approval`
- `orthographic reference board`
- `single canvas only`
- `front side back on one sheet`
- `turnaround layout, not a poster`
- `16:9 layout`

If the model still drifts, rewrite the prompt to front-load the layout before style:

```text
One single character design sheet on a single canvas. Front view, side view, back view of the exact same character, full body, aligned left to right, identical costume and hairstyle, neutral standing pose, plain background. [STYLE AND CHARACTER DETAILS]
```

Prompt review workflow:
- Generate the first draft prompt
- Check whether the output explicitly contains `one image`, `same character`, `front view`, `side view`, `back view`, and `aligned left to right`
- Only after the layout is stable should you increase beauty, cinematic, or rendering-detail language

### Character Tag Library

Extract distinctive, consistent tags for AI prompt injection:

```
# Character: "Yuki"
TAGS: "short white hair, red eyes, scar on right eyebrow, black tactical vest, mechanical left arm"
```

**Rules for Tags:**
1. Use distinctive visual features (moles, scars, tattoos)
2. Include clothing/accessories that define the character
3. Note asymmetrical features
4. Specify colors precisely

### AI Prompt Injection

When generating any shot with this character:

```
# ❌ Without tags
"A woman fighting"

# ✅ With character tags
"A young woman with short white hair, red eyes, scar on right eyebrow, wearing black tactical vest, fighting pose, cinematic, 8k..."
```

## Multi-Character Management

For scenes with multiple characters:

```
CHARACTER-A: "Yuki" - short white hair, red eyes, scar, black vest, mechanical arm
CHARACTER-B: "Ken" - tall, buzz cut, green military uniform, scar on chin
CHARACTER-C: "Robot Dog" - four-legged, blue optical sensors, silver chassis, weapon pod
```

Recommended character-first extension:
- Create one CSV row per recurring character
- Mark each row with `story_role`
- Fill `relation_to_main` so downstream storyboard prompts can decide who appears in setup / conflict / climax shots
- Keep separate three-view sheets for protagonist and opponent if both appear repeatedly
- Only add a new character row when the story actually contains that recurring role; do not infer extra cast only from genre
- Create a matching `relationships.csv` so repeated pairings have stable `relationship_type`, `interaction_pattern`, and `prompt_hint`
- Build relationship rows for all recurring pairs that matter on screen, not only protagonist-linked pairs
- Fill `visual_relation`, `emotional_relation`, and `blocking_pattern` so multi-character shots stay consistent in both staging and mood

### Relationship Matrix

| Character Pair | Relationship | Interaction Type |
|----------------|--------------|------------------|
| Yuki ↔ Ken | Partners | Back-to-back combat |
| Yuki ↔ Robot Dog | Handler | Commands, hand signals |
| Ken ↔ Robot Dog | Wary | Initial distrust |

## Scene Consistency

Establish scene codes for environment consistency:

```
SCENE-01: "Alien Colony Base"
- Setting: Abandoned human colony, red dust atmosphere, two moons visible
- Time: Dusk, orange-red lighting
- Props: Ruined buildings, overturned vehicles, alien organic structures

SCENE-02: "Underground Tunnel"
- Setting: Dark tunnel with bioluminescent alien plants
- Time: Always dark, lit by alien flora
- Props: Ancient alien technology, water drips

SCENE-03: "Open Desert"
- Setting: Barren alien desert, rock formations
- Time: Harsh midday sun, long shadows
- Props: Sand, scattered debris
```

### Scene Prompt Injection

```
# ❌ Random
"alien planet surface with some rocks"

# ✅ Consistent
"SCENE-01: abandoned human colony, red dust atmosphere, ruined buildings, two moons in sky, orange dusk lighting, 8k, cinematic"
```

## Reference Image Workflow

1. **Generate character reference images first**
   - Default to one three-view character sheet in a single image
   - Front / Side / Back views must all be present
   - Use neutral pose and plain background for consistency
   - Approve this sheet before generating expressions or alternate outfits
   - Only create multiple expressions or key outfits as a second-stage extension

2. **Generate scene establishing shots**
   - Use scene codes in all subsequent prompts

3. **Build visual consistency across all shots**
