---
name: office-comic-relief
description: Generate simple, warm, humorous Chinese vertical comics (3:4) for office workers. Use when the user wants A/B dialogue-based stress-relief comic content where A is a supportive duck and B is a ranting frog, with short emotionally resonant workplace scenes, then generate a final colored comic image via Gemini image model (preferred: gemini banana nano 2).
---

# Office Comic Relief

Generate a low-complexity, emotionally resonant comic for office workers in two steps.

## Workflow

1. Create the script with Gemini conversation style.
2. Generate image prompt and produce final comic image.

Keep outputs concise, warm, humorous, and practical.

## Step 1 — Dialogue Script (Gemini first)

Generate 1 short scene with:
- Audience: office workers after work
- Tone: warm + humorous + comforting
- Complexity: low
- Format: A/B dialogue only
- Character roles:
  - A: duck, companion/supporter
  - B: frog, ranting worker

Constraints:
- 4–8 dialogue lines total
- Each line should be short and colloquial Chinese
- Focus one daily pain point only (overtime, meetings, unclear requirements, KPI anxiety, commute exhaustion, etc.)
- End with a tiny emotional release or hope
- Do not include narration labels like “画面建议/分镜说明/角色名说明” in final text for the image

Recommended generation prompt for script:

```text
请写一段适合“打工人下班后解压”的双人对话漫画脚本。
角色设定：A是鸭子（陪伴者，温暖幽默），B是青蛙（吐槽者，打工人）。
要求：
1) 仅输出对话内容，每句加中文引号；
2) 共4-8句，简短口语化；
3) 聚焦一个职场困境；
4) 结尾有被理解和放松感；
5) 不要输出任何旁白、分镜建议、角色名、说明文字。
```

## Step 2 — Comic Image Generation (Gemini banana nano 2 preferred)

Render one colored comic image.

Hard constraints:
- Vertical ratio 3:4
- Chinese text
- Top-bottom layout (上下格式)
- Style: warm, humorous, soft color palette
- No role names shown in image (do NOT print “青蛙B”“鸭A”等)
- Dialogues appear as quoted Chinese text only
- Avoid extra meta text

Image prompt template:

```text
彩色治愈系职场解压漫画，竖版3:4，上下分区排版。
主角为一只可爱黄色鸭子（陪伴者）和一只绿色青蛙（吐槽的打工人），
风格温暖幽默，柔和光影，线条干净，适合社交媒体发布。
画面表现下班后放松场景（如路边长椅/便利店门口/地铁站外）。
在画面中只放中文对话气泡，内容如下：
{{DIALOGUES_WITH_QUOTES}}
不要出现角色名字标注，不要出现“画面建议”“角色设定”等说明性文字。
```

If model supports sizing/aspect params, set aspect ratio to 3:4 explicitly.

## Output

Return:
1) Final dialogue used
2) Generated image file/result for user delivery

If image model call fails, keep dialogue and provide a single retry with the same constraints and simplified background.