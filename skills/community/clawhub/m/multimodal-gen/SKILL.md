---
name: multimodal-gen
description: |
  多模态内容生成技能。覆盖文生图、图生图、文生视频、语音转写，统一封装提示词范式与调用约定，衔接系统内置的 ImageGen / VideoGen 工具。内置 prompt 构造助手脚本。适用于配图、海报、视频素材、语音笔记转写。
version: 1.0.0
author: WorkBuddy
agent_created: true
visibility: "public"
tags:
  - 文生图
  - 图生图
  - 文生视频
  - 语音转写
  - 多模态
---

# multimodal-gen — 多模态生成台

_把"我要一张图/一段视频"变成稳定可控的生成请求。_

## 能力映射
| 需求 | 工具 | 说明 |
|------|------|------|
| 文生图 | `ImageGen` | 文本→图像；注意单图消耗约 5–10 积分 |
| 图生图 | `ImageGen`（带 image 参数） | 基于参考图变换风格/元素 |
| 文生视频 | `VideoGen` | 文本→短视频（约 1–3 分钟，5s 约 50–100 积分） |
| 图生视频 | `VideoGen`（带 image） | 图片→动态视频 |
| 语音转写 | 本地 ffmpeg + whisper / 或外部 API | 音频→文本（标记 needs_web） |

## 提示词范式
- **文生图**：主体 + 环境 + 风格 + 镜头 + 画质词。例：「赛博朋克风格的城市夜景，霓虹反射在湿漉漉的街道，广角，电影感，8k」。
- **图生图**：明确"保留什么 / 改什么"。例：「保持构图，把白天改成黄昏，增加暖色调」。
- **文生视频**：分镜脚本式描述 + 时长 + 运镜。例：「镜头从远处推近一座雪山，云层流动，阳光洒下，5 秒」。
- **语音转写**：指明语言/方言，长音频先切片。

## 脚本：提示词构造助手
```bash
# 把简略需求扩写成结构化生成提示
python scripts/prompt_build.py "一张猫咪插画" --style 水彩 --aspect 1:1
```
输出可直接喂给 ImageGen/VideoGen 的优化提示词。

## 成本控制
- 生成前告知用户积分消耗（ImageGen ~5–10/图，VideoGen ~50–100/5s）。
- 视频先用短时长验证效果，再拉长。

## 自我进化学习系统
```bash
python scripts/learner.py record <技能目录> --capability 文生图 --note "用户偏好写实风而非卡通"
python scripts/learner.py record <技能目录> --capability 文生视频 --fail --error 时长超限 --note "超过10s被拒"
python scripts/learner.py insight <技能目录>
python scripts/learner.py reflect <技能目录>
```
记忆落盘 `learned_patterns.json`。

## 安全边界
- 不生成侵权、违法、色情、虚假人物肖像等内容。
- 商用素材确认版权与平台合规。
- 语音转写仅处理授权音频。
