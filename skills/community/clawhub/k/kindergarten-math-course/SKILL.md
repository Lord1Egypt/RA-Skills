---
name: kindergarten-math-course
slug: kindergarten-math-course
displayName: 幼儿园识数与加减法体系课程
version: 1.3.1
summary: 面向 3-7 岁幼儿的识数与加减法体系课程，按 L1-L5 五级进阶，自动生成 A4 可打印练习页与答案页，并支持能力诊断与批改反馈。
description: 3-7 岁幼儿识数与加减法体系课程。按 L1 识数1-5、L2 识数6-10、L3 比大小与分解组成、L4 10以内加减、L5 20以内进退位五级体系，生成 A4 可打印数学练习页（含答案页），并支持能力诊断、练习批改与进阶建议。Use when 用户提到 幼儿园/幼儿/小班/中班/大班/幼小衔接/学前 的 数学、识数、认数字、数数、点数、比大小、分解组成、凑十法、加减法、口算、应用题、练习纸、练习题、给孩子出题、数学启蒙、数学练习；or asks for kindergarten math worksheets, counting, number recognition, addition/subtraction within 10 or 20. Also use when 需要判断孩子数学起点、规划学习路径、批改幼儿数学练习或给出家长指导话术。
tags:
  - 教育
  - 幼儿
  - 数学
  - 识数
  - 加减法
  - 幼小衔接
  - 练习题
  - kindergarten-math
license: MIT
homepage: https://skillhub.cn/skills/user_89a2cacc/kindergarten-math-course
agent_created: true
---

# 幼儿园识数与加减法体系课程

## Overview

面向 3-7 岁幼儿的数学启蒙交付能力：把"识数 → 数的顺序 → 比大小与分解组成 → 10 以内加减 → 20 以内进退位"组织成 L1-L5 五级可进阶体系，按等级与题型生成可直接打印的 A4 练习页，并在练习后完成批改、薄弱点定位与下一步建议。核心产出是**可打印练习页**，附带家长指导话术。

## 快速上手

```bash
# 某等级一份练习（附答案 JSON）
python scripts/generate_worksheet.py --level L2 --seed 7 --out math_L2.html --json math_L2.json

# 预填孩子姓名 + 得分栏
python scripts/generate_worksheet.py --level L4 --name 小明 --score --out math_L4.html

# 诊断卷（覆盖全部题型，用于定级）
python scripts/generate_worksheet.py --preset diagnostic --out diag.html --json diag.json
```

对 WorkBuddy 直接说更简单："给我孩子出一份 10 以内加减法练习" / "生成一份数学诊断卷"。

## 触发条件

| 类别 | 触发词 / 场景 |
|---|---|
| 对象词 | 幼儿、幼儿园、小班、中班、大班、学前、幼小衔接、3岁/4岁/5岁/6岁孩子、我家娃、孩子 |
| 内容词 | 识数、认数字、数数、点数、数一数、数的顺序、相邻数、比大小、分解组成、分与合、凑十、破十、加减法、加法、减法、口算、进位加、退位减、应用题、数学启蒙、数学练习 |
| 交付词 | 练习题、练习纸、练习页、题卡、作业纸、打印、出几道题、给孩子做 |
| 流程词 | 数学诊断、测一下水平、从哪开始、学完下一步、批改、错了几题、怎么教 |
| 英文 | kindergarten math, counting worksheet, number recognition, addition within 10, subtraction within 20 |

**不触发**：小学一年级以上的教材同步辅导、奥数、乘除法、分数、方程、成人数学。遇到这些直接说明超出本 Skill 范围。

判定原则：只要同时出现"幼儿阶段对象"与"数/运算/练习"意图，即触发本 Skill，无需用户说出"Skill"或课程名。

## 执行逻辑

### Step 0 · 采集信息（最多问一次，缺失即用默认值）

需要的三项信息：**年龄/年级、当前水平（是否已知）、本次要练什么**。

- 用户已给出其中任意一项 → 直接推导其余，不再追问。
- 三项全缺 → 走诊断路径（Step 1 的诊断卷），在回复中说明"先做 10 题定位起点"。
- 确实需要选择时（例如无法确定大班还是中班），用 AskUserQuestion 一次性问完，不要多轮追问。

默认假设（不询问时直接采用，并在回复中注明）：未知水平 → L1 诊断；未指定题量 → L1/L2 用 10 题、L3 用 12 题、L4/L5 用 20 题；未指定列数 → 2 列（L1/L2 用 1 列）。

### Step 1 · 定级

等级对照：L1 小班 3-4 岁识数 1-5；L2 中班 4-5 岁识数 6-10；L3 中班下比大小与分解组成；L4 大班上 10 以内加减；L5 大班下/幼小衔接 20 以内进退位。完整知识点与晋级标准见 `references/curriculum.md`。

- 已知年龄但未测水平 → 生成对应等级的练习。
- 起点未知 → 生成诊断卷：`--preset diagnostic`（10 题，每题标注等级）。家长回传结果后，按"某等级 2 题全对即视为掌握，从最低未掌握等级开始"定位。

### Step 2 · 组卷

调用脚本（绝对路径 `C:\Users\李玉明\.workbuddy\skills\kindergarten-math-course\scripts\generate_worksheet.py`，Windows 下 Python 不可用时改用 `C:\Users\李玉明\.workbuddy\binaries\python\versions\3.13.12\python.exe`）：

```
python "<skill>/scripts/generate_worksheet.py" --level L4 --count 20 --seed 7 \
  --out "<工作区>/幼儿园数学_L4.html" --json "<工作区>/幼儿园数学_L4_答案.json"
```

- 补薄弱点 → 用 `--topics` 指定单一题型，题量减半
- 口头作答 → 加 `--no-answers`
- 复现同一套题 → 使用相同 `--seed`
- 页眉预填孩子姓名 → 加 `--name 小明`
- 大班高密度排版 → 加 `--columns 3`
- 参数与配方见 `references/worksheet-spec.md`

必须同时输出 `--json`，后续批改直接用它比对，不要凭记忆重算答案。

### Step 3 · 交付

1. 用 present_files 呈现生成的 HTML，并提示：浏览器打开后点「打印 / 另存为 PDF」，勾选「背景图形」（田字格虚线依赖背景）。
2. 在回复中给出**三条以内**的家长指导：本次题型与数量、建议用时（10-15 分钟）、一条具体操作提示（如"进位加先让孩子说 9 和几凑成 10"）。话术模板见 `references/pedagogy.md`。
3. 不写过程性描述、不写日期来源说明，直接给内容和指导。

### Step 4 · 批改与进阶

用户回传答案（文字、口述或照片）后：

1. 对照 JSON 判分，输出：共 X 题、做对 Y 题、正确率 Z%。
2. 按正确率决策（详见 `references/curriculum.md` 晋级标准）：≥90% 升下一级；60-89% 同级加练且错题题型占比提到 50%；<60% 降一级，实物操作后再抽象。
3. 同一题型错 ≥2 题 → 用错题重练直接生成针对性练习（读上次 JSON，按错题题型出同型新题，每个错题配 2 道新题）：

```
python "<skill>/scripts/generate_worksheet.py" \
  --review "<工作区>/幼儿园数学_L4_答案.json" --wrong 4,7,11 \
  --out "<工作区>/幼儿园数学_L4_错题重练.html" --json "<工作区>/幼儿园数学_L4_错题重练_答案.json"
```

未指定题号时也可用 `--topics` 手选题型，题量减半。
4. 每级至少完成 3 份练习才考虑晋级；连续两次 ≥90% 才允许跳级。
5. 给家长的反馈固定三段：结果 → 薄弱点 → 下一步（一个改进点，5-10 分钟的亲子小游戏）。禁止横向比较与否定性评价。

### Step 5 · 进度记录（可选）

用户多次使用或明确要求时，在工作区维护 `幼儿数学学习档案.md`，追加记录：日期、等级、题型、题量、正确率、错题库、下一步。模板见 `assets/progress-journal.md`。

## 硬规则

- 先理解后运算：L1-L4 一律不计速、不计时；只有 L5 后期才引入限时。
- 竖式仅在 L5（幼小衔接）引入，作为进位加/退位减的书写辅助，不追求算法熟练度，更不要求心算口算速度；L1-L4 一律不用竖式。
- 不在幼儿阶段引入乘法口诀、负数、超纲数值（L4 和不超过 10，L5 结果不超过 18）。
- 练习页必须含答案页（除非用户明确要求口头作答），方便家长当场核对。
- 一次只提一个改进点，先肯定具体行为再纠错。
- 每次只生成一份练习，避免一次性堆 50 题。

## 资源

- `references/curriculum.md` — L1-L5 知识点、题型映射、晋级与补练标准、诊断定位规则
- `references/pedagogy.md` — 教学原则、分题型讲解话术、常见错误纠正、家长反馈模板
- `references/worksheet-spec.md` — 脚本参数、版式规范、常用组卷配方
- `scripts/generate_worksheet.py` — 练习页生成器（A4 可打印 HTML + JSON 答案）
- `scripts/selftest.py` — 发版前自检（去重 / 答案合法性 / 等级覆盖 / 同卷无重复），改动脚本后必跑
- `scripts/generate_icon.py` — 生成平台图标（PNG 不进 Skill 包，需网页端上传）
- `assets/progress-journal.md` — 学习档案模板（Step 5 可选）

## 自检

安装后或修改脚本后必跑（详见 `scripts/selftest.py`，校验去重/答案合法性/等级覆盖/同卷无重复）：

```bash
python scripts/selftest.py
```

## Changelog

- **1.2.0**：新增 4 个题型（序数/第几、按数涂色、看图列式、竖式计算）补齐课程大纲承诺；`build_questions` 同卷去重，避免撞题；新增 `selftest.py` 发版自检（题目唯一率按空间分级、答案合法性正则校验、等级覆盖、同卷无重复）；新增 `generate_icon.py` 与 `assets/icon.png` 平台图标。
- **1.1.0**：新增错题重练（`--review`/`--wrong` 按错题题型生成同型新题）、页眉姓名预填（`--name`）、三列排版（`--columns 3`）、答案页标注每题题型；修正 homepage。
- **1.0.0**：首次发布，L1-L5 五级体系 + A4 可打印练习页生成器 + 能力诊断与批改反馈。

## License

本 Skill 以 MIT 协议发布，完整文本见下方：

```text
MIT License

Copyright (c) 2026 kindergarten-thinking-course authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
