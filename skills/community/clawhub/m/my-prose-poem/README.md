<div align="center">

# 🎖️ 我的散文诗 (My-Prose-Poem)

> *"有些经历，让 AI 帮你落笔，生出一篇散文诗。"*

<!-- Badge Row 1: Core Info -->
[![ClawHub](https://img.shields.io/badge/ClawHub-My--Prose--Poem-E75C46?logo=clawhub)](https://clawhub.ai/JustZeroX/my-prose-poem)  [![GitHub](https://img.shields.io/badge/GitHub-JustZeroX-181717?logo=github)](https://github.com/JustZeroX/skill-My-Prose-Poem)  [![Version](https://img.shields.io/badge/Version-0.0.1-orange)](https://github.com/JustZeroX/skill-My-Prose-Poem)


<!-- Badge Row 2: Tech Stack -->
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=3776AB)](https://www.python.org/)   [![Pillow](https://img.shields.io/badge/Pillow-10.0.0-brightgreen)](https://pypi.org/project/Pillow/10.0.0/)

<!-- Badge Row 3: Platforms -->
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://github.com/JustZeroX/skill-my-prose-poem)  [![Windows](https://img.shields.io/badge/Windows-0078D6?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGgzOXYzOUgweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik00OSAwaDM5djM5SDQ5eiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDQ5aDM5djM5SDB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQ5IDQ5aDM5djM5SDQ5eiIvPjwvc3ZnPg==)](https://github.com/JustZeroX/skill-my-prose-poem)   [![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://github.com/JustZeroX/skill-my-prose-poem)

<!-- Badge Row 4: License -->
[![License](https://img.shields.io/badge/License-MIT-BD2D2D)](LICENSE)
<br>

旅行回来，脑子里全是画面和情绪，写出来却像旅游打卡。<br>
深夜有感，想发一条长长的朋友圈，写了两句就删了。<br>
翻出旧照片，那个瞬间明明很重要，却怎么也说不清楚。<br>
<br>
**不是不会写作，是感慨太多，反而不知道从哪里开始。**<br>
**这个 Skill 不替你写——它帮你挖掘出隐藏在生活中的情感和故事。**

</div>

---

## ✨ 功能特点

- **🎤 只问不写** — 先通过多轮提问补完素材（经历层 → 感受层 → 感悟层），再动笔
- **📸 照片收集模式** — 多张照片统一收集，按拍摄时间排序后编写故事，不一张一写
- **🚫 不虚构** — 7 条硬约束，禁止补人物关系、补对话、补因果、补情绪放大
- **✂️ 克制叙述** — 拒绝"文绉绉"，拒绝公众号感，像和安静的朋友聊天
- **📏 信息密度分级** — 根据用户提供的素材量，自动选择写作密度（丰富/中等/较少/极少）
- **🌙 清醒的温柔结尾** — 不鸡汤，不讲大道理，让读者自己感受

---

## 🚀 快速开始

### 步骤 1：安装

#### 方式 1：Via ClawHub（推荐 ⭐）

```bash
# 1. 安装 ClawHub（如未安装）
npm install -g clawhub

# 2. 安装 my-prose-poem
clawhub install my-prose-poem
```

#### 方式 2：Via GitHub

```bash
git clone https://github.com/JustZeroX/skill-my-prose-poem.git ~/.openclaw/skills/my-prose-poem
```

### 步骤 2：安装依赖（可选）

```bash
pip install -r requirements.txt
```

> `pillow` 用于读取照片 EXIF，不是必须。缺少时会自动提示用户补问时间地点，不中断流程。

### 步骤 3：使用

在支持 OpenClaw Skill 的 Claude 对话中，直接触发：

```
写日记
帮我记录今天
整理一下最近的感受
根据这张照片写段文字
旅行回忆
生活片段
内心独白
```

只要提到这些关键词，Skill 会自动激活，引导你完成写作。

---

## 📖 使用示例

### 示例 1：旅行回忆

> **用户输入**：上周去了趟大理，古城那边坐了一下午，什么都没想，就看着云发呆。

```markdown
古城在下午四点有一种特别的光。那种光落在苍山上，把云的边缘染成灰白色。

温度不热，风里有青草和不知道哪儿飘来的桂花味。

我坐在一家门口的矮凳子上，看着那片云发呆。

很久没有这种感觉了。不是发呆，是真的静下来。

像一片被风吹落的叶子，终于掉进了水里，不是沉下去，是漂着，随波，但不起伏。

后来想想，可能很多人都是这样吧。只是大家都演得很好，没人提。
```

### 示例 2：日常感受

> **用户输入**：下雨天，坐在咖啡馆里，看着窗外人跑过去，角落有个人一直没回来。

```markdown
雨下了一整天，没有要停的意思。

我坐在窗边，拿铁已经凉了。雨顺着玻璃往下流，弯弯曲曲的。

角落那张桌子一直空着，旁边椅背上搭着一件外套，桌上那杯美式早凉了，杯壁上全是水珠。

我走的时候路过那张桌子，外套还搭在椅背上，美式还是那个样子。

希望下次来的时候，他出去能回来。
```

### 示例 3：情绪整理

> **用户输入**：每天挤地铁回家，车厢里所有人都在低头看手机，没人说话。到家已经累得什么都不想做。

```markdown
大城市的生活节奏太快了，每天都像机器一样运转。

早上挤地铁的时候，车厢里所有人都在低头看手机，没人说话，没人抬头。那一刻我觉得自己就是车厢的一部分，和旁边那些人没什么区别。

到家已经累得什么都不想做。以前觉得这样很正常，大家都这样。后来想想，不是的，这种"正常"根本就有问题。

现在也还没想清楚问题在哪，但我心里清楚的知道不该这么过。

让我紧绷的是：先这样过着吧。
```

---

## 🧩 核心概念

### 多轮提问机制

AI 会分三层补完素材：

| 层次 | 内容 | 补问次数 |
|------|------|---------|
| **经历层** | 时间、地点、基本事件 | 最多 1 次 |
| **感受层** | 当时的心理状态 | 最多 1 次 |
| **感悟层** | 对事件的深度思考 | 可选，不强制 |

每轮只问一个问题。回答简短就收束，不反复追问。

### 不虚构边界（7 条硬约束）

1. ❌ 不补人物关系（除非用户明确说"老友"、"爱人"）
2. ❌ 不补对话（严禁虚构任何直接或间接引语）
3. ❌ 不补因果（不推断用户为何去某地）
4. ❌ 不放大情绪（不把"有点难过"升级为"彻骨孤独"）
5. ❌ 不根据画面补剧情（有人物 ≠ 有故事）
6. ❌ 不基于照片推断情感（深夜 ≠ 忧郁）
7. ❌ 不凭空补充感官细节（未提及身体感受时不写）

### 写作密度等级

| 等级 | 触发条件 | 目标字数 |
|------|---------|---------|
| 丰富 | 三层信息完整 | 300~600 字 |
| 中等 | 经历+感受完整 | 200~350 字 |
| 较少 | 仅有经历层 | 150~250 字 |
| 极少 | 只有几句话 | 100~150 字 |

---

## 📖 项目背景

**为什么做这个？**

有很多人都有这样的时刻：

- 旅行回来，脑子里装满了感受，但落在纸上只剩流水账
- 深夜有感，想发一条长长的朋友圈，但不知道怎么组织成完整的段落
- 翻出旧照片，回忆涌上来，却怎么也说不清楚那个瞬间到底好在哪里

这种感觉不是"不会写作"，而是**感慨太多，反而不知道从哪里开始**。

这个 Skill 就是为了解决这个问题而生的：不是替你写，而是帮你挖。通过提问，把散落在感受里的东西一点一点带出来，最后用克制的、诚实的文字呈现出来。

---

## ⚙️ 配置与依赖

| 依赖 | 必需 | 说明 |
|------|------|------|
| `pillow` | 可选 | 读取照片 EXIF，缺少时自动走降级流程 |

```bash
pip install -r requirements.txt
```

**EXIF 说明：**
- 仅读取 `DateTime`、`GPSInfo`、`Model` 作为背景辅助
- 不推断感受或故事
- 不做联网地理编码

---

## 🙏 致谢

- **TRAE** — 整个 Skill 的开发和迭代过程中提供的支持与陪伴

---

## 📝 License

MIT License

---

> 💡 **Badge 说明**：以上 Badge 为自动生成，如与实际不符可手动删除或修改。

---

# 🎖️ My Prose Poem

**A literary-minded listener and recorder.**

It doesn't write stories for you. Instead, through restrained questioning, it helps you excavate those vague feelings and fleeting moments scattered through daily life — and turn them into words.

---

## ✨ Features

- **🎤 Ask First, Write Later** — Multi-round questions to complete the material (experience → feeling → insight), then write
- **📸 Photo Assistance** — Optional EXIF extraction from photos to anchor time and place
- **🚫 No Fabrication** — 7 hard constraints: no invented relationships, dialogue, causality, or emotional amplification
- **✂️ Restrained Narration** — Rejects "bookish" language and social-media platitudes; feels like chatting with a quiet friend
- **📏 Adaptive Density** — Auto-selects writing density (rich/medium/minimal/extreme) based on material provided
- **🌙 Sober Warmth in Endings** — No鸡汤 (motivational quotes), no grand lessons — lets readers feel it themselves

---

## 🚀 Quick Start

### Install Dependencies (Optional)

```bash
pip install -r requirements.txt
```

> `pillow` enables EXIF reading and is optional. If missing, the Skill gracefully falls back to asking the user for time/place instead.

### Trigger

When OpenClaw detects relevant keywords, the Skill activates automatically:

```
写日记 (write a diary)
帮我记录今天 (help me record today)
整理一下最近的感受 (sort through recent feelings)
根据这张照片写段文字 (write something based on this photo)
旅行回忆 (travel memories)
生活片段 (life fragments)
内心独白 (inner monologue)
```

---

## 📖 Examples

### Example 1: Travel Memory

> **User**: Spent last afternoon in Dali's old town, sitting and watching clouds. Didn't think about anything.

```markdown
古城在下午四点有一种特别的光。那种光落在苍山上，把云的边缘染成灰白色。

温度不热，风里有青草和不知道哪儿飘来的桂花味。

我坐在一家门口的矮凳子上，看着那片云发呆。

很久没有这种感觉了。不是发呆，是真的静下来。

像一片被风吹落的叶子，终于掉进了水里，不是沉下去，是漂着，随波，但不起伏。

后来想想，可能很多人都是这样吧。只是大家都演得很好，没人提。
```

### Example 2: Daily Scene

> **User**: Rainy day at a café, watching someone run past the window. Someone at the corner table never came back.

```markdown
雨下了一整天，没有要停的意思。

我坐在窗边，拿铁已经凉了。雨顺着玻璃往下流，弯弯曲曲的。

角落那张桌子一直空着，旁边椅背上搭着一件外套，桌上那杯美式早凉了。

我走的时候路过那张桌子，外套还搭在椅背上，美式还是那个样子。

希望下次来的时候，他出去能回来。
```

### Example 3: Emotional Reflection

> **User**: Commuting home by subway every day. Everyone stares at their phones. Too tired to do anything by the time I get home.

```markdown
大城市的生活节奏太快了，每天都像机器一样运转。

早上挤地铁的时候，车厢里所有人都在低头看手机，没人说话，没人抬头。那一刻我觉得自己就是车厢的一部分，和旁边那些人没什么区别。

到家已经累得什么都不想做。以前觉得这样很正常，大家都这样。后来想想，不是的，这种"正常"根本就有问题。

现在也还没想清楚问题在哪，但我心里清楚的知道不该这么过。

让我紧绷的是：先这样过着吧。
```

---

## 🧩 Core Concepts

### Multi-Round Questioning

The AI completes material across three layers:

| Layer | Content | Follow-up Limit |
|-------|---------|---------------|
| **Experience** | Time, place, basic event | Max 1 question |
| **Feeling** | Psychological state | Max 1 question |
| **Insight** | Deeper reflection | Optional, not forced |

One question per round. Short answers are accepted — no relentless follow-ups.

### No-Fabrication Boundaries (7 Hard Constraints)

1. ❌ No invented relationships (unless user explicitly says "old friend", "partner")
2. ❌ No invented dialogue (no direct or indirect quotes)
3. ❌ No invented causality (don't infer why the user went somewhere)
4. ❌ No emotional amplification (don't escalate "a bit sad" into "devastating loneliness")
5. ❌ No story invented from visuals (people/objects in photos ≠ plot)
6. ❌ No emotions inferred from photos (late night ≠ melancholy)
7. ❌ No凭空 sensory details (don't describe physical sensations not mentioned by user)

### Writing Density Levels

| Level | Trigger | Target Length |
|-------|---------|--------------|
| Rich | All three layers complete | 300~600 chars |
| Medium | Experience + Feeling complete | 200~350 chars |
| Minimal | Only Experience | 150~250 chars |
| Extreme | Just a few sentences | 100~150 chars |

---

## 📖 Project Background

**Why does this exist?**

Many people have moments like these:

- Returning from a trip, head full of feelings, but what lands on paper is just a factual account
- Having a deep thought late at night, wanting to post something meaningful, but unable to organize it into a coherent paragraph
- Looking at old photos, memories flooding back, yet unable to articulate what made that moment special

This isn't about "not knowing how to write" — it's that **there's too much to say, so you don't know where to start**.

This Skill was built to solve exactly that: not writing for you, but excavating with you. Through questions, it surfaces what's buried in your feelings, then presents it in restrained, honest writing.

---

## ⚙️ Dependencies

| Dependency | Required | Note |
|------------|----------|------|
| `pillow` | Optional | Reads photo EXIF; missing triggers graceful fallback |

```bash
pip install -r requirements.txt
```

---

## 🙏 Acknowledgements

- **TRAE** — For the ongoing support and companionship throughout the development and iteration of this Skill

---

## 📝 License

MIT License
