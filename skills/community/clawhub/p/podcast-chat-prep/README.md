# podcast-chat-prep：整档播客批量化速通

把一档播客几十期上百期的逐字稿，批量变成"没听过也能深度聊天"的素材包。单篇笔记是扫盲，嘉宾观点变化追踪和人设画像才是深度了解——你连他什么时候改过口都知道，这就是信息差。

朋友推荐了一档播客，你根本没时间从头听？社交场合想接话但没法编？这个工具把逐字稿提炼成金句、故事、话术和内部梗，聊天时自然引用，证明你真的听过。

## 适合谁用

- 播客重度听众，社交场景要接话的人
- 想系统研究一档播客（嘉宾、观点、主题线）的研究型听众
- 做连麦/直播，需要把音频反哺成公众号内容的人

## 快速开始

```bash
# 1. 先把音频转成逐字稿（任选其一）
#    通义听悟（免费，网页上传）/ 飞书妙记 / 剪映字幕导出

# 2. 把逐字稿喂给 AI，按 SKILL.md 流程生成素材包
```

零依赖，clone 下来就能用。只需逐字稿 markdown，不需要装任何环境。

## 文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 完整流程：批量化分析→观点追踪→人设画像→素材库 |
| `assets/episode-template.md` | 单期笔记模板（7 模块） |
| `assets/summary-template.md` | 跨期总结模板（观点演变时间线+人设画像） |
| `assets/chat-material-template.md` | 聊天素材库模板（话术库+内部梗） |

## 核心能力

- **批量化处理**：同一档播客 ≥3 期自动启动跨期追踪，几十期几百期都能处理
- **单期笔记**：7 模块，金句原文引用、标注发言人
- **嘉宾观点变化追踪**：跨期对比同一话题说法，标注维持/升级/改口/打脸，输出演变时间线
- **嘉宾人设画像**：跨期串联故事和说话习惯，至少 2 期以上才下结论
- **聊天素材库**：话术库、多视角碰撞、内部梗、N 分钟速记
- **内容反哺**：连麦场景提炼公众号素材，按账号人设分类

## 推荐流程

1. 音频 → 通义听悟/飞书妙记/剪映 → 带时间戳的逐字稿
2. 预处理：标注发言人、清理填充词
3. 批处理单期笔记（每期一个）
4. 跨期追踪：观点演变时间线 + 人设画像
5. 最后出聊天素材库 / 公众号素材

---

# podcast-chat-prep: batch-absorb an entire podcast

Turn dozens or hundreds of episode transcripts from one podcast into a "chat-ready" material pack — even if you've never listened. Per-episode notes get you up to speed; guest stance tracking and persona profiles give you depth. Know when a guest changed their mind — that's the information edge.

Friend recommended a podcast and you have no time to listen? Want to join a conversation without pretending? This tool distills transcripts into quotes, stories, talking points, and inside jokes you can reference naturally.

## Who it's for

- Heavy podcast listeners who want to hold their own in conversations
- Research-oriented listeners studying one podcast (guests, stances, themes)
- Live-streamers who want to turn audio content into WeChat-pub material

## Quick start

```bash
# 1. Transcribe audio with any tool
#    Tingwu (free) / Feishu Minutes / Jianying subtitle export

# 2. Feed the transcript to an AI and follow the SKILL.md workflow
```

Zero dependencies — clone and go. You only need transcript markdown, no environment setup.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full workflow: batch analysis → stance tracking → persona profile → material library |
| `assets/episode-template.md` | Per-episode note template (7 modules) |
| `assets/summary-template.md` | Cross-episode summary template (stance evolution timeline + persona profile) |
| `assets/chat-material-template.md` | Chat material library template (talking points + inside jokes) |

## Core capabilities

- **Batch processing**: 3+ episodes of one podcast auto-triggers cross-episode tracking; handles dozens or hundreds
- **Per-episode notes**: 7 modules, verbatim quotes with speaker labels
- **Guest stance tracking**: cross-episode comparison of the same topics — maintained/upgraded/reversed/contradicted, output as an evolution timeline
- **Guest persona profile**: stories and speaking habits stitched across episodes, conclusions only after 2+ episodes
- **Chat material library**: talking points, multi-perspective collisions, inside jokes, N-minute cheat sheet
- **Content reuse**: extract WeChat-pub material for live-stream scenarios, organized by account persona

## Recommended workflow

1. Audio → Tingwu/Feishu Minutes/Jianying → timestamped transcript
2. Preprocess: label speakers, clean filler words
3. Batch per-episode notes (one per episode)
4. Cross-episode tracking: stance evolution timeline + persona profile
5. Output the chat material library / WeChat-pub material
