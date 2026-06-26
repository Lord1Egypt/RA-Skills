---
name: openclaw-retro
description: |
  Weekly/periodic engineering retrospective skill that generates delivery reviews based on git history and code quality metrics. Supports 24h, 7d, 14d, 30d cycles with contributor analysis and growth recommendations.
  中文：每周/周期工程回顾技能，基于 git 历史与代码质量指标生成交付复盘。支持 24h、7d、14d、30d 周期，附带贡献者分析与成长建议。
  日本語：Git履歴と品質指標を使って週次レビューを自動化。/retro 24h/7d/14d/30d に対応し、貢献者ごとの振り返りと成長機会を提示。
  한국어：주간/주기적 엔지니어링 회고 에이전트. Git 이력과 품질 지표를 기반으로 /retro 24h/7d/14d/30d 분석을 수행하고 기여자별 피드백을 제공합니다.
  Español：Habilita retrospectivas de ingeniería semanales (24h/7d/14d/30d) usando historial de Git y métricas de calidad, con análisis por contribuidor y recomendaciones de crecimiento.
---

# ClawLite Retro — 工程回顾

当用户输入 `/retro` 时，运行此 skill。

## 参数

- `/retro` — 默认：最近 7 天
- `/retro 24h` — 最近 24 小时
- `/retro 14d` — 最近 14 天
- `/retro 30d` — 最近 30 天

解析参数确定时间窗口。如果没有给出参数，默认为 7 天。

**午夜对齐窗口：** 对于 `d`（天）单位，从本地午夜计算绝对开始日期。例如，如果今天是 2026-03-21 且窗口是 7 天：开始日期是 2026-03-14。使用 `--since="2026-03-14T00:00:00"` 进行 git log 查询。

---

## Step 1：收集原始数据

首先，获取 origin 并识别当前用户：
```bash
git fetch origin <default> --quiet
git config user.name
git config user.email
```

`git config user.name` 返回的名称是**"你"** — 读取这个 retro 的人。所有其他作者是队友。

并行运行所有这些 git 命令：

```bash
# 1. 窗口内所有提交（时间戳、主题、hash、作者、文件变化、行数变化）
git log origin/<default> --since="<window>" --format="%H|%aN|%ae|%ai|%s" --shortstat

# 2. 每次提交的测试 vs 总 LOC 细分（带作者）
git log origin/<default> --since="<window>" --format="COMMIT:%H|%aN" --numstat

# 3. 提交时间戳（用于会话检测和每小时分布）
git log origin/<default> --since="<window>" --format="%at|%aN|%ai|%s" | sort -n

# 4. 最常更改的文件（热点分析）
git log origin/<default> --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn

# 5. 每位作者的提交数量
git shortlog origin/<default> --since="<window>" -sn --no-merges

# 6. 测试文件数量
find . -name '*.test.*' -o -name '*.spec.*' 2>/dev/null | grep -v node_modules | wc -l

# 7. TODOS.md 积压
cat TODOS.md 2>/dev/null || true
```

---

## Step 2：计算指标

以摘要表形式计算和呈现这些指标：

| 指标 | 值 |
|------|----|
| 提交到 main | N |
| 贡献者 | N |
| 合并 PR | N |
| 总插入行数 | N |
| 总删除行数 | N |
| 净增 LOC | N |
| 测试 LOC（插入）| N |
| 测试 LOC 比例 | N% |
| 版本范围 | vX.Y.Z → vX.Y.Z |
| 活跃天数 | N |
| 检测到的会话 | N |
| 平均 LOC/会话小时 | N |

然后在下面立即显示**每位作者排行榜**：

```
贡献者            提交数   +/-          主要区域
你 (garry)           32   +2400/-300   browse/
alice                12   +800/-150    app/services/
bob                   3   +120/-40     tests/
```

按提交数降序排序。当前用户（来自 `git config user.name`）总是排第一，标记为"你 (名称)"。

**积压健康（如果 TODOS.md 存在）：**
- 总开放 TODOs（排除 `## Completed` 章节中的项目）
- P0/P1 计数（关键/紧急项目）
- 此期间完成的项目

---

## Step 3：提交时间分布

以小条形图显示本地时间的每小时提交直方图：

```
小时  提交数  ████████████████
 00:    4      ████
 07:    5      █████
...
```

识别并标注：
- 高峰时间
- 死区
- 模式是双峰（早晨/晚上）还是连续的
- 深夜编码集群（晚上 10 点后）

---

## Step 4：工作会话检测

使用连续提交之间的 **45 分钟间隔**阈值检测会话。

分类会话：
- **深度会话**（50+ 分钟）
- **中等会话**（20-50 分钟）
- **微型会话**（<20 分钟，通常是单次提交的快速修复）

计算：
- 总活跃编码时间（会话持续时间总和）
- 平均会话长度
- 每活跃小时的 LOC

---

## Step 5：提交类型细分

按常规提交前缀分类（feat/fix/refactor/test/chore/docs）。显示为百分比条：

```
feat:     20  (40%)  ████████████████████
fix:      27  (54%)  ███████████████████████████
refactor:  2  ( 4%)  ██
```

如果 fix 比例超过 50% — 标记为"快速发货，快速修复"模式，可能表明审查缺口。

---

## Step 6：热点分析

显示 top 10 最常更改的文件。标记：
- 更改 5+ 次的文件（流失热点）
- 热点列表中的测试文件 vs 生产文件
- VERSION/CHANGELOG 频率（版本纪律指标）

---

## Step 7：本周发布

**专注度分数：** 计算触及最常更改的顶级目录（例如 `app/services/`）的提交百分比。更高分数 = 更深入的专注工作。更低分数 = 分散的上下文切换。报告为："专注度分数：62%（app/services/）"

**本周最大发布：** 自动识别窗口中单个最高 LOC 的 PR。突出显示：
- PR 编号和标题
- LOC 变化
- 为什么重要（从提交消息和改动文件推断）

---

## Step 8：团队成员分析

对于每位贡献者（以你（当前用户）开始，然后是队友）：

### 你

```
📊 你的本周回顾
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
提交数:    N    [commit type breakdown]
代码变化:  +X/-Y  (净 Z LOC)
测试覆盖:  N% 的提交有测试变化
专注区域:  主要在 [top directory]
会话:      N 次（其中 D 次深度会话）

本周亮点:
• [基于实际提交的具体内容]
• [这周值得注意的内容]

值得关注:
• [具体的、建设性的反馈，基于数据]
```

### 每位队友

```
👤 [姓名]
━━━━━━━━━━━━━
提交数:    N
代码变化:  +X/-Y
专注区域:  [directory]

表扬:
• [基于他们做的具体内容 — 引用真实提交/文件]

成长机会:
• [具体的、建设性的内容，基于数据，不是泛泛而谈]
```

**反表扬规则（反垃圾 AI）：**
- 好的："你在 auth/ 重构了 UserSessionManager — 这是真正的架构改进，不只是移动代码。"
- 坏的："你展示了强大的工程技能。"
- 好的："修复了 3 个单独的错误，但都在 checkout/ — 那个区域的 bug 密度值得深入研究。"
- 坏的："你解决了问题，显示了你解决问题能力。"

**成长机会必须有数据：** 如果你找不到来自实际提交的建设性内容，写"数据太少，无法给出有意义的建议" — 不要编造反馈。

---

## Step 9：TODOS.md 积压审查

如果 TODOS.md 存在：

1. **本周完成的项目：** 交叉引用 diff 与 TODOS.md。哪些项目有证据表明已完成？
2. **添加的新 TODOs：** 检查 diff 中的 `TODO`、`FIXME`、`HACK` 注释，与 TODOS.md 中已知项目交叉引用。
3. **P0/P1 更新：** 任何关键项目需要基于本周工作重新优先排序？

---

## Step 10：本周总结 + 下周焦点

**一段总结** — 将这一切联系在一起。本周发生了什么？什么变得更好了？什么仍然是挑战？

**下周建议焦点（1-3 项）：**
- 基于数据，不是凭空想象
- 具体，可操作
- 按影响排序

---

## 输出格式

以此顺序呈现：

1. 📈 **指标摘要表**
2. 👥 **贡献者排行榜**
3. ⏰ **时间分布直方图**
4. 🔥 **热点分析**
5. 🚀 **本周最大发布**
6. 👤 **团队成员分析**（你先，然后队友）
7. 📋 **积压审查**（如果适用）
8. 📝 **本周总结 + 下周焦点**

---

## 完成状态

- **DONE** — 回顾完成，覆盖所有贡献者
- **DONE_WITH_CONCERNS** — 完成但有值得注意的问题（例如 fix 比例高，热点集中）
- **BLOCKED** — 无法访问 git 历史或在指定窗口中没有提交
