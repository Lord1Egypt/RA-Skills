---
name: kindergarten-thinking-course
slug: kindergarten-thinking-course
displayName: 幼儿园思维课程体系
version: 1.2.1
category: education
platforms: [WorkBuddy, claude-code, codex, deepseek-harness]
license: MIT
homepage: https://skillhub.cn/skills/user_89a2cacc/kindergarten-thinking-course
author: workbuddy-user-89a2cacc
agent_created: true
description: 面向 3-7 岁幼儿的 L1-L4 思维启蒙体系，生成 A4 可打印训练页与答案。
summary: 面向 3-7 岁幼儿的思维启蒙与逻辑训练体系课程，按 L1-L4 四级进阶，生成 A4 可打印思维训练练习页，含能力诊断、批改进阶、花名册批量出卷、家长指导话术与上架自检。
keywords:
  - 思维启蒙
  - 逻辑训练
  - 幼儿园
  - 幼小衔接
  - 可打印练习
  - printable worksheet
  - thinking course
tags:
  - 教育
  - 幼儿
  - 思维
  - 逻辑
  - 益智
  - 幼小衔接
  - 练习题
  - 可打印
  - kindergarten-thinking
  - printable-worksheet
---

# 幼儿园思维课程体系

## Overview

面向 3-7 岁幼儿的思维启蒙交付能力：把"分类对应 → 排序规律 → 空间方位 → 图形几何 → 比较推理 → 观察专注"组织成 L1-L4 四级可进阶体系，按等级与题型生成可直接打印的 A4 思维训练页，并在练习后完成批改、薄弱点定位与下一步建议。核心产出是**可打印思维训练页**。

与 `kindergarten-math-course` 互补：本 Skill 聚焦**非数值的思维能力**（逻辑、空间、模式、观察），不替代数与运算训练。

## 快速上手

```bash
# 某等级一份练习（附答案 JSON）
python scripts/generate_worksheet.py --level L2 --seed 7 \
  --out think_L2.html --json think_L2.json

# 预填孩子姓名 + 得分栏 + 全部题型诊断
python scripts/generate_worksheet.py --level L1 --name 小明 --score \
  --out think_L1.html --json think_L1.json
python scripts/generate_worksheet.py --preset diagnostic \
  --out diag.html --json diag.json
```

对 WorkBuddy 直接说更简单："给我孩子出一份找规律练习" / "生成一份思维诊断卷"。

## 触发条件

| 类别 | 触发词 |
|---|---|
| 对象 | 幼儿 / 幼儿园 / 小班 / 中班 / 大班 / 学前 / 幼小衔接 / 3-7岁孩子 / 我家娃 |
| 内容 | 思维 / 逻辑思维 / 找规律 / 分类 / 配对 / 排序 / 比长短轻重 / 方位 / 图形 / 迷宫 / 找不同 / 观察力 / 推理 / 等量代换 |
| 交付 | 练习题 / 练习页 / 题卡 / 打印 / 出几道题 / 给孩子做 / 益智题 / 脑力题 |
| 流程 | 思维诊断 / 测一下 / 从哪开始 / 批改 / 错了 / 怎么教 |
| EN | kindergarten thinking, logic worksheets, pattern, classification, spatial, maze, find the difference |

**不触发**：小学奥数、正式四则运算（加减乘除超纲部分）、成人逻辑/编程、学科同步辅导。
判定原则：只要同时出现"幼儿阶段对象"与"思维/逻辑/空间/规律/观察"意图即触发；无需用户说出"Skill"或课程名。

## 执行逻辑

### Step 0 · 采集信息（最多问一次）

需要的信息：**年龄/年级、当前水平（已知？）、本次练什么题型**。
- 已给任意一项 → 推导其余，不再追问
- 三项全缺 → 走诊断路径（Step 1）
- 一次性 AskUserQuestion，不要多轮追问

**默认假设**：未知水平 → L1 诊断；未指定题量 → L1/L2=6、L3=8、L4=10；未指定列数 → 2 列。

### Step 1 · 定级

L1 小班 3-4 岁基础分类对应；L2 中班 4-5 岁排序/规律/方位；L3 大班 5-6 岁模式推理/等量代换；L4 幼小衔接 6-7 岁综合逻辑。完整知识点与晋级标准见 `references/curriculum.md`。

- 已知年龄未测水平 → 生成对应等级练习
- 起点未知 → 用 `--preset diagnostic`（覆盖各主题 10+ 题，每题标注等级），家长回传后按"某等级 2 题全对即视为掌握"定位

### Step 2 · 组卷

```bash
python "<skill>/scripts/generate_worksheet.py" --level L2 --count 8 --seed 7 \
  --out "<workspace>/幼儿思维_L2.html" --json "<workspace>/幼儿思维_L2.json"
```

**最常用开关**：

| 想要 | 加这个开关 |
|---|---|
| 指定题型 | `--topics pattern,shape,position`（拼错会列出合法值；超出本等级的会被剔除） |
| 补薄弱点 | `--topics <单题型>` 题量减半 |
| 口头作答（不附答案页） | `--no-answers` |
| 复现同一套题 | `--seed 7`（不传则每次随机；JSON 里也写入了 `seed`） |
| 一键复现已发出去的卷子 | `--regen <旧.json>`（自动取 seed/level/lang/name） |
| 列出题型 × 等级矩阵 | `--list` |
| 姓名留空手填 | **默认就是空白下划线框**，也可 `--name 小明` 预填 |
| 全班批量（强制忽略 JSON 残留姓名） | `--no-name` |
| 高密度 / 大字号 | `--columns 3` / `--columns 1` |
| 英文界面 | `--lang en`（指令与答案同步翻译） |
| 显示得分栏 | `--score`（页尾可手填的得分/正确数/日期/评语） |

**完整参数表与配方见 `references/activity-spec.md`**；题量上限 30、观察类（maze/diff/same）单张自动 ≤ 4 题、诊断卷自动扩到覆盖全部题型。

### Step 3 · 交付

1. 用 present_files 呈现 HTML；提示用户浏览器「打印 / 另存为 PDF」并勾选「背景图形」
2. 回复中给**三条以内**家长指导：本次题型与数量、建议用时（L1/L2 约 10 分钟、L3/L4 约 15 分钟）、一条具体操作提示（如"先让孩子说出规律再填空"）。话术模板见 `references/pedagogy.md`
3. 不写过程描述、不写日期/来源，直接给内容与指导

### Step 4 · 批改与进阶

用户回传答案后：
1. 对照 JSON 判分：共 X 题、做对 Y 题、正确率 Z%
2. 决策：≥90% 升一级；60-89% 同级加练且错题题型占比提到 50%；<60% 降一级
3. 同一题型错 ≥2 题 → 错题重练：
   ```bash
   python "<skill>/scripts/generate_worksheet.py" \
     --review "<workspace>/L2.json" --wrong 4,7 \
     --out "<workspace>/L2_重练.html" --json "<workspace>/L2_重练.json"
   ```
4. 每级至少 3 份练习才晋级；连续两次 ≥90% 才允许跳级
5. 给家长的反馈固定三段：**结果 → 薄弱点 → 下一步**（一个改进点、5-10 分钟亲子小游戏）。禁止横向比较与否定性评价

### Step 5 · 进度记录（可选）

用户多次使用或要求时，在工作区维护 `幼儿思维学习档案.md`。模板见 `assets/progress-journal.md`。

## 硬规则

- 先理解后训练：L1-L3 一律不计速、不计时；只有 L4 后期才引入限时挑战
- 不在幼儿阶段引入抽象符号运算、负数、超纲逻辑（真值表、命题逻辑）
- 练习页必须含答案页（除非用户明确口头作答），方便家长核对
- 一次只提一个改进点，先肯定具体行为再纠错
- 每次只生成一份练习；观察/专注类题型单次 ≤ 4 题

## 安全与隐私（skillhub TRACE-T 红线）

- **零外网**：仅本地 Python 标准库 + 受信任第三方，无 `requests/urllib/socket/http` 调用
- **零凭证**：不读 ~/.ssh / .env / AppData / token / 浏览器缓存 / 操作系统目录
- **零执行注入**：所有输出经 HTML escape（`< > & " '`），学生姓名作为不信任输入处理
- **最小权限**：文件操作只在用户 CLI 传入的 `--out` / `--json` 路径与 `--out-dir` 子目录内
- **可审计**：所有生成 `*.json` 都带 seed，可在不出网情况下 `--regen` 字节级复现

## 文件清单

```
SKILL.md                ← 本文件：触发词 + Step 0-5 + 硬规则 + 安全清单
README.md               ← 5 秒上手 + 完整命令清单
CHANGELOG.md            ← 迭代日志
LICENSE                 ← MIT
assets/icon.png         ← Skill 图标
scripts/
  generate_worksheet.py ← CLI 主入口
  batch_roster.py       ← 花名册批量生成全班卷子
  test_skill.py         ← 上架前回归自检（19 项）
  preflight.py          ← 发布前合规自检（zip / YAML / 大小 / 路径）
  common.py             ← 共享样式 / I18N / 等级池
  generators/g_*.py     ← 题型插件（新增丢这里即可）
references/
  curriculum.md         ← L1-L4 知识点、题型映射、晋级标准
  activity-spec.md      ← 完整 CLI 参数表 / 配方 / 排版规范
  pedagogy.md           ← 家长话术 / 反馈模板
assets/
  progress-journal.md   ← 学习档案模板
```

## 故障排查

| 现象 | 原因 | 解法 |
|---|---|---|
| 打印时没有背景颜色 | 浏览器打印对话框「背景图形」未勾 | 打印设置里勾选「背景图形」 |
| 答案页与题目同页 | 浏览器禁用 `@media print` | Chrome / Edge 默认可用；Safari 需在打印高级选项开启「打印背景」 |
| `--regen` 报"JSON 不含 seed" | 该 JSON 来自 v1.0 之前 | 重装 v1.1+（v1.1+ 自动写入 seed 字段） |
| `--topics pattrn` 报错 | 1.0 之前会静默跳过 | v1.1+ 会列出合法值；改正拼写或留空 |
| 全班卷子全部预填同一名学生 | 忘了加 `--no-name` | 用 `--no-name` 强制空白 |
| 迷宫/图形在白底浏览器看不清 | CSS 未加载 | 重新生成最新版 |
| 嵌入调用种子不一致 | `--seed` 默认随机 | 显式传 `--seed` 即可字节级复现 |
| L1 出现等量代换 | 旧版本（v1.0 之前）等级污染 bug | 重装 v1.1+ |
| 字体乱码（极个别 PDF 工具） | 输出 `Microsoft YaHei` 等中文字体未安装 | stylesheet 有 `PingFang SC` fallback；最稳是把 PDF 导出到装有中文字体的设备 |
| 评分栏每题小勾选框不显示 | 忘记加 `--score` | 评分栏是可选开关，加 `--score` 显示 |

- 迷宫、找不同等开放题以"家长判断"为批改依据，不机械判对错

## 资源

- `references/curriculum.md` — 课程大纲与晋级标准
- `references/activity-spec.md` — 完整 CLI 参数、版式规范、组卷配方
- `references/pedagogy.md` — 家长话术、反馈模板
- `scripts/preflight.py` — 发布前自检（输出 `SHIP_REPORT.md`）

## 自检

修改后运行（应全部 PASS）：

```bash
python scripts/test_skill.py     # 19 项功能回归
python scripts/preflight.py     # 发布前合规自检
```

## Changelog

- **1.2.0** — skillhub 发布版：补齐 frontmatter 必填字段（`category`、`platforms`）、description 收紧到 ≤50 字、SKILL.md 渐进式披露、加入安全/隐私/无外网清单、新增 `preflight.py` 自检脚本
- **1.1.0** — 19 项回归测试；花名册批量出卷；错题/诊断/复现；姓名默认空白；`--no-name`/`--score`/`--lang`；主题色与 brand 角标
- **1.0.0** — 首次发布
