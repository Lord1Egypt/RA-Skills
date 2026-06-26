---
name: meeting-minutes-assistant
description: 将会议录音转成结构化会议纪要。适用于用户上传会议音频后，希望通过 ASR 转写、LLM 总结和可选 TTS 播报，自动提取会议主题、讨论要点、决策和行动项的场景。输入支持 `audio_file`、`need_voice_summary`、`language`；默认输出 JSON 结构化纪要，并可附带语音摘要文件路径。
---

# AI Meeting Minutes Assistant

## 适用范围

此 Skill 用于把会议音频整理成结构化会议纪要。

默认能力：
- 使用 ASR 将会议录音转成文本
- 清理口头禅和重复表达，提高可读性
- 使用 LLM 输出结构化纪要
- 可选用 TTS 生成语音摘要

不做：
- 多说话人身份精准识别
- 视频内容分析
- 会议知识库检索
- 实时流式会议转录

## 输入

默认输入字段：
- `audio_file`
- `need_voice_summary`
- `language`

默认值：
- `need_voice_summary`: `false`
- `language`: `zh`

## 输出

默认返回 JSON，字段包括：
- `topic`
- `discussion_points`
- `decisions`
- `action_items`
- `cleaned_transcript`
- `voice_summary_path`

字段结构见 [references/output_schema.md](references/output_schema.md)。

## 工作流

按以下顺序执行：

1. 校验输入
   - 确认 `audio_file` 存在且可读
   - 过短音频直接报错，不进入总结流程

2. 执行 ASR
   - 调用 SenseAudio ASR 接口
   - 返回原始 `transcript`

3. 清理转写文本
   - 去除明显口头禅、重复停顿和无意义填充词
   - 保留事实、结论、人名和行动项

4. 生成会议纪要
   - 将清理后的文本交给 LLM
   - 输出主题、讨论要点、决策和行动项
   - 结果必须是结构化 JSON

5. 可选生成语音摘要
   - 若 `need_voice_summary=true`
   - 用 TTS 把简短总结转成音频

6. 返回结果
   - 返回结构化纪要
   - 同时保存本地 JSON 文件

## LLM 要求

- 优先提炼会议主题
- `discussion_points` 只保留核心讨论点
- `decisions` 只写明确形成的结论
- `action_items` 尽量保留责任人和待办事项
- 如果转写中缺少信息，不要编造
- 输出必须为 JSON

Prompt 模板见 [references/prompts.md](references/prompts.md)。

## 错误处理

以下情况要明确返回错误：
- 音频过短：`Meeting audio too short to summarize`
- ASR 失败：`Speech recognition failed`
- 文本过长：按块总结后再聚合

## 直接运行

运行脚本：
- `scripts/run_meeting_minutes.py`

安装依赖：
- `pip install -r requirements.txt`

环境变量参考：
- [/.env.example](/mnt/cache/liudelong/cws/code6/openclaw-skill/meeting_record/.env.example)

示例：

```bash
python scripts/run_meeting_minutes.py --audio-file ./meeting.wav --need-voice-summary
```

接口约定：
- LLM 默认使用 `https://models.audiozen.cn/v1`
- ASR/TTS 默认使用 `https://api.senseaudio.cn`

## 注意事项

- 纪要应突出事实、结论和待办，不要写成长篇复述
- 清理文本时不要删掉关键人名、时间、数字和决策
- 行动项尽量保留“谁做什么”
