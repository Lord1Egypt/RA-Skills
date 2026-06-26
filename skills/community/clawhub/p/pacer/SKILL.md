---
name: pacer
version: 0.1.2
description: >
  Your AI career companion. Scan your situation, map possible paths, simulate
  futures, and track progress week by week — with interactive charts.
author: hectormeta
tags: [career, planning, productivity, opc, startup, life-design]
license: MIT
requires:
  - memory: true        # 需要持久记忆功能
  - heartbeat: weekly   # 每周主动触发一次
---

# Pacer 🏃

**Your AI Career Companion | 你的AI职业陪跑伴侣**

> 不告诉你该做什么，陪你想清楚自己要什么。

---

## 它能做什么

**四个阶段，每步都有可视化图表：**

- 📄 **扫描现状** — 上传CV（PDF/Word/TXT）或文字描述，自动解析生成现状快照卡，6个维度全覆盖
- 🗺️ **规划路径** — 有目标就深度规划单一路径（技能雷达图+阶段甘特图），没目标就生成多方向对比（4维度横向评分）
- 🔮 **模拟未来** — 双轨时间轴可视化，看清选择新路径 vs 维持现状在6-12个月后的两种轨迹
- 📍 **追踪进度** — 里程碑甘特图+进度环形图+每日打卡热力图，每周 Heartbeat 自动更新

---

## 快速安装

```bash
npx clawhub@latest install pacer
```

或全局安装后运行（推荐，避免限速）：
```bash
npm install -g clawhub && clawhub login && clawhub install pacer
```

或直接告诉你的 OpenClaw 智能体：
```
Install this skill: https://github.com/hectormeta/pacer-skill
```

---

## 开始使用

安装后，发送以下任意一条消息：

- "帮我用Pacer规划一下我的下一步"
- "我现在很迷茫，不知道该做什么"
- 直接上传你的CV文件

**触发词：** 职业规划、career、我该怎么办、下一步、创业方向、迷茫、不知道做什么、规划、pacer

---

## 示范对话节选

```
用户：我想创业，但不知道该做什么。

Pacer：好，先帮你摸清底牌。你现在最擅长的3件事是什么？

[5个问题后生成快照卡]

Pacer：基于你的情况，有 3 条路可以走。先看整体对比图，
再告诉我哪个方向你想深入了解。

[输出多方向对比图表]

方向A — 内容咨询顾问：你有运营背景和数据能力，溢价空间更大。
         第一步：本周联系1个电商朋友，问他们内容上最头疼的问题。
```

更多完整对话见 `examples/` 目录。

---

## 适合这些人

- 想创业但不知道从哪开始
- 职场人考虑转型、晋升或跨行
- 应届生规划第一份工作
- OPC / 一人公司创业者
