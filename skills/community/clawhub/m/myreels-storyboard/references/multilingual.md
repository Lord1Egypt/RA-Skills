# Multilingual Support Reference

## Supported Languages

- 🇨🇳 Chinese (zh)
- 🇯🇵 Japanese (ja)
- 🇬🇧 English (en)

## User Input Handling

### Story Input

User can input story or outline in any language:

- **Chinese**: 「一个女孩在樱花树下微笑，阳光洒落」
- **Japanese**: 「桜の下で笑う少女、陽光が差し込む」
- **English**: 「A girl smiling under a cherry tree, sunlight filtering through」

### AI Response Language

| User Language | AI Response Language | Notes |
|--------------|---------------------|-------|
| Chinese | Chinese | Storyboard descriptions in Chinese |
| Japanese | Japanese | Storyboard descriptions in Japanese |
| English | English | Storyboard descriptions in English |
| Mixed | Dominant user language | If one language clearly dominates, follow it |
| Other / Unclear | Most recent instruction language, otherwise English | Avoid arbitrary fallback to Chinese |

### visual_prompt is Always English

Regardless of user input language, the `visual_prompt` field **must be in English** for AI image generation.

Do not flatten non-English stories into generic placeholders. Translate the actual story specifics into English:
- Keep named characters, props, locations, and actions
- Preserve beat-specific information from the outline
- Avoid generic filler such as "story premise from the provided outline"

### description Field - User Language Summary

The `description` field provides a **human-readable summary** of each shot in the **user's input language**:

| User Language | description Field | Example |
|--------------|------------------|---------|
| Chinese | 中文 | "女主角在废弃殖民地入口扫描周围环境" |
| Japanese | 日本語 | "女主角が廃墟になった植民地の入り口をスキャンしている" |
| English | English | "Female lead scanning surroundings at colony entrance" |

**Purpose**: Helps user quickly understand each shot without reading the full AI prompt.

**NOT for AI generation**: This field is ignored by myreels-api; only `visual_prompt` is used for image/video generation.

Quality rule:
- Each `description` should describe the actual beat of that specific shot, not repeat a generic phase label across multiple rows

## CSV Language Policy

Keep the CSV schema stable, but localize the review content:

- Column names stay in English for schema stability
- IDs and stable codes stay machine-friendly: `character_id`, `relationship_id`, `shot_id`, `scene_code`
- User-facing values should follow the user's language across all three CSVs
- AI-facing prompt fields stay in English so the same files remain portable across models and tools

Recommended field policy:

- `characters.csv`
  Human-facing fields follow the user's language: `name`, `story_role`, `relation_to_main`, `gender`, `ethnicity`, `hair`, `eyes`, `face`, `build`, `outfit`, `accessories`, `personality`
- `characters.csv`
  Prompt-facing fields stay English: `single_image_turnaround_prompt`, `negative_prompt`, `front_view_prompt`, `side_view_prompt`, `back_view_prompt`, `character_tags`
- `relationships.csv`
  Human-facing fields follow the user's language: `character_a_name`, `character_b_name`, `relationship_type`, `visual_relation`, `emotional_relation`, `blocking_pattern`, `interaction_pattern`
- `relationships.csv`
  Prompt-facing field stays English: `prompt_hint`
- `storyboard.csv`
  Human-facing fields follow the user's language: `shot_type`, `camera_angle`, `movement`, `duration`, `description`, `action`, `dialogue`, `emotion`, `sound_fx`, `notes`, `difficulty`, `status`
- `storyboard.csv`
  Prompt-facing field stays English: `visual_prompt`

If a downstream integration later needs normalized English enums, create a separate export copy instead of replacing the user-facing review CSV.

Recommended normalized English export fields:
- `storyboard.program-en.csv`
  Normalize `shot_type`, `camera_angle`, `movement`, `emotion`, `difficulty`, `status`
- `relationships.program-en.csv`
  Normalize `relationship_type`
- `characters.program-en.csv`
  Normalize `story_role`, `relation_to_main`, and any other enum-like fields needed by automation

## Shot Terminology Reference

| English | Chinese | Japanese |
|---------|---------|----------|
| Wide / Long Shot | 远景 | 遠景 |
| Full Shot | 全景 | フルショット |
| Medium Shot | 中景 | ミディアムショット |
| Close-up | 特写 / 近景 | クローズアップ |
| Extreme Close-up | 大特写 | エクストリームクローズアップ |
| Eye-level | 平视 | レベルショット |
| Low-angle | 仰视 | 下から仰角 |
| High-angle | 俯视 | 上から俯瞰 |
| Bird's Eye | 鸟瞰 | 俯瞰ショット |
| Dutch | 荷兰角 | ダッチアングル |
| Dolly In | 推近 | ドリーイン |
| Dolly Out | 拉远 | ドリーアウト |
| Pan | 摇镜 | パン |
| Follow | 跟拍 | フォロー |
| Fixed / Static | 固定 | 固定 |
| Orbit | 环绕 | 周回 |
| Tilt | 倾斜 | ティルト |

Notes:
- Prefer standard filmmaking terminology in user-facing tables.
- Keep `visual_prompt` in English even when the human-readable `description` field is Chinese or Japanese.

## Dialogue Handling

- User-provided dialogue is kept in original language
- Recorded in the `dialogue` field without translation
- Japanese/English dialogue remains in original text

## CSV Output

CSV file encoding is UTF-8, correctly storing all three languages' characters.

## Language Resolution Guidance

Do not treat language choice as a single-message regex problem.

Use this order instead:
1. Look at the actual conversation context, not only the latest sentence.
2. If one language clearly dominates, use that for user-facing CSV values.
3. If the story is mixed-language, follow the user's most recent instruction language.
4. If no dominant language is clear, default to English instead of arbitrarily forcing Chinese.

Implementation note:
- A simple character-set detector can be used as a weak hint.
- It should not override clearer evidence from the surrounding conversation.

## Storyboard Generation Rules

1. User input → Detect the dominant language from the actual conversation context
2. Storyboard content → Generate user-facing CSV values in that dominant language
3. If the input is mixed and no dominant language is clear, use the user's most recent instruction language; otherwise default to English
4. AI-facing prompt fields such as `visual_prompt` and turnaround prompts → **Always English**, while preserving concrete story details
5. If automation needs English enums, generate a secondary `*.program-en.csv` export
6. User confirmation → Review tables and CSVs display user-language content for easy approval

## Re-run Stability

Language localization should not make reruns less reproducible.

- Keep user-facing review CSVs localized
- Keep AI-facing prompts in English
- Persist each generation request, task snapshot, and metadata sidecar next to the relevant artifact family
- On rerun, reuse the latest approved English prompt and generation parameters unless the user explicitly requests changes
