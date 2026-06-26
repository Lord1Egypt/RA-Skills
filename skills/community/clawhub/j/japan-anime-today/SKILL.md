---
name: japan-anime-today
description: 查询并整理“今天/指定日期日本动画新番”的播出或官方配信信息，输出中文表格。Use when the user asks for today's Japanese anime releases, 新番时间表, 日本动画今日更新, anime airing today in Japan, or a specific date's Japan anime schedule with title / platform / time / episode number.
---

# 今日日本动画新番

## Overview

Use this skill to turn a relative or absolute date into a verified Japanese anime schedule, then present it in Chinese as: `作品名 / 平台 / 时间 / 第X话`.

The information is time-sensitive. Always browse or use current schedule sources before answering; do not rely on memory.

## Workflow

1. Resolve the date and timezone.
   - If the user says "今天", use the current date in the user's timezone, then state the absolute date.
   - For Japan schedules, report times in JST. China is UTC+8 and Japan is UTC+9; convert only when the user asks for local time.
   - Treat Japanese TV notation such as `24:30` or `25:58` as late-night notation for the next calendar day, but keep the broadcaster's notation in the table.

2. Build a candidate list.
   - Search in Japanese first, for example:
     - `{YYYY年M月D日} アニメ 番組表`
     - `今日 アニメ 放送予定`
     - `{YYYY} 春アニメ 木曜日 放送時間`
     - `{作品名} 公式 放送 配信 第{N}話`
   - Include current-season TV anime, web anime, and shorts if they have a new episode premiere that day.
   - Exclude reruns, movies, recap specials, live-action programs, and non-Japanese animation unless the user asks for them.

3. Prefer authoritative sources.
   - Best: official anime site, official X/news post, official streaming page, broadcaster program page.
   - Good cross-checks: Japanese TV guides such as G-GUIDE/bangumi.org, broadcaster schedules, dアニメストア, ABEMA, DMM TV, U-NEXT, Netflix, Prime Video, AnimeFesta.
   - Season trackers such as Kansou.me, AniChart, or LiveChart are useful for discovery, but verify platform/time/episode against official or TV-guide sources when possible.

4. Verify episode numbers.
   - Prefer explicit `第X話`, `#X`, episode title pages, streaming episode pages, or TV-guide entries.
   - If a source lists the show but not the episode number, cross-check another source.
   - Only infer by weekly count from premiere date as a last resort, and mark it as an inference.
   - Do not invent Chinese titles or episode numbers. If the accepted Chinese title is unclear, use `中文暂译（日本原名）` or just the Japanese original.

5. Normalize and deduplicate.
   - If multiple stations air the same episode, show the earliest TV platform and time first, then major official streaming platforms if relevant.
   - If a streaming platform premieres before TV, use that platform/time as the primary row.
   - If regional stations differ, keep the row concise: `AT-X / TOKYO MX` or `TBS系`.
   - Sort by JST time ascending, preserving `24:xx`/`25:xx` after `23:xx`.

## Output

Respond in Chinese. Use this table exactly unless the user asks for another format:

| 作品名 | 平台 | 时间 | 第X话 |
|---|---|---:|---|
| 作品中文名（原名，如需要） | 平台 | JST 时间 | 第 X 话 |

After the table, add short notes only when useful:

- State the date and timezone, for example: `按 2026 年 4 月 30 日日本时间整理。`
- Explain late-night notation: `24:xx/25:xx 是日本电视台深夜记法，实际为次日凌晨。`
- Include source links used for verification.
- If a result cannot be verified, write `待确认` and explain the gap in one sentence.

## Quality Bar

- Prefer fewer verified rows over a broad but weak list.
- Avoid long quoted text from sources; summarize schedule facts.
- If sources conflict, use official pages over aggregators and mention the conflict briefly.
- Keep the final answer focused on the requested fields, not a research log.
