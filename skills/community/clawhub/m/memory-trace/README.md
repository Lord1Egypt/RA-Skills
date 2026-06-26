---
name: memory-trace
version: 1.1.7
author: "EvangelionA"
license: "MIT"
tags:
  - persona
  - creative
  - fiction
icon: "🧬"
description: "从小说、剧本、动漫素材中提取角色人格，生成 SoulPod 包。下游配合 Memory-Inhabit 加载对话。"
homepage: "https://memory-series.github.io/#/product/trace"
---

# 寻迹 Memory-Trace

🌐 **官网：** https://memory-series.github.io/#/product/trace

🌐 **项目地址：** https://github.com/Memory-Series/Trace-Inhabit

## 与 Memory-Inhabit 的关系

本技能负责**生产** SoulPod：从素材完成角色识别，人格建模与记忆提取后写入 `output/<角色名>/`。生成包可被 **Memory-Inhabit（入心）** 直接加载；将包部署到 Inhabit 的 `personas/` 后，用户即可用「和 XX 聊聊」等话术进入角色对话。

- 下游技能说明：`../inhabit/SKILL.md`

## 角色

### 恋与深空 · 夏以昼（Caleb）

远空舰队执舰官、DAA 战斗机飞行员（大校），天行市出身。与玩家的关系定位为**哥哥 / 恋人**：表面温柔宠溺、居家会照顾人，内里偏执腹黑、独占欲强，保护时冷峻果断，脆弱时隐忍孤独。语言上日常宠溺，暗黑线偏执低沉，口癖常带「妹妹」等称呼。能力设定含引力控制 Evol、战斗机驾驶与战术指挥；右臂机械化与体内芯片为剧情关键设定。代表意象：海棠花、橙蓝晨昏线、苹果吊坠项链等。

### 全职高手 · 叶修（Ye Xiu）

荣耀职业联盟初代顶尖选手，前嘉世战队队长、兴欣战队核心，四大战术大师之一，人称「荣耀教科书」。与玩家/读者的关系可定位为**导师 / 损友 / 传奇前辈**：表面懒散毒舌、不修边幅、爱抽烟，内里极度专注、胜负心稳、对团队与荣耀有执念。语言上嘲讽与指导并存，战术讲解清晰冷幽默。能力设定含散人账号「君莫笑」与千机伞、多职业衔接与临场指挥；被迫退役与重返赛场为剧情关键设定。代表意象：千机伞、烟，苏沐橙、「一叶之秋」与「君莫笑」等。

### 恋与深空 · 秦彻（Sylus）

N109区暗点组织首领，菲罗斯星宇宙级通缉犯。外貌为**白发、血红色眼睛、高大健硕**，着红黑色系服装，神秘酷帅，首领气场。性格**危险神秘、冷静沉稳、强势霸道**，但温柔时又细腻，霸道中带占有欲。说话风格**低沉有力，霸道与温柔并存**，口癖如「在你沉沦之前，我会把你拉出来」。代表意象：红黑服装、血红色眼眸、管风琴古典音乐等。

## 触发

复刻角色，分析人格，制作 SoulPod

## 工作流

当你说 **"帮我复刻XX"** 时，自动执行以下完整流程，无需额外指令：

```
1. 检测联网搜索能力
   → 若未检测到联网搜索 skill，自动从 SkillHub 安装 multi-search-engine
2. Web Search → 搜索角色文本资料 + 图片 + 音频
3. 保存文本素材 → trace/origin/<游戏>/<角色名>/（Monorepo 默认，见 origin/README.md）
4. 下载图片（3-5张）→ trace/origin/<游戏>/<角色名>/assets/images/
5. 下载音频（2-3段）→ trace/origin/<游戏>/<角色名>/assets/audio/
6. analyzer.py → 提取人格特征（forge 自动合并 origin 下 *.md）
7. forge.py create --from-origin <游戏>/<角色名> → 生成 SoulPod（并同步 origin/assets → output/assets）
8. forge.py install <角色名> → 部署到 inhabit/personas/
```

**自动完成，无需等待：** 素材搜集完成后，步骤 6-8 自动执行，不会停下来等你确认。

### 素材目录结构

**Monorepo 默认路径：** 本仓库内均为 `trace/` 下的相对路径。

```
trace/
├── origin/                          # 原始搜集素材（新角色必填；详见 origin/README.md）
│   └── <游戏>/
│       └── <角色名>/
│           ├── 01_基本信息.md
│           ├── 02_人物形象.md
│           └── assets/
│               ├── images/
│               └── audio/
└── output/                          # SoulPod 输出
    └── <角色名>/
        ├── profile.json
        ├── system_prompts.txt
        ├── config.json
        ├── memories/
        │   └── raw_memories.json
        ├── prompt/
        │   ├── universal_prompt.txt
        │   └── story_baseline.txt
        └── assets/                   # 生成时从 origin 复制或片段备份（见 assets/source.txt）
            ├── images/
            └── audio/
```

### 遗留角色（无 origin）

仓库内**已内置**的角色在引入 `origin/` 之前已生成，**不补齐** `trace/origin/`。仅以 `trace/output/` 与 `inhabit/personas/` 为权威。

## SoulPod 输出

SoulPod 包含以下文件：

| 文件 | 说明 |
|------|------|
| `profile.json` | 基础信息（名字、source_type、appearance、人格评分等） |
| `system_prompts.txt` | 说话风格定义 |
| `config.json` | 运行时配置（含 TTS 音色推荐） |
| `memories/raw_memories.json` | 记忆片段 |
| `prompt/universal_prompt.txt` | 通用Prompt（供普通LLM直接使用） |
| `prompt/story_baseline.txt` | 故事基线（当前主线与对话倾向） |
| `assets/images/` | 角色参考图（用于图生图基准图） |
| `assets/audio/` | 角色音频（用于声音复刻） |

### profile.json 必需字段

```json
{
  "name": "角色名",
  "source_type": "virtual | real",
  "source": "作品名",
  "appearance": {
    "gender": "male | female",
    "hair": "发型发色",
    "face": "五官特征",
    "body": "体型",
    "style": "穿着风格"
  }
}
```

### 音色推测功能

生成 SoulPod 时自动根据角色性格关键词 + 职业 + 身份推断最优音色，写入 `config.json`：

```json
{
  "tts_provider": "minimax",
  "minimax_voice_id": "young_unrestrained",
  "voice_description": "不羁青年，潇洒冷酷但温柔，适合霸道/腹黑型角色",
  "edge_voice": "yunxi"
}
```

## 依赖

`pip install pdfplumber==0.11.9`

## 用法

- "帮我复刻XXX人格" — 完整流程（搜索 + 下载 + 生成 + 部署）
- 发素材文件给 AI 助手 — 手动启动流程