# IELTS Speaking Coach — Testing Guide

## Quick Checks

### 1. Entry mode

Test one of these phrases:

- `进入雅思口语模式`
- `启动雅思口语教练`
- `Use IELTS speaking coach`

Expected result: the skill returns the fixed 1-7 menu.

### 2. Menu selection

Reply with:

- `1` for Part 1
- `2` for Part 2
- `3` for Part 3
- `4` for scoring
- `5` for grammar correction
- `6` for learning path
- `7` for mock exam

Expected result: the skill maps numeric replies correctly.

### 3. Audio pronunciation scoring

Send a voice message in scoring mode.

Expected result:
- ffmpeg converts audio to WAV
- ASR transcribes the audio
- PR score is based on ASR confidence (not estimated)
- Output notes "PR: 音频实测" instead of "无音频估算"

### 4. Text-only fallback

Send a text transcript in scoring mode (no audio).

Expected result:
- PR is estimated from median of FC, LR, GRA
- Output notes "PR: 无音频估算"

### 5. Part 2 cue card source

Enter Part 2 mode and verify that the cue card comes from:

1. `cue-cards-2025-may-aug.md` first
2. `cue-cards.md` second (42 cards with difficulty tags)

### 6. Scoring template

Send a short transcript in scoring mode and verify the output contains:

1. 总分
2. 单项分
3. 评分依据
4. 主要问题
5. 提升建议
6. 参考改写
7. 下一步学习方向

### 7. Grammar correction template

Send a sentence with a clear spoken grammar mistake and verify the output contains:

1. 原句
2. 修改后
3. 错误说明
4. 更自然的口语表达
5. 一句话建议

### 8. Learning path (Menu 6)

Send "6" or "学习路线" and provide band scores.

Expected result:
- 当前定位
- ZPD词汇目标 (5-8 words)
- ZPD语法目标 (2-3 structures)
- 话题词块
- 每日建议
- 阶段目标+周期

### 9. Mock exam (Menu 7)

Send "7" or "模拟考试".

Expected result:
- Part 1 → Part 2 → Part 3 sequential flow
- No per-answer feedback during test
- Final comprehensive report at the end

### 10. Adaptive difficulty

Test with different band levels:
- Band 5: Should get familiar daily topics
- Band 7: Should get abstract/hypothetical questions

## Notes

- This release requires `shell` permission for ffmpeg/ASR audio processing.
- If ffmpeg is not installed, audio features will be unavailable but text-only mode still works.
- Optional backend API at `http://host.docker.internal:8081` for persistent learning state.
