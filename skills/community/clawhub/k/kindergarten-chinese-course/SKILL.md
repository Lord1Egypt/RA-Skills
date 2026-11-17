---
name: kindergarten-chinese-course
slug: kindergarten-chinese-course
displayName: 幼儿园识字与诗歌课程体系
version: 1.0.3
category: education
platforms: [WorkBuddy, claude-code, codex, deepseek-harness]
license: MIT
homepage: https://skillhub.cn/skills/user_89a2cacc/kindergarten-chinese-course
author: workbuddy-user-89a2cacc
agent_created: true
description: 3-7 岁幼儿识字与诗歌课程：L1 看图认字 → L2 描红 → L3 组词 → L4 古诗填空，生成 A4 可打印练习页（含答案页）。Use when 用户提到 识字、描红、笔顺、组词、古诗、儿歌、默写、幼小衔接练字；or asks for Chinese tracing worksheets, hanzi, poem with pinyin.
summary: 面向 3-7 岁幼儿的识字与诗歌启蒙体系，按 L1-L4 四级进阶，生成 A4 可打印练习页（看图认字、描红、组词、古诗带拼音、古诗填空），含答案页、评分栏与家长指导话术。
keywords:
  - 识字
  - 汉字
  - 描红
  - 笔顺
  - 古诗
  - 诗歌
  - 儿歌
  - 背诵
  - 组词
  - 幼儿
  - 幼小衔接
  - 可打印练习
  - printable worksheet
tags:
  - 教育
  - 幼儿
  - 语文
  - 识字
  - 古诗
  - 儿歌
  - 描红
  - 可打印
  - kindergarten-chinese
---

# 幼儿园识字与诗歌课程体系

## Overview

面向 3-7 岁幼儿的语文启蒙交付能力：把"看图认字 → 描红书写 → 组词运用 → 古诗诵读 → 古诗填空"组织成 L1-L4 四级可进阶体系，按等级与题型生成可直接打印的 A4 练习页，并附答案页与家长指导。核心产出是**可打印识字/诗歌练习页**。

与 `kindergarten-thinking-course`（逻辑思维）、`kindergarten-math-course`（数与运算）互补：本 Skill 聚焦**非数值的语文能力**（汉字认读书写、诗歌积累）。

## 触发条件

| 类别 | 触发词 |
|---|---|
| 对象 | 幼儿 / 幼儿园 / 小班 / 中班 / 大班 / 学前 / 幼小衔接 / 3-7岁孩子 / 我家娃 |
| 内容 | 识字 / 汉字 / 认字 / 描红 / 笔顺 / 古诗 / 诗歌 / 儿歌 / 背诵 / 组词 / 默写 |
| 交付 | 识字练习 / 出几道字 / 给孩子练字 / 打印古诗 / 学唐诗 |
| 流程 | 从哪开始 / 批改 / 错了怎么教 |
| EN | kindergarten chinese, character tracing, hanzi, poem, nursery rhyme, pinyin |

**不触发**：小学中高年级阅读理解、写作技巧、成人书法。判定原则：同时出现"幼儿阶段对象"与"汉字/诗歌"意图即触发。

## 执行逻辑

### Step 0 · 采集信息（最多问一次）
需要：**年龄/年级、本次练什么题型**。两项全缺 → 默认 L1 综合卷；已给任意一项 → 推导其余。

### Step 1 · 定级
L1 小班 3-4 岁（象形字认读+描红+儿歌）；L2 中班 4-5 岁（独体字+五言古诗）；L3 大班 5-6 岁（常用字+组词+七言古诗）；L4 幼小衔接 6-7 岁（生字+古诗填空默写）。完整映射见 `references/curriculum.md`。

### Step 2 · 组卷
```bash
python "<skill>/scripts/generate_worksheet.py" --level L2 --topics recognize,trace,poem \
  --seed 7 --score --out "<workspace>/识字_L2.html" --json "<workspace>/识字_L2.json"
```
**最常用开关**：`--level` 等级；`--topics` 指定题型（recognize/trace/poem/word/fill）；`--count` 汉字题量（仅诗歌时表诗歌数，上限 3）；`--seed` 复现；`--name`/`--no-name` 姓名；`--score` 评分栏；`--lang en` 英文；`--no-answers` 不输出答案页；`--regen <旧json>` 一键复现；`--list` 浏览题型×等级映射。

### Step 3 · 交付
1. 用 present_files 呈现 HTML；提示浏览器「打印 / 另存为 PDF」（已开启 `print-color-adjust:exact`，无需手动勾背景图形）。
2. 给**三条以内**家长指导：本次题型与数量、建议用时（L1/L2 约 10 分钟、L3/L4 约 15 分钟）、一条操作提示（如"先指图说名字再点字念"）。
3. 不写过程描述、不写日期/来源。

### Step 4 · 批改与进阶
- 识字/描红以"能认/能描"为达标，不机械判对错；古诗填空对照答案页批改。
- 正确率 ≥ 90% → 升一级；60-89% → 同级加练；< 60% → 降一级，先实物/指读再回纸面。
- 每级至少 3 份才晋级；连续两次 ≥ 90% 才跳级。
- 反馈固定三段：**结果 → 薄弱点 → 下一步**（一个改进点 + 5-10 分钟亲子小游戏）。禁止横向比较与否定性评价。

### Step 5 · 进度记录（可选）
多次使用或要求时，维护 `幼儿语文学习档案.md`（模板见 `assets/progress-journal.md`）。

## 硬规则
- L1-L3 不计速、不计时；L4 后期才引入限时默写挑战。
- 不在幼儿阶段要求默写超纲字、机械抄写；描红握笔姿势优先于写对。
- 练习页含答案页（除非 `--no-answers`），方便家长核对。
- 一次只提一个改进点，先肯定具体行为再纠错。
- 每次默认生成一份练习；诗歌单次 ≤ 3 首。

## 安全与隐私（skillhub TRACE-E 红线）
发布前由 `scripts/preflight.py` 自动核验，输出 `SHIP_REPORT.md`。

| 维度 | 含义 | 本 Skill 的保证 |
|---|---|---|
| **T**rusted · 零外网 | 不向外发起任何网络请求 | 仅用 Python 标准库；无 `requests/urllib/socket/http` 等 import 与调用 |
| **R**estricted · 零凭证 | 不读取任何密钥/隐私 | 不读 `~/.ssh` / `.env` / `AppData` / token / 浏览器缓存 / 系统目录 |
| **A**nti-inject · 零注入 | 不信任输入不直接进 HTML | 姓名等输入统一 `html.escape`；汉字/诗歌为内置可信数据 |
| **C**ontained · 最小权限 | 文件写入范围受限 | 仅写入 `--out` / `--json` 指定路径；答案与题目同文件（单 HTML） |
| **E**vidence · 可审计 | 结果可复现可核查 | 所有生成 `*.json` 写入 `seed`，`--regen` 字节级复现；答案内嵌便于核对 |

- 发布前自检：`python scripts/preflight.py`（应全部 PASS）
- 回归测试：`python scripts/test_skill.py`（生成/复现/单文件答案/红线/英文/校验）

## 文件清单
```
SKILL.md                 ← 本文件
README.md                ← 上手 + 命令清单
CHANGELOG.md             ← 迭代日志
LICENSE                  ← MIT
SHIP_REPORT.md           ← preflight 自检输出（发布前生成）
references/
  curriculum.md          ← L1-L4 知识点、题型映射、晋级标准
  activity-spec.md       ← 完整 CLI 参数表 / 配方 / 版式规范
  pedagogy.md            ← 家长话术 / 反馈模板
assets/progress-journal.md ← 学习档案模板
scripts/
  generate_worksheet.py  ← CLI 主入口（单文件 HTML，答案内嵌）
  preflight.py           ← TRACE-E 红线自检，输出 SHIP_REPORT.md
  test_skill.py          ← 回归测试（19 项级别）
```

## 自检
发布前请人工验证（应全部通过）：
```bash
python scripts/generate_worksheet.py --list
python scripts/generate_worksheet.py --level L2 --topics recognize,trace,poem --seed 7 \
  --out /tmp/t.html --json /tmp/t.json
python scripts/generate_worksheet.py --regen /tmp/t.json --out /tmp/r.html --json /tmp/r.json
# diff /tmp/t.html /tmp/r.html 应一致
```
