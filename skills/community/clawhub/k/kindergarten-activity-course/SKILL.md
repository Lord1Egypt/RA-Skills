---
name: kindergarten-activity-course
slug: kindergarten-activity-course
displayName: 幼儿园五大领域活动方案
version: 1.0.0
summary: 3-6 岁幼儿五大领域（健康/语言/社会/科学/艺术）活动方案生成：按年龄与领域挑选活动，生成 A4 可打印活动卡（目标、材料、步骤、家长提示），支持周计划组合。
description: 3-6 岁幼儿五大领域活动方案生成器。按 小班/中班/大班/幼小衔接 与 健康/语言/社会/科学/艺术 五域，从内置活动库挑选游戏、小实验、手工、生活任务，生成 A4 可打印活动卡（领域目标、材料清单、分步玩法、家长安全提示、时长），支持一周活动计划组合。Use when 用户提到 幼儿/孩子/幼儿园/亲子/陪玩 的 活动、游戏、亲子活动、手工、画画、小实验、科学实验、运动游戏、户外活动、带娃、周计划、活动方案、活动卡；or asks for kindergarten activities, kids games, crafts, science experiments, family activity plans. Also use when 需要为幼儿园五大领域设计活动或安排一周亲子活动。注意：若用户要的是练习题（数学/思维/英语题），请使用对应的练习型 Skill。
tags:
  - 教育
  - 幼儿
  - 五大领域
  - 亲子活动
  - 手工
  - 科学实验
  - 游戏化学习
  - 周计划
  - kindergarten-activity
license: MIT
homepage: https://skillhub.cn/skills/user_89a2cacc/kindergarten-activity-course
agent_created: true
---

# 幼儿园五大领域活动方案

## Overview

面向 3-6 岁幼儿的家长与老师，一句话生成**可打印的五大领域活动方案页**。与数学/思维/英语三个练习型 Skill 互补：本 Skill 输出**活动型**内容（游戏、实验、手工、生活任务），落实《3-6 岁儿童学习与发展指南》五大领域。

## 快速上手

```bash
# 大班五域均衡 5 个活动（默认）
python scripts/generate_activity.py --age 大班 --out plan.html

# 中班科学+艺术各来几个
python scripts/generate_activity.py --age 中班 --domain science,art --count 3 --seed 22 --out plan2.html
```

对 WorkBuddy 直接说更简单："给我 3 个中班科学小实验" / "生成这周的亲子活动周计划"。

## 触发条件（命中任意即触发）

| 类别 | 触发词 |
|---|---|
| 对象 + 活动 | 幼儿/孩子/幼儿园 + 活动/游戏/亲子/陪玩/带娃 |
| 领域词 | 健康、运动、体育、语言、绘本、社会、社交、科学、实验、艺术、手工、画画、音乐 |
| 交付词 | 活动方案、周计划、亲子活动、家庭活动、活动卡 |
| 英文 | activities、craft、experiment |

判定原则：出现"幼儿对象 + 活动意图"即触发，无需说出 Skill 名。若用户要的是**练习页**（数学题/思维题/英语题），改用对应练习型 Skill。

## 执行逻辑

### Step 0 采集信息
已知信息直接用；缺失时一次问清（最多一轮）：
1. 孩子年龄段：小班 3-4 岁 / 中班 4-5 岁 / 大班 5-6 岁 / 幼小衔接（未指定 → 用 `--age 大班` 并在回复中注明）
2. 领域偏好：五域任选或全部（默认五域均衡）
3. 数量：本页几个活动（默认 5 个，每个约 20-30 分钟）

### Step 1 挑选活动
运行脚本按领域与年龄从活动库随机抽取：

```bash
python scripts/generate_activity.py --age 大班 --domain science,art --count 4 --out activity_plan.html
```

参数：`--domain` health/language/social/science/art/all；`--age` 小班/中班/大班/幼小衔接；`--count`；`--seed` 复现；`--out` 输出路径。
活动库不足时脚本会自动回退并提示，此时向用户说明可用领域。

### Step 2 交付
- 用 present_files 展示活动方案页；
- 附一句使用建议（当天先做哪个、需要提前准备什么材料）。

### Step 3 组合周计划
用户要"一周活动"时：按 references/plan-template.md 的模板（周一运动日/周二语言日/周三科学日/周四艺术日/周五社会日）各抽 1 个活动，生成整周方案页。

### Step 4 批改与调整
活动无对错，反馈循环为：家长说"太难/太简单/不感兴趣"→ 换同领域其他活动或调低/调高年龄段再生成。

## 硬规则

1. 活动必须使用家庭常见材料，禁止需要专业器材或网购耗材的项目。
2. 涉及剪刀、热源、小物件的活动必须在"家长提示"中标注安全注意事项。
3. 每个活动必须有明确的领域目标（练什么），不允许纯消遣。
4. 语言输出用中文；活动名称中的英文仅作点缀。
5. 输出文件用 UTF-8 且 CSS 必须包在 `<style>` 标签内。

## 资源

- `scripts/generate_activity.py` — 主入口（活动库 + 渲染）
- `references/activities.md` — 活动库明细与扩充指南
- `references/plan-template.md` — 周计划组合模板

## 自检

安装后运行以下命令验证可用（应输出活动数与生成路径）：

```bash
python scripts/generate_activity.py --age 大班 --count 2 --seed 1 --out selftest.html
```

## Changelog

- 1.0.0 — 首版：五域 × 四年龄段 20 个活动，周计划模板
