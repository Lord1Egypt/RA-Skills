---
name: jira-bug-analysis
description: >
  从 Jira Server/DC 拉取 Bug 数据，进行全面的 AI 分析，并生成交互式 HTML 报表。
  分析维度包括：Bug 趋势、优先级/严重程度分布、组件热点、解决时间、经办人负载、
  未解决 Bug 老化等。当用户要求分析 Jira Bug、生成 Bug 报表、或查看 Bug 指标时使用此 Skill。
argument-hint: "[project-key] [--server URL] [--token PAT] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]"
---

# Jira Bug Analysis Skill

从 Jira Server/Data Center 拉取 Bug 数据，进行全面分析，并生成自包含的 HTML 报表。

## Step 1: Gather Connection Parameters

向用户收集以下必要信息（如果用户已在调用参数中提供，则跳过询问）：

**必填参数：**
- **Jira Server URL**: 例如 `https://jira.company.com`
- **认证方式**（二选一）：
  - Personal Access Token (PAT)（推荐）
  - 用户名 + 密码
- **Project Key**: Jira 项目标识，例如 `PROJ`

**可选参数：**
- **起始日期** (`--start-date`): 筛选此日期之后创建的 Bug，格式 YYYY-MM-DD
- **结束日期** (`--end-date`): 筛选此日期之前创建的 Bug，格式 YYYY-MM-DD
- **Issue Type 名称** (`--issue-type`): 默认为 `Bug`。如果 Jira 实例使用中文或自定义名称（如 `故障`、`缺陷`），需指定实际名称。如果用户不确定，可先用 REST API 查询项目实际的 Issue Type 列表
- **Severity 自定义字段 ID** (`--severity-field`): 如果 Jira 实例中有「严重程度」自定义字段，提供其字段 ID（如 `customfield_10072`）。告诉用户可以在 Jira 管理后台的自定义字段页面找到此 ID
- 如果用户的 Jira 使用自签名证书，需要添加 `--no-verify` 参数

如果用户没有提供日期范围，建议默认使用最近 90 天。

## Step 2: Install Dependencies

运行以下命令安装 Python 依赖：

```bash
pip install -r ${SKILL_DIR}/requirements.txt
```

如果 `pip` 命令失败，尝试使用项目虚拟环境：

```bash
source ${SKILL_DIR}/.venv/bin/activate && pip install -r ${SKILL_DIR}/requirements.txt
```

## Step 3: Execute Data Pull

构建并执行以下命令来获取 Jira Bug 数据：

```bash
python ${SKILL_DIR}/scripts/get_jiraData.py \
  --server <JIRA_SERVER_URL> \
  --token <PAT> \
  --project <PROJECT_KEY> \
  [--issue-type Bug] \
  [--start-date YYYY-MM-DD] \
  [--end-date YYYY-MM-DD] \
  [--severity-field customfield_NNNNN] \
  [--no-verify]
```

如果使用用户名密码认证，将 `--token` 替换为 `--username <USER> --password <PASS>`。

**脚本输出**：stdout 为结构化 JSON 数据，stderr 为进度信息。捕获 stdout 的 JSON 内容进行后续分析。

**Issue Type 自动检测**：如果脚本返回 0 条数据，可能是 Issue Type 名称不匹配。此时应通过 REST API 查询项目实际的 Issue Type 列表：
```bash
curl -u <USER>:<PASS> -k <SERVER>/rest/api/2/project/<PROJECT_KEY> | python3 -c "import sys,json;[print(t['name']) for t in json.load(sys.stdin).get('issueTypes',[])]"
```
如果发现实际名称为中文（如 `故障`、`缺陷`），用 `--issue-type` 参数指定后重新执行。

**错误处理**：
- 如果脚本退出码非零，向用户展示 stderr 中的错误信息
- 401 错误：提示用户检查认证凭据
- 403 错误：提示用户检查项目访问权限
- 连接错误：提示用户检查服务器 URL 和网络/VPN 连接
- SSL 错误：建议使用 `--no-verify` 参数

## Step 4: Analyze the Data

基于获取到的 JSON 数据进行全面分析。JSON 包含三部分：`metadata`（元数据）、`aggregations`（聚合统计）、`issues`（原始 Issue 列表）。

**重点关注以下分析维度：**

### 4.1 Executive Summary（执行摘要）
- 总 Bug 数量、未解决数量、已解决数量
- 未解决率（未解决/总数）
- Bug 创建趋势方向（增长/稳定/下降）
- 平均解决时间

### 4.2 Bug Creation Trend（Bug 创建趋势）
- 按月展示 Bug 创建数量变化
- 识别峰值月份并尝试关联可能的原因
- 对比创建量与解决量的差异趋势

### 4.3 Priority Distribution（优先级分布）
- 各优先级的 Bug 数量和占比
- 如果 Blocker/Critical 占比异常高，发出警告

### 4.4 Severity Distribution（严重程度分布）
- 各严重程度级别的数量和占比（如果有 severity 数据）
- 对比 severity 与 priority 是否存在不匹配

### 4.5 Component/Module Hotspots（组件热点）
- 哪些组件的 Bug 最多
- 哪些组件的平均解决时间最长
- 识别需要重点关注的模块

### 4.6 Resolution Time Analysis（解决时间分析）
- 整体解决时间统计（均值、中位数、P90）
- 按优先级分析解决时间——高优先级 Bug 是否得到快速响应
- 按严重程度分析解决时间
- 识别解决时间异常长的 Bug

### 4.7 Assignee Workload（经办人工作负载）
- 各经办人的 Bug 分配数量
- 未分配的 Bug 数量
- 各经办人的已解决 Bug 数和解决效率

### 4.8 Unresolved Bug Aging（未解决 Bug 老化分析）
- 按老化区间统计：0-7天、8-30天、31-90天、90天以上
- 按优先级统计未解决的 Bug
- 标记超过 90 天未解决的高优先级 Bug

### 4.9 Labels & Tags（标签分析）
- 常见标签/主题分析
- 识别回归 Bug（regression 标签）等模式

### 4.10 Recommendations（建议）
- 基于以上分析提出 3-5 条可操作的改进建议
- 针对具体问题给出针对性建议（例如：组件 X 需要更多测试覆盖、经办人 Y 负载过高需要分摊等）

**已解决/未解决判定规则（两步判定）：**
脚本采用两步判定逻辑，聚合数据中的 `unresolved_count`、`by_assignee_detailed` 等字段均基于此规则：
1. **第一步**：检查 `resolution` 字段 — 不为空则判定为「已解决」
2. **第二步**：若 `resolution` 为空，再检查 `status` — 以下状态视为「已解决」：**已关闭、INVALID、DUPLICATED、无法复现、已解决**
3. 其余状态（如 OPEN、Inprogress、POSTPONE）视为「未解决」

每条 Issue 的 JSON 中包含 `_resolved` 布尔字段，表示最终判定结果。

**注意**：聚合数据已在 Python 脚本中预计算，直接使用 `aggregations` 中的数值，不要自行重新计算。只在需要具体举例时才引用 `issues` 数组中的个别 Issue。

## Step 5: Generate HTML Report

基于分析结果生成一个**自包含的 HTML 文件**，要求如下：

### 技术要求
- **单文件**：所有 CSS 和 JavaScript 内联在 HTML 中，不依赖外部 CDN 或文件
- **图表**：使用内联 SVG 绘制图表（柱状图、饼图、趋势图等），不使用外部图表库
- **兼容性**：可直接用 `file://` 协议在浏览器中打开

### 数据驱动渲染（重要）

**禁止在 HTML 中硬编码任何数据数值。** 所有图表和表格必须从嵌入的原始 JSON 数据动态渲染：

1. 在 HTML `<head>` 中嵌入完整的脚本输出 JSON：
   ```html
   <script>
   const REPORT_DATA = <将 get_jiraData.py 输出的完整 JSON 粘贴于此>;
   </script>
   ```
2. 所有 SVG 图表必须由 JavaScript 函数从 `REPORT_DATA.aggregations` 读取数据后动态创建 DOM 元素，**不得在 SVG 标签中手写数字**
3. Issue 明细表格从 `REPORT_DATA.issues` 数组渲染
4. 指标卡片（总数、未解决数等）从 `REPORT_DATA.aggregations` 和 `REPORT_DATA.metadata` 读取
5. AI 分析建议（Section 10）也应尽量从 `REPORT_DATA` 中读取数据动态拼接，而非手写固定数字

这样确保页面上展示的每一个数值都可追溯到原始数据，不存在数据编造或计算偏差的可能。

### 图表动态尺寸规则

- 所有水平柱状图的 SVG 高度必须根据数据项数量动态计算，**禁止使用固定高度**
- 计算公式：`svgHeight = dataItems.length * 40 + topPadding + bottomPadding`
- 每根柱子高度 28px，间距 12px
- 左侧为文字标签预留足够空间（至少 150px），标签不得超出 SVG viewBox
- 当数据项超过 15 个时，外层容器设置 `max-height: 600px; overflow-y: auto` 实现滚动

### 页面结构

```
Header: 报表标题、项目名称、日期范围、生成时间（蓝紫渐变背景）
Navigation: 顶部粘性导航栏，包含各章节锚点链接

Sections:
1. Executive Summary — 8 张指标卡片（4列x2行），数据从 aggregations 读取
   数据分类说明面板 — 可折叠，展示已解决/未解决的两步判定规则及来源拆分
2. Bug Trend — SVG 柱状图，按月展示创建数和解决数
3. Priority Distribution — SVG 水平柱状图或环形图
4. Severity Distribution — SVG 图表（如果有 severity 数据，否则跳过此节）
5. Component Hotspots — SVG 柱状图，按数量降序排列
6. Resolution Time — 统计表格（含说明列）+ 按优先级解决时间表格
7. Assignee Analysis — SVG 水平柱状图（使用 `aggregations.by_assignee_detailed` 数据，按 total 降序）+ 表格（经办人、总数、已解决、未解决、解决率、平均解决天数）。柱状图高度按经办人数量动态计算
8. Aging Analysis — SVG 柱状图展示老化区间分布 + 未解决按优先级表格
9. Labels — 柱状图（Top 25）
10. AI Recommendations — 从 REPORT_DATA 动态拼接的改进建议列表
11. Issue Detail Table — 完整 Bug 列表，支持客户端搜索、排序和 Excel 下载

Footer: 报告说明和生成信息
```

### 视觉风格
- 使用专业的**明亮主题**（页面背景 #f0f2f5，卡片/区块白色，Header 蓝紫渐变）
- 清晰的排版层次，紧凑间距，最大宽度 1200px
- 响应式布局，适配不同屏幕宽度
- SVG 图表使用 `viewBox` + `preserveAspectRatio="xMinYMin meet"` 实现自适应容器宽度，**禁止固定像素宽度**
- SVG 图表配色统一协调

### 指标卡片布局
- 使用 `grid 4 列` 布局（`grid-template-columns: repeat(4, 1fr)`），共 8 张卡片排成 2 行
- 每张卡片内部：上方为图标 + 标签（横排），下方为数值，再下方为灰色辅助信息
- 数值和标签必须设置 `overflow: hidden; text-overflow: ellipsis; white-space: nowrap` 防止内容溢出卡片边界
- 8 张卡片：总故障数、已解决、未解决、中位数解决时间、本月新增、90天+高龄、最热组件、积压最多的经办人

### 数据分类说明面板
在指标卡片下方放置一个**可折叠面板**，标题为「数据分类说明：已解决与未解决是如何判定的？」：
- 默认收起，点击展开
- 展开后清晰说明两步判定规则（resolution 优先，status 兜底）
- 左右两栏分别展示：已解决的来源拆分（resolution 判定 vs status 判定的各状态计数）、未解决的 status 分布
- 数据从 `REPORT_DATA.issues` 的 `_resolved`、`resolution`、`status` 字段动态统计

### 数据来源提示（Tooltip）
- 每个 Section 标题旁放置一个 **?** 圆形提示图标，鼠标悬停弹出气泡说明数据来源字段和计算方式
- 例如：趋势图提示「按 created / resolutiondate 按月聚合」，解决时间提示「resolution_days = (resolutiondate - created) / 86400」

### Issue 表格功能
- 搜索框：实时过滤表格内容
- 可点击列头排序
- 显示字段：Key、Summary、Status、Priority、Severity、Assignee、Created、Resolution Days
- 状态和优先级用不同颜色标记

### 原始数据 Excel 下载功能
在 Issue 明细表的搜索框旁边放置一个**「下载 Excel」**按钮，点击后在客户端生成并下载包含全部原始 Issue 数据的 Excel 文件。

**技术实现要求：**
- 使用纯 JavaScript 在客户端生成 **Excel XML Spreadsheet（Office 2003 XML 格式）**，不依赖任何外部库或 CDN
- 将全部 `issues` 数组中的数据写入 Excel，每条 Issue 一行
- **Excel 列**：Key、Summary、Status、Priority、Severity、Assignee、Reporter、Created、Resolved、Resolution、Components、Labels、Fix Versions、Original Estimate (h)、Time Spent (h)、Resolution Days
- 数值字段（估时、耗时、解决天数）使用 `Number` 类型，其余使用 `String` 类型
- 表头行加粗并设置背景色以便区分
- 设置合适的列宽（如 Summary 列 300、Key 列 80 等）
- 对 XML 特殊字符（`&`, `<`, `>`, `"`）进行转义
- 文件名格式：`{PROJECT_KEY}_bug_raw_data_{YYYY-MM-DD}.xls`
- 通过 `Blob` + `URL.createObjectURL` + 临时 `<a>` 标签触发下载

**按钮样式：**绿色背景（`#44bb66`），白色粗体文字，圆角，与搜索框同行排列

### 文件命名和保存
- 文件名：`{PROJECT_KEY}_bug_analysis_{YYYY-MM-DD}.html`
- 保存在用户的**当前工作目录**（不是 skill 目录）
- 生成后告知用户文件路径

## Error Recovery

- **脚本返回 0 条数据**：告知用户未找到匹配的 Bug，建议扩大日期范围或检查项目 Key 是否正确
- **Severity 字段全部为 null**：在报表中跳过严重程度分析章节，并在执行摘要中说明
- **数据量超过 500 条**：分析时重点关注聚合数据，只在必要时引用个别 Issue
- **网络或认证错误**：展示具体错误信息，给出排查建议
