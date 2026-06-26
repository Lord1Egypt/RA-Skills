---
name: pans-meeting-summarizer
description: |
  AI算力销售会议智能总结工具。从会议录音或文字记录自动生成结构化纪要、行动项和客户洞察，支持同步更新CRM系统。
  触发词：会议纪要, 会议总结, 录音转文字, 待办提取, 客户洞察, meeting minutes, call notes, action items, CRM更新
---

# pans-meeting-summarizer - AI算力销售会议纪要生成器

## 描述
AI算力销售会议智能总结工具。从会议录音或文字记录自动生成结构化纪要、行动项和客户洞察，支持同步更新CRM系统。

## 触发词
会议纪要, 会议总结, 录音转文字, 待办提取, 客户洞察, meeting minutes, call notes, action items, CRM更新

## 功能特性
- 🎙️ 音频转录：支持多种音频格式（m4a/wav/mp3）转文字
- 📝 智能纪要：自动提取会议要点、决策、讨论内容
- ✅ 行动项：识别待办事项、负责人、截止时间
- 🔍 客户洞察：分析客户需求、痛点、预算、决策链
- 🔄 CRM同步：一键更新客户跟进记录到CRM系统

## 使用方式
\`\`\`bash
# 从音频生成纪要
python scripts/summarize.py --audio meeting.m4a --output notes.md

# 从文字记录生成纪要
python scripts/summarize.py --text transcript.txt --output notes.md

# 生成纪要并同步CRM
python scripts/summarize.py --audio meeting.m4a --sync-crm --client "腾讯云"

# 指定输出格式
python scripts/summarize.py --text transcript.txt --format json --output notes.json
\`\`\`

## CLI 参数
- \`--audio\`: 音频文件路径（支持 m4a/wav/mp3）
- \`--text\`: 文字记录文件路径
- \`--output\`: 输出文件路径（默认 stdout）
- \`--format\`: 输出格式（markdown/json，默认 markdown）
- \`--sync-crm\`: 同步更新CRM系统
- \`--client\`: 客户名称（CRM同步时需要）
- \`--help\`: 显示帮助信息

## 输出内容
### 会议纪要
- 会议主题、时间、参与人
- 讨论要点、决策事项
- 下一步计划

### 行动项
- 待办事项清单
- 负责人、优先级、截止时间

### 客户洞察（销售场景）
- 预算情况
- 决策链分析
- 竞品情况
- 痛点需求
- 购买信号

## 依赖
- OpenAI Whisper（音频转录）
- OpenAI API（摘要生成）

## 适用场景
- 客户会议后快速生成跟进记录
- 销售复盘和团队协作
- CRM数据自动化更新
- 会议效率提升

---
AI算力销售工具集 | 提升销售效率