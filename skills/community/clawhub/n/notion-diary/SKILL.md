---
name: notion-diary
description: Write diary entries or short 24-hour reports in Chinese or English, then sync them into Notion using a user-supplied NOTION_API_KEY and the bundled Python script. Use when the user invokes /notion_diary, asks to write a diary with one of four preset styles, wants command-driven journal input, wants to authorize Notion by filling an API key, wants to sync diary text or photo notes into Notion, or wants a fallback short report generated from the last 24 hours of conversation when no diary was written today.
metadata: {"openclaw":{"emoji":"📝","homepage":"https://docs.openclaw.ai/skills","requires":{"bins":["python3"],"env":["NOTION_API_KEY"]},"primaryEnv":"NOTION_API_KEY","install":[{"id":"brew-python","kind":"brew","formula":"python","bins":["python3"],"label":"Install Python 3 (brew)","os":["darwin"]}]}}
user-invocable: true
homepage: https://docs.openclaw.ai/tools/skills
---

# Notion Diary

Use this skill to turn user input into a diary entry or a short 24-hour report, then sync it into Notion through the bundled Python helper at `{baseDir}/scripts/notion_diary_sync.py`.

## Command Surface

OpenClaw sanitizes the skill name to the slash command `/notion_diary`.

Accept these command patterns:

- `/notion_diary diary style=<plain|gentle|reflective|lyrical>`
- `/notion_diary diary date=<YYYY-MM-DD> style=<...>`
- `/notion_diary report24h style=<plain|gentle|reflective|lyrical>`
- `/notion_diary auto style=<...>`

Chinese aliases are also valid:

- `diary` -> `日记`
- `report24h` -> `日报`
- `auto` -> `自动`

Treat the first token after `/notion_diary` as the mode. Parse `date=` and `style=` when present. Everything else in the message is source material for the entry.

## Style Presets

Support exactly four preset styles. Read [references/style-presets.md](references/style-presets.md) before drafting when the user does not define their own style.

- `plain`: concise, factual, diary-as-log.
- `gentle`: warm, smooth, personal.
- `reflective`: restrained, lived-in, slightly introspective. Prefer this by default.
- `lyrical`: more scene and atmosphere, but still grounded.

If the user gives no style, use:

1. `reflective` when the material contains emotion, travel, or relationships.
2. `plain` when the material is mostly work updates.

## Authorization And Runtime Inputs

This skill expects `NOTION_API_KEY` to be injected by OpenClaw. Read [references/openclaw-config.example.jsonc](references/openclaw-config.example.jsonc) before first use.

Keep this package registry-safe:

- Do not bundle real API keys.
- Do not bundle personal page ids, data source ids, or workspace-specific URLs.
- Keep the example config fully placeholder-based so the skill can be published to ClawHub safely.

Optional environment variables:

- `NOTION_DIARY_DATA_SOURCE_ID`: preferred existing target.
- `NOTION_DIARY_DATABASE_ID`: existing database id if the data source id is not known.
- `NOTION_DIARY_PARENT_PAGE_ID`: parent page used to find or create the `Daily Journal` database.
- `NOTION_DIARY_DATABASE_NAME`: default database title. Defaults to `Daily Journal`.
- `NOTION_DIARY_DEFAULT_STYLE`: default style code. Defaults to `reflective`.

Prefer `NOTION_DIARY_DATA_SOURCE_ID` when available. If it is missing, use `NOTION_DIARY_DATABASE_ID`. If both are missing, use `NOTION_DIARY_PARENT_PAGE_ID` to locate or create the diary database.

The script creates a date-ready database schema. If you want a visible calendar layout in Notion, create the calendar view once in the Notion UI using the `Date` property.

## Diary Workflow

1. Parse the mode, date, and style.
2. Gather the raw diary material from the command body, the attached text, and the current conversation context.
3. Draft a first-pass diary in the requested style without inventing facts.
4. After the first pass, ask 1 to 3 targeted follow-up questions that help deepen missing moments, transitions, or emotional shifts.
5. Revise the diary with the user's answers.
6. Create or update the Notion entry for that date through the bundled script.

Only skip the follow-up questions when one of these is true:

- the user explicitly says to sync immediately
- the material is already complete enough for a polished diary
- the mode is `report24h` and the user asked for a short brief rather than a refined diary

Prefer titles in this shape:

- `YYYY-MM-DD | 一句话主题`

Prefer a short summary sentence for the Notion `Summary` property.

## Follow-Up Question Rules

Ask questions that improve the diary rather than expand it mechanically.

- Prefer questions about one missing moment, one emotional turn, or one concrete detail.
- Ask at most 3 questions.
- Ask only what would noticeably improve the final diary.
- Keep the questions short and specific.

Good follow-up examples:

- 当时你最强烈的感受是什么？
- 下午去古城的时候，现场的状态更像是轻松、匆忙，还是有点收尾的感觉？
- 晚上学 AI 时，你是兴奋、平静，还是有点疲惫但充实？

Avoid generic questions like:

- 还有什么想补充的吗？
- 今天开心吗？
- 详细说说。

## 24-Hour Report Workflow

Use this mode when:

- the user explicitly invokes `report24h` or `日报`
- the user invokes `auto` and there is no usable diary material for today
- the user asks for a short daily recap instead of a full diary

Before drafting a 24-hour report:

1. Use `sessions_list` to identify the current sender's most relevant session from the last 24 hours.
2. Prefer the literal key `main` for direct chat when it is clearly the active thread.
3. Use `sessions_history` to fetch the recent transcript. Keep `includeTools` off unless tool outputs are part of the substance the user wants summarized.
4. Summarize only the last 24 hours of visible conversation for the relevant session. Do not pull unrelated sessions unless the user explicitly asks for a broader recap.

The 24-hour report must stay shorter than a full diary:

- 1 short summary paragraph
- 2 to 5 bullets or short paragraphs for key actions, blockers, and progress
- no embellished storytelling unless the user explicitly asks for it

If a proper diary entry for today already exists and the user asks for `auto`, prefer updating that diary instead of generating a separate short report.

## Photo Handling

When the user provides one or more photos, insert image placement markers into the content before calling the sync script:

- `[[image:1]]`
- `[[image:2]]`

Each marker must appear on its own line between paragraphs. Pass the real local file paths or public URLs through repeated `--image` arguments to the script in the same order.

If there are images but no obvious placement, append them after the body.

When image paths or public image URLs are available, the sync should do all three:

- insert the photos into the page body at the matching marker positions
- write the photos into the Notion `Photos` property
- use the first valid photo as the page cover

## Sync Script

Use `{baseDir}/scripts/notion_diary_sync.py`.

Typical calls:

```bash
python3 {baseDir}/scripts/notion_diary_sync.py lookup \
  --date 2026-03-28 \
  --mode diary
```

```bash
python3 {baseDir}/scripts/notion_diary_sync.py sync \
  --date 2026-03-28 \
  --mode diary \
  --style reflective \
  --title "2026-03-28 | 曼谷的最后一天" \
  --summary "曼谷最后一天的收尾、想念和被回应。" \
  --content-file /tmp/diary.txt \
  --image /absolute/path/photo1.jpg
```

```bash
python3 {baseDir}/scripts/notion_diary_sync.py sync \
  --date 2026-03-28 \
  --mode report \
  --style plain \
  --title "2026-03-28 | 24h 简短日报" \
  --summary "过去 24 小时的工作与交流简报。" \
  --content-file /tmp/report.txt
```

The script will:

- find or create the diary database
- create or update the page for the target date and mode
- store the body in page content
- keep `Title`, `Date`, `Mode`, `Style`, and `Summary` properties in sync
- best-effort upload local images up to 20 MB through the Notion file upload API
- populate the `Photos` property and page cover when photos are provided

## Drafting Rules

- Mirror the user's language unless asked otherwise.
- Keep facts intact and do not invent details.
- For `plain`, optimize for clear sequence and compactness.
- For `gentle`, allow warmth but keep it natural.
- For `reflective`, use the user's preferred balanced style: first set the day's overall state, then move through concrete events and emotional changes gradually.
- For `reflective`, the priority is not “more literary”; the priority is natural pacing, light transitions, and a sense of inner movement without over-writing.
- Let the sentences breathe a little, but keep them readable and grounded.
- For `lyrical`, add atmosphere lightly; do not become purple or melodramatic.

## Failure Handling

- If the Notion API key is missing, explain that the skill needs `skills.entries["notion-diary"].apiKey` or `NOTION_API_KEY`.
- If the integration cannot access the target page or database, ask the user to share the parent page with the integration and provide the correct page or data source id.
- If image upload fails, keep the diary sync successful and add a short text fallback instead of failing the whole run.
- If some images fail but others succeed, keep the successful photos in Notion and fall back to text only for the failed ones.
- If session history is unavailable for `report24h`, summarize only the visible recent chat and say that the report used a limited context window.

## Resources

- Read [references/style-presets.md](references/style-presets.md) for the four voice presets.
- Read [references/openclaw-config.example.jsonc](references/openclaw-config.example.jsonc) for OpenClaw configuration and env injection.
- Read [references/notion-rest-notes.md](references/notion-rest-notes.md) when changing the sync script or the Notion schema.
