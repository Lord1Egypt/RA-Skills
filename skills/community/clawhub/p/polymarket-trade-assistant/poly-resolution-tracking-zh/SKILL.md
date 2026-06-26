---
name: poly-resolution-tracking-zh
version: 1.0.2
description: 追踪 Polymarket 市场的结算数据源。获取事件数据，解析结算条件，评估可追踪性，抓取数据源当前状态，并运行终端持续监控，以颜色编码的告警提示分数变化、领先者变化和市场/数据偏差。当用户要求追踪特定 Polymarket 市场的结算、监控结算数据源、或设置市场结算变化告警时使用此技能。
metadata: {"openclaw": {"emoji": "🎯", "requires": {"bins": ["python3"]}}}
---

# Polymarket 结算追踪器

监控特定 Polymarket 市场的结算数据源。检测可能影响市场结算的底层数据变化，与市场价格对比，并在出现重大变动时发出告警。

## 工作流程

按顺序执行以下 6 个步骤，不可跳过。

### 第 1 步：询问用户并获取事件

询问用户要追踪哪个市场。接受 Polymarket URL 或事件 slug。

运行事件获取脚本：

```bash
python scripts/fetch_event.py <slug_or_url>
```

脚本接受完整 URL（`https://polymarket.com/event/...`）或仅 slug。返回包含事件元数据和所有子市场的 JSON，包括价格、结果和描述。

向用户展示：
- 事件标题和 URL
- 子市场数量和按价格排列的候选
- 结算日期和剩余时间
- 描述的关键摘录（结算条件）

### 第 2 步：解析结算条件

阅读事件描述并提取：

1. **结算源 URL** — 确定结果的具体数据源
2. **指标** — 测量的内容（分数、排名、价格、票数等）
3. **结算日期/时间** — 何时进行检查
4. **条件** — 特殊规则（平局规则、回退机制、字母排序）
5. **候选项** — 子市场问题中的可能结果列表

将提取的条件清晰呈现给用户确认。

### 第 3 步：评估可追踪性

评估结算数据源是否可以自动监控。使用 [references/trackability-framework.md](references/trackability-framework.md) 中的框架。

检查四个维度：

1. **数据源可访问性** — URL 是否公开？是否需要 JS 渲染？
2. **指标客观性** — 指标是否定量/客观，还是主观的？
3. **数据格式** — JSON API、HTML 表格、PDF、视频？
4. **更新频率** — 源数据多久更新一次？

分配可追踪等级：

| 等级 | 条件 | 操作 |
|------|------|------|
| **完全** | JSON API + 定量指标 | 自动监控 |
| **部分** | 需要 HTML 抓取 | 通过脚本 + WebFetch 监控 |
| **手动** | 数据可访问但不可抓取 | 建议手动检查计划 |
| **不可** | 主观/私密/模糊 | 拒绝并说明原因 |

**扫描不可追踪关键词**（在描述中）："discretion"、"sole judgment"、"opinion"、"decides"、"may determine"、"subjective"。

**如果不可追踪（手动或不可）：**
- 具体说明无法自动追踪的原因
- 手动等级：根据距结算时间建议检查计划
- 不可等级：解释主观条件，建议改为监控市场价格
- **在此停止** — 不进入第 4-6 步

**如果可追踪（完全或部分）：** 继续第 4 步。

### 第 4 步：抓取结算数据

获取结算数据源的当前状态。

对已知源类型，使用抓取脚本：

```bash
python scripts/scrape_source.py --url <结算源_url> [--type arena_leaderboard|generic|auto]
```

脚本根据 URL 自动检测源类型。支持的类型：
- **arena_leaderboard**：Chatbot Arena / LMArena 排行榜（HTML 表格解析）
- **generic**：任何包含表格的 HTML 页面（提取所有表格）

如果脚本失败（JS 渲染内容、机器人检测），使用 **WebFetch** 作为回退获取渲染后的页面内容，然后手动提取相关数据。

将抓取的数据条目映射到市场候选项：
- 按组织/实体名称匹配
- 对每个候选项记录：排名、分数/指标值、置信区间（如有）
- 识别当前领先者和与第二名的差距

### 第 5 步：生成快照并对比

使用 [references/output-template.md](references/output-template.md) 中的模板展示初始状态：

1. **结算数据表** — 按排名列出候选项及分数
2. **市场价格表** — 候选项及当前市场概率
3. **对齐分析** — 数据领先者是否与市场领先者一致？
4. **风险评估：**
   - 领先差距（竞争有多接近？）
   - 置信区间重叠（置信区间是否重叠？）
   - 距结算时间
   - 市场确信度（市场有多确定？）

根据距结算时间推荐监控间隔：

| 距结算时间 | 建议间隔 |
|-----------|---------|
| > 7 天 | 360 分钟（6 小时） |
| 2-7 天 | 120 分钟（2 小时） |
| 1-2 天 | 60 分钟（1 小时） |
| < 24 小时 | 30 分钟 |
| < 6 小时 | 15 分钟 |

### 第 6 步：启动监控服务

询问用户是否要启动持续监控。如果是，运行：

```bash
python scripts/monitor.py --slug <slug> --interval <分钟数>
```

监控在前台运行，持续显示状态更新：

- **颜色编码告警**（终端输出）：
  - `CRITICAL`（红色）：领先者变更 — 结算结果将翻转
  - `WARNING`（黄色）：差距缩小、置信区间重叠、分数显著变化
  - `ALERT`（品红色）：市场价格与数据不一致
  - `INFO`（灰色）：无变化、微小更新
- **状态持久化**：每次循环保存状态到 `~/polymarket-tracking/`
- **差异对比**：每次循环对比当前与上次状态
- **优雅退出**：Ctrl-C 保存最终状态并退出

可选参数：
- `--once` — 运行单次快照后退出（不持续循环）
- `--alert-log <文件>` — 同时将告警以 JSON lines 格式写入日志文件
- `--state-dir <路径>` — 自定义状态目录（默认：`~/polymarket-tracking/`）

报告和状态文件保存到 `~/polymarket-tracking/`。

## 故障排除

- **脚本无法解析结算源页面**：页面可能使用 JS 渲染。用 WebFetch 获取渲染后内容，手动提取数据。
- **市场价格与候选名称不匹配**：检查子市场问题格式。候选名称提取处理 "Will X have the best..." 模式。对特殊格式需手动指定映射。
- **未找到 slug 对应的事件**：确认 slug 完全匹配。尝试直接访问 `https://gamma-api.polymarket.com/events?slug=<slug>` 验证。
- **监控每次循环显示 "No change"**：结算数据源未更新时属正常。考虑增大间隔以减少不必要的 API 调用。

## 参考文件

- [references/polymarket-api.md](references/polymarket-api.md) — Polymarket API 端点文档
- [references/trackability-framework.md](references/trackability-framework.md) — 可追踪性评估标准和不可追踪市场处理
- [references/output-template.md](references/output-template.md) — 报告模板和告警格式规范
