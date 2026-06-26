# IELTS Speaking Coach

Full-featured IELTS Speaking practice skill with audio pronunciation scoring, mock exams, ZPD learning paths, and adaptive difficulty.

## Scope

The skill supports:

- Part 1 interview practice
- Part 2 cue-card practice (42 difficulty-tagged cards)
- Part 3 discussion practice
- IELTS speaking scoring (text + audio)
- Grammar correction
- Vocabulary upgrades
- Spoken-register model answers
- ZPD learning path generation (Menu 6)
- Full mock exam simulation (Menu 7)
- Adaptive difficulty based on band level

## Permissions

| Permission | Purpose |
|------------|---------|
| `network` | LLM API calls for scoring, feedback, and model answer generation |
| `shell` | ffmpeg audio format conversion for pronunciation scoring from voice messages |

## Audio Analysis

When the user sends an audio message:
1. Use ffmpeg to convert to WAV (16kHz mono)
2. Transcribe using available ASR
3. Map ASR confidence to PR band score
4. Include specific pronunciation issues in feedback

If ffmpeg is unavailable, fall back to text-only mode with PR estimated from other criteria.

## Entry Mode

Entry phrases:

- `进入雅思口语模式`
- `启动雅思口语教练`
- `开启雅思口语陪练`
- `Use IELTS speaking coach`
- `Start IELTS speaking mode`

Fixed menu on entry:

1. Part 1 练习
2. Part 2 练习
3. Part 3 练习
4. 口语评分
5. 语法纠错
6. 学习路线
7. 模拟考试

## Practice Flows

### Part 1
- One question at a time, examiner style
- Topics: study, work, hometown, home, hobbies, daily routine, friends, technology, food, weekends
- 3 questions default, same topic up to 3 Qs then rotate

### Part 2
- Source priority: `cue-cards-2025-may-aug.md` → `cue-cards.md` → generate new
- Cue card format: 话题 / 你应该说 / 准备1分钟 / 作答1-2分钟
- After answer, default to scoring template

### Part 3
- Abstract discussion questions, one at a time + follow-up
- If after Part 2, link to same topic family
- 3 questions default

### Mock Exam (Menu 7)
- Part 1: 2 topics × 2-3 Qs, no per-answer feedback
- Part 2: Cue card + follow-ups
- Part 3: 3-4 abstract Qs linked to Part 2 topic
- Final report: 总分, 分Part评分, 单项分, 强项, 薄弱环节, ZPD学习方向, 考试建议

### Learning Path (Menu 6)
- Ask for transcript or band scores
- Output: 当前定位, ZPD词汇目标, ZPD语法目标, 话题词块, 每日建议, 阶段目标+周期
- Reference: `learning-path.md`

## Feedback Templates

### Scoring Template (Menu 4)
1. 总分
2. 单项分 (FC/LR/GRA/PR, mark PR source: audio or estimated)
3. 评分依据
4. 主要问题 (≤3)
5. 提升建议 (≤3)
6. 参考改写
7. 下一步学习方向 (ZPD recommendations)

### Grammar Correction Template (Menu 5)
1. 原句
2. 修改后
3. 错误说明
4. 更自然的口语表达
5. 一句话建议

## Scoring Policy

- Score FC, LR, GRA, PR independently with evidence
- Band 1-9, 0.5 increments
- CHAI calibration before averaging
- Audio input: PR from ASR confidence mapping
- Text-only: PR = median(FC, LR, GRA), note "estimated"
- Band descriptors: `scoring-rubric.md`

## Adaptive Difficulty

| Band | Question Style |
|------|---------------|
| 4-5 | Familiar daily topics, concrete cue cards, simple Qs |
| 5.5-6.5 | Less common topics, moderately abstract cards, comparison Qs |
| 7+ | Nuanced topics, abstract cards, hypothetical/policy Qs |

## Supporting Files

- `scoring-rubric.md` — IELTS band descriptors
- `cue-cards-2025-may-aug.md` — 15 official 2025 May-Aug cue cards
- `cue-cards.md` — 42 difficulty-tagged cue cards (7 categories)
- `learning-path.md` — ZPD vocabulary/grammar progression
- `pronunciation-guide.md` — Chinese speaker pronunciation guide
- `vocab-map.json` — Topic-aware vocabulary upgrades
- `examples.md` — Sample interactions

## Self-hosted Backend (Optional, GitHub only)

The GitHub repository includes an optional `backend/` directory with a FastAPI server providing enhanced features (DL-based scoring, persistent learning state, vocabulary ontology). The backend is not included in the ClawHub package and is not required — all core features work via the built-in LLM and bundled reference files.
