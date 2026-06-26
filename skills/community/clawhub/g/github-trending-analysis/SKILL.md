---
name: github-trending
description: 获取 GitHub 热门趋势项目（每日/每周/每月），访问每个仓库了解项目功能。默认返回前 10 个项目，包含描述、统计数据和从 README 提取的实际功能。用于用户询问 GitHub 趋势、热门仓库、流行项目时。始终用中文输出结果。
---

# GitHub Trending

获取并分析不同时间段的 GitHub 热门项目。

## 使用方式

触发短语：
- "github trending"
- "github 热门"
- "github 趋势项目"
- "最近 github 上有什么热门项目"

参数：
- `--period` 或 `-p`: 时间段（daily/weekly/monthly）。默认：daily
- `--limit` 或 `-l`: 返回项目数量（1-15）。默认：10
- `--language` 或 `-L`: 按编程语言过滤（如 python, javascript, rust）
- `--compare`: 对比模式，对比两个时间段（如 `daily,weekly` 或 `weekly,monthly`）
- `--report`: 生成趋势报告（weekly-report 或 monthly-report）

## 工作流程

### 基础模式（单时间段）

1. **抓取 trending 页面**
   - URL 模式：`https://github.com/trending?since={period}`
   - 使用 `web_fetch`，maxChars=15000
   - 解析 markdown 输出提取项目列表

2. **提取项目元数据**
   对列表中每个项目提取：
   - 仓库名称（owner/repo）
   - 描述
   - 编程语言
   - 总 Star 数
   - 本周期新增 Star 数
   - Fork 数

3. **访问每个仓库**
   - 抓取 `https://github.com/{owner}/{repo}`，maxChars=8000
   - 提取 README 内容（前 3-5 段）
   - 识别：项目功能、关键特性、使用场景
   - 优雅处理失败（跳过不可用的项目）

4. **格式化输出（中文）**
   返回 markdown 格式：
   ```markdown
   ## GitHub 热门项目 - {今日/本周/本月}
   
   ### 1. owner/repo
   **语言**: {language} | **Stars**: {total} (+{new} {今日/本周/本月})
   
   {原始描述}
   
   **项目功能**: {从 README 提取的内容}
   
   🔗 https://github.com/owner/repo
   
   ---
   ```

### 对比模式（--compare）

1. **抓取两个时间段的数据**
   - 分别获取两个时间段的 trending 列表
   - 提取每个项目的元数据

2. **分析差异**
   - **新上榜项目**：只在较短周期出现的项目
   - **持续热门**：两个周期都出现的项目
   - **热度变化**：对比 Star 增长速度

3. **输出对比报告**
   ```markdown
   ## GitHub 趋势对比：{周期1} vs {周期2}
   
   ### 📈 新上榜项目（仅在{周期1}）
   {列出新项目及其亮点}
   
   ### 🔥 持续热门（两个周期都在榜）
   {列出项目及热度变化}
   
   ### 📊 趋势洞察
   - 热门语言分布变化
   - 领域趋势（AI/工具/框架等）
   ```

### 报告模式（--report）

1. **周报（weekly-report）**
   - 抓取本周 daily trending（取 3 天采样）
   - 统计本周最热项目（按出现频次 + Star 增长）
   - 分析：
     - Top 10 本周最热项目
     - 热门技术栈
     - 新兴领域
   - 输出格式：
     ```markdown
     # GitHub 本周趋势报告
     **时间**: {日期范围}
     
     ## 🏆 本周 Top 10
     {项目列表 + 详细分析}
     
     ## 📊 技术趋势
     - 热门语言：{统计}
     - 热门领域：{AI/DevOps/Web 等}
     
     ## 💡 值得关注
     {3-5 个特别推荐项目}
     ```

2. **月报（monthly-report）**
   - 抓取本月 weekly trending（取 2-3 周采样）
   - 对比月初和月末的趋势变化
   - 输出格式类似周报，但包含月度趋势分析

## 实现要点

- 先抓取 trending 列表，然后按顺序访问仓库（避免并发触发速率限制）
- 如果仓库抓取失败，标记为"无法访问详情"并继续
- 每个项目的 README 提取限制在 ~500 字以内
- **输出必须使用中文**，包括标题、字段名、描述等所有内容

### 对比和报告模式的实现细节

- **对比模式**：顺序抓取两个时间段，避免并发请求
- **报告模式**：
  - 周报：采样 3 天（周一/周三/周五或最近 3 天）
  - 月报：采样 2-3 周（每周取一次 weekly trending）
  - 使用项目出现频次作为热度权重
  - 自动去重（同一项目多次出现只统计一次，但记录频次）
- **缓存策略**：可选将抓取结果保存到 `memory/github-trending-{date}.json` 避免重复请求

## 错误处理

- 网络超时：跳过项目，标记为不可用
- README 过长：截取前 3-5 段
- 语言过滤器无效：忽略过滤，抓取所有语言
- 时间段参数无效：默认使用 "daily"
- 对比模式参数格式错误：提示正确格式（如 `daily,weekly`）
- 报告模式采样失败：降级到单次抓取并说明

## 使用示例

```bash
# 基础查询
github trending
github trending --period weekly --limit 15

# 语言过滤
github trending --language python

# 对比模式
github trending --compare daily,weekly
github trending --compare weekly,monthly --language rust

# 报告模式
github trending --report weekly-report
github trending --report monthly-report --language javascript
```
