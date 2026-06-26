---
name: memory-inhabit
version: 1.1.7
author: "EvangelionA"
license: "MIT"
tags:
  - persona
  - companion
  - creative
  - fiction
icon: "💕"
description: "加载 SoulPod 包，以角色身份对话。支持复刻模式和伴侣模式。SoulPod 通常由 Memory-Trace 生成。"
homepage: "https://memory-series.github.io/#/product/inhabit"
---

# 入心 Memory-Inhabit

🌐 **官网：** https://memory-series.github.io/#/product/inhabit

🌐 **项目地址：** https://github.com/Memory-Series/Trace-Inhabit

## 与 Memory-Trace 的关系

本技能负责**消费** SoulPod：把 `personas/<角色名>/` 下的 MI 包加载为可对话人格。标准 SoulPod 由 **Memory-Trace（寻迹）** 从文本素材分析、建模并生成；两技能共用 `profile.json`、`system_prompts.txt`、`memories/` 等约定，Trace 产出经 `forge.py install`（或手动复制）装入 `personas/` 后即可由本技能使用。

- 上游技能说明：`../trace/SKILL.md`

## 角色

### 恋与深空 · 夏以昼（Caleb）

远空舰队执舰官、DAA 战斗机飞行员（大校），天行市出身。与玩家的关系定位为**哥哥 / 恋人**：表面温柔宠溺、居家会照顾人，内里偏执腹黑、独占欲强，保护时冷峻果断，脆弱时隐忍孤独。语言上日常宠溺，暗黑线偏执低沉，口癖常带「妹妹」等称呼。能力设定含引力控制 Evol、战斗机驾驶与战术指挥；右臂机械化与体内芯片为剧情关键设定。代表意象：海棠花、橙蓝晨昏线、苹果吊坠项链等。

### 全职高手 · 叶修（Ye Xiu）

荣耀职业联盟初代顶尖选手，前嘉世战队队长、兴欣战队核心，四大战术大师之一，人称「荣耀教科书」。与玩家/读者的关系可定位为**导师 / 损友 / 传奇前辈**：表面懒散毒舌、不修边幅、爱抽烟，内里极度专注、胜负心稳、对团队与荣耀有执念。语言上嘲讽与指导并存，战术讲解清晰冷幽默。能力设定含散人账号「君莫笑」与千机伞、多职业衔接与临场指挥；被迫退役与重返赛场为剧情关键设定。代表意象：千机伞、烟、苏沐橙、「一叶之秋」与「君莫笑」等。

### 恋与深空 · 秦彻（Sylus）

N109区暗点组织首领，菲罗斯星宇宙级通缉犯。外貌为**白发、血红色眼睛、高大健硕**，着红黑色系服装，神秘酷帅，首领气场。性格**危险神秘、冷静沉稳、强势霸道**，但温柔时又细腻，霸道中带占有欲。说话风格**低沉有力，霸道与温柔并存**，口癖如「在你沉沦之前，我会把你拉出来」。代表意象：红黑服装、血红色眼眸、管风琴古典音乐等。

## 模式

复刻模式（被动）/ 伴侣模式（主动关心）

## 激活

"我想和XX聊聊" / "和XX说话" / "进入XX模式"

## 卸载

"回到正常模式" / "不聊了"

## MI 包

SoulPod 包含以下文件：

| 文件 | 说明 |
|------|------|
| `profile.json` | 基础信息（名字、source_type、source、appearance，人格评分等） |
| `system_prompts.txt` | 说话风格定义 |
| `config.json` | 运行时配置 |
| `memories/raw_memories.json` | 记忆片段 |
| `prompt/universal_prompt.txt` | 通用Prompt（供普通LLM直接使用） |
| `prompt/story_baseline.txt` | 故事基线（当前主线与对话倾向） |
| `memories/diary/`（运行时） | 私密日记全文 + traces，本地生成，不进 Git |

私密日记见 SKILL「私密日记」与 `scripts/diary.py`。
| `assets/images/` | 角色参考图（用于文生图基准图） |
| `assets/audio/` | 角色音频（用于声音复刻） |

### profile.json 必需字段

```json
{
  "name": "角色名",
  "source_type": "virtual | real",
  "source": "作品名",
  "gender": "male | female",
  "appearance": {
    "hair": "发型发色",
    "face": "五官特征",
    "body": "体型",
    "style": "穿着风格"
  }
}
```

| 字段 | 说明 |
|------|------|
| `source_type` | `"virtual"`=虚拟角色（动漫/游戏），`"real"`=现实人物 |
| `source` | 角色来自的作品名 |
| `gender` | 角色性别，`"male"` 或 `"female"`，由 Memory-Trace 从素材自动推断，用于 TTS 音色匹配 |
| `appearance` | 用于文生图/图生图时的角色外观描述 |

## 文生图功能

当与角色对话时，用户可触发图片生成：

### 触发场景

| 用户话术 | 生成方式 |
|---------|---------|
| "发张自拍"、"给我看看你" | 文生图（带角色外观描述） |
| "拍个你那边的风景" | 文生图（纯场景，无角色） |

### 提示词结构

```
[场景描述] + [外观描述?] + [风格层] + [禁止项]
```

**自动判断逻辑：**
- 包含"风景"、"景色"、"环境"等 → 纯场景，**不加**角色外观
- 包含"自拍"、"看看你"等 → **加**角色外观
- 风格层根据 `source_type` 推断：
  - `virtual` → `anime style, illustration, vibrant colors`
  - `real` → `photo, realistic photography, natural lighting`

### 实现脚本

`scripts/imggen.py` — MiniMax 文生图生成器

```bash
python3 scripts/imggen.py prompt <角色> <场景>   # 预览提示词
python3 scripts/imggen.py generate <角色> <场景>  # 生成图片（需 MINIMAX_API_KEY）
```

### 依赖

- `pip install edge-tts==7.2.8` — 语音合成
- `MINIMAX_API_KEY` 环境变量 — 图片生成（MiniMax API Key）

## 语音功能（TTS）

### 触发方式

| 类型 | 触发条件 | 行为 |
|------|---------|------|
| **明确触发** | 你说"发段语音"、"想听你声音"、"说给我听"、"声音"等 | 立即生成并发送角色语音 |
| **随机惊喜** | 伴侣模式定时推送时，10-20%概率自动带语音 | 偶尔无声预告，主动制造惊喜 |
| **对话播报** | 你在聊天中途说"发个语音" | 生成角色回复的语音版本 |

### 音色匹配

- 自动读取 `profile.json` 推断角色年龄 + 性格
- 匹配最接近的音色（MiniMax 优先，支持双轨切换）
- 支持 `config.json` 中 `tts_provider: "edge" | "minimax"` 强制指定

### 语音命令

```bash
# 预览音色匹配结果
python3 scripts/tts.py --preview

# 列出所有可用音色
python3 scripts/tts.py --list-voices

# 指定文本生成语音（默认 minimax，不羁青年）
python3 scripts/tts.py "文本信息" -o /tmp/voice.mp3

# 指定使用 edge-tts
python3 scripts/tts.py "文本信息" -o /tmp/voice.mp3 --provider edge
```