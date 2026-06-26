---
name: huo15-comic-script
displayName: 火15 漫剧-剧本分镜
description: 主题一句话 → 分幕分镜剧本 JSON（国风/仙侠/宫斗/江湖）。输出 script.json 含 characters、scenes、dialogue、camera、mood。触发词：生成剧本、漫剧剧本、分镜脚本、漫剧script。
version: 0.1.0
aliases:
  - 漫剧剧本
  - 分镜剧本
---

# 火15 漫剧-剧本分镜 Skill

> 主题 → 结构化 script.json，后续所有 skill 以此为输入。

---

## 输入

```bash
python scripts/script_gen.py \
  --theme "少年剑仙三年归来" \
  --duration 240 \
  --style 三渲二国风 \
  --genre 仙侠 \
  --out output/demo/script.json
```

## 输出 script.json 结构

```json
{
  "title": "归剑录",
  "style": "三渲二国风",
  "genre": "仙侠",
  "duration_total": 240,
  "scene_duration": 5,
  "logline": "...",
  "characters": [
    {
      "id": "C1",
      "name": "顾青崖",
      "age": "18",
      "visual": "白衣剑仙，剑眉星目，发束玉冠，腰佩青玉剑",
      "personality": "沉稳内敛",
      "voice": "zh_male_qingnian"
    }
  ],
  "scenes": [
    {
      "id": "S01",
      "location": "青崖峰绝顶",
      "time": "黎明",
      "characters": ["C1"],
      "action": "少年立于云海之上，长剑出鞘",
      "dialogue": [{"char": "C1", "text": "三年归来，该了结旧怨了"}],
      "camera": "远景→中景推近",
      "duration": 5,
      "mood": "苍凉壮阔"
    }
  ]
}
```

## Agent 模式

Claude Agent 可**直接按 schema 写 script.json**，跳过 Python 脚本。脚本仅作为 fallback（Anthropic SDK 调用）和校验器。

## 国风提示词模板

脚本内嵌 `PROMPT_TEMPLATE`，对不同 `genre` 选用对应叙事节奏：
- 仙侠：起兴→伏笔→反转→决战
- 宫斗：暗流→试探→反击→结局
- 江湖：相遇→比武→情义→重逢
- 志怪：诡异→探查→真相→启示
