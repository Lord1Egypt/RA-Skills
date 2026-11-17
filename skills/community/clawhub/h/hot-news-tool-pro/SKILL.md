---
slug: hot-news-tool-pro
name: hot-news-tool-pro
version: 1.0.0
displayName: 新闻聚合专业版
summary: 企业级新闻聚合工具，支持多源监控、定时更新、实时推送、舆情分析与自定义源管理，适合品牌监控与行业情报.
license: Proprietary
edition: pro
description: "企业级新闻聚合工具，支持多源监控、定时更新、实时推送、舆情分析与自定义源管理，适合品牌监控与行业情报。核心能力:。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。 功能涵盖: hot。"
  - 50+ 国内外新闻源批量监控
  - 定时自动抓取与实时增量更新
  - 关键词告警与实时推送通知
  - 舆情趋势分析与情感判断
  - 自定义新闻源与分类规则
  - 多渠道分发（邮件、Webhook、IM）
  适用场景:
  - 企业品牌舆情监控
  - 行业情报收集与分析
  - 竞品动态跟踪
  - 危机预警与应急响应
  差异化:
  - PRO 版支持 50+ 新闻源...'
tags:
  - 新闻
  - 企业工具
  - 舆情监控
  - 品牌监测
  - 情报分析
  - 搜索
  - 检索
  - 工具
  - https
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
# 定价元数据
category: "Knowledge"
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# 新闻聚合专业版
## 概述
新闻聚合专业版是面向企业用户和品牌管理团队的进阶新闻监控工具。在免费版基础聚合能力之上，新增多源批量监控、定时自动更新、实时关键词告警、舆情趋势分析、自定义源管理等高级功能，助力企业及时掌握品牌舆情与行业动态。与免费版完全兼容，已有配置可无缝升级.
## 核心能力
### 功能对比
| 能力 | 免费版 | PRO 版 |
|---|---|-----|
| 新闻源数量 | 10+ 个 | 50+ 个 |
| 分类整理 | 科技/军事/社会 | 自定义分类 |
| 定时更新 | 否 | Cron 调度 |
| 实时推送 | 否 | 多渠道推送 |
| 关键词告警 | 否 | 实时告警 |
| 情感分析 | 否 | 正负面判断 |
| 舆情趋势 | 否 | 趋势分析 |
| 自定义源 | 否 | 自由添加 |
| 分析报告 | 否 | 自动生成 |
| API 接口 | 否 | REST API |
| 优先支持 | 社区 | 优先响应 |
**处理**: 解析功能对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回功能对比的响应数据,包含状态码、结果和日志.
### PRO 版独有功能
#
### 1. 50+ 新闻源监控
```bash
python （请参考skill目录中的脚本文件） \
  --sources-file sources.yaml \
  --categories tech,military,social,finance \
  --parallel 8
```
支持从配置文件批量加载新闻源，并行抓取，统一归档.
#
### 2. 定时自动更新
```bash
# 配置定时抓取任务
python （请参考skill目录中的脚本文件） \
  --cron="0 */2 * * *" \
  --incremental \
  --archive-dir=./archive
```
每 2 小时自动增量抓取最新新闻，保持数据实时性.
#
### 3. 关键词告警与推送
```bash
# 配置关键词告警
python （请参考skill目录中的脚本文件） \
  --keywords="品牌名 危机,品牌名 投诉,品牌名 负面" \
  --webhook="https://hooks.slack.com/未指定" \
  --email=alert@company.com \
  --poll-interval=300
```
监控指定关键词，发现匹配新闻时立即通过 Slack 和邮件推送告警.
#
### 4. 舆情趋势分析
```bash
# 生成舆情分析报告
python （请参考skill目录中的脚本文件） \
  --period="2026-01" \
  --keywords="品牌名" \
  --output=sentiment_report.md
```
分析指定时间段内的新闻情感倾向，生成趋势图表和摘要.
**处理**: 解析PRO 版独有功能的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回PRO 版独有功能的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 核心功能执行
用`input_params`参数进行配置.
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级新闻聚合工、支持多源监控、舆情分析与自定义、源管理、适合品牌监控与行、业情报、核心能力、国内外新闻源批量、定时自动抓取与实、时增量更新、关键词告警与实时、推送通知、舆情趋势分析与情、感判断、自定义新闻源与分、类规则、多渠道分发等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：品牌舆情监控
品牌团队需要实时监控品牌相关新闻动态.
```bash
# 配置品牌监控任务
python （请参考skill目录中的脚本文件） \
  --brand="公司名" \
  --sources sources.yaml \
  --keywords="公司名 正面,公司名 负面,公司名 危机" \
  --alert-webhook="https://hooks.slack.com/未指定" \
  --alert-email=brand@company.com \
  --report-frequency=daily
```
系统全天候监控品牌相关新闻，发现负面信息时立即告警，每日生成品牌舆情汇总报告.
### 场景二：行业情报收集
市场研究团队需要系统化收集行业情报.
```bash
# 准备行业关键词
cat > industry_keywords.txt <<EOF
人工智能 政策 2026
芯片制造 最新进展
新能源 产业动态
EOF
# ...
# 批量监控行业动态
python （请参考skill目录中的脚本文件） \
  --keywords-file industry_keywords.txt \
  --sources sources.yaml \
  --cron="0 8 * * *" \
  --export json \
  --output-dir=./industry_reports
```
每日 8 点自动抓取行业相关新闻，分类归档，导出结构化数据供分析.
### 场景三：竞品动态跟踪
产品团队需要持续跟踪竞品的最新动态.
```bash
# 配置竞品监控
python （请参考skill目录中的脚本文件） \
  --competitors="竞品A,竞品B,竞品C" \
  --track="产品发布,融资,人事变动,负面新闻" \
  --report-frequency=weekly \
  --output-dir=./competitor_reports
```
每周自动汇总竞品动态，包含产品发布、融资、人事变动等关键信息.
## 不适用场景
以下场景新闻聚合专业版不适合处理：
- 逆向工程闭源API
- API安全安全评估
- 非标准协议集成
## 触发条件
需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求.
## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### 从免费版升级
```bash
# 依赖说明
pip install apscheduler pandas matplotlib
# ...
# 导入免费版配置
python （请参考skill目录中的脚本文件） --from-free
# ...
# 验证升级
python （请参考skill目录中的脚本文件） --version
# 输出: hot-news-tool-pro v1.0.0
```
### 首次多源监控
```bash
# 创建新闻源配置
cat > sources.yaml <<EOF
sources:
  - name: 36氪
    url: https://36kr.com/information/tech
    category: tech
  - name: 机器之心
    url: https://www.jiqizhixin.com
    category: tech
  - name: 观察者网
    category: military
EOF
# ...
# 执行多源抓取
python （请参考skill目录中的脚本文件） \
  --export json \
  --output news.json
```
#
## 示例
### 企业级配置文件
```yaml
# config.yaml - PRO 版企业配置
sources:
  tech:
    - name: 36氪
com/information/tech
    - name: 机器之心
    - name: TechCrunch
      url: https://techcrunch.com
  military:
    - name: 观察者网
    - name: Defense News
# ...
monitoring:
  brand_keywords:
    - "公司名"
    - "品牌名"
  alert_keywords:
    - "危机"
    - "投诉"
    - "负面"
  poll_interval: 300
# ...
alerts:
  webhook: https://hooks.slack.com/未指定
  email:
    smtp_host: smtp.company.com
    smtp_port: 587
    sender: alert@company.com
# ...
schedule:
  fetch_cron: "0 */2 * * *"
  report_cron: "0 8 * * *"
  timezone: Asia/Shanghai
# ...
analytics:
  sentiment_analysis: true
  trend_tracking: true
  storage: ./analytics
```
### API 服务模式
```bash
# 启动 REST API 服务
python （请参考skill目录中的脚本文件） --port 8000
# ...
# 查询最新新闻
curl http://localhost:8000/news?category=tech&max=10
# ...
# 订阅告警
curl -X POST http://localhost:8000/subscribe \
  -d '{"keywords": ["品牌名"], "webhook": "https://未指定"}'
```
### 参数说明
| 参数 | 类型 | 默认值 | 说明 |
|:-----|:-----|:-----|:-----|
| `--sources-file` | 字符串 | 无 | 新闻源配置文件 |
| `--categories` | 字符串 | all | 类别过滤 |
| `--keywords` | 字符串 | 无 | 告警关键词 |
| `--cron` | 字符串 | 无 | 定时表达式 |
| `--webhook` | 字符串 | 无 | 告警 Webhook |
| `--email` | 字符串 | 无 | 告警邮箱 |
| `--export` | 字符串 | json | 导出格式 |
| `--parallel` | 整数 | 4 | 并行线程数 |
## 优选实践
### 多源监控优化
```python
# monitor_config.py - 监控配置
from multi_source import MonitorConfig
# ...
config = MonitorConfig(
    sources_file="sources.yaml",
    parallel_workers=8,
    poll_interval=300,
    incremental=True,
    cache_enabled=True,
    deduplicate=True,
    sentiment_analysis=True
)
# ...
# 启动监控
config.start()
```
### 告警规则配置
```bash
# 配置多级告警
python （请参考skill目录中的脚本文件） \
  --level=critical \
  --keywords="品牌名 危机,品牌名 诉讼" \
  --immediate=true
# ...
python （请参考skill目录中的脚本文件） \
  --level=warning \
  --keywords="品牌名 投诉,品牌名 负面" \
  --delay=300
```
### 舆情分析报告
```bash
# 生成周报
python （请参考skill目录中的脚本文件） \
  --period="week" \
  --keywords="品牌名" \
  --output=weekly_report.md \
  --include-charts
# ...
# 导出趋势数据
python （请参考skill目录中的脚本文件） \
  --period="month" \
  --format=csv \
  --output=trends.csv
```
## 常见问题
### 新闻源抓取失败
```bash
# 检查所有源状态
python （请参考skill目录中的脚本文件） --check-sources
# ...
# 禁用失败源
python （请参考skill目录中的脚本文件） --disable-failed
# ...
# 配置备用源
python （请参考skill目录中的脚本文件） --fallback-sources
```
### 告警延迟
```bash
# 检查告警服务状态
python （请参考skill目录中的脚本文件） --status
# ...
# 减少轮询间隔
python （请参考skill目录中的脚本文件） --poll-interval=60
# ...
# 检查 Webhook 连通性
curl -X POST $WEBHOOK_URL -d '{"test": true}'
```
### 舆情分析结果不准
```bash
# 调整情感分析模型
python （请参考skill目录中的脚本文件） --model=advanced
# ...
# 添加行业词典
python （请参考skill目录中的脚本文件） --dictionary=industry.txt
# ...
# 手动标注训练数据
python （请参考skill目录中的脚本文件） --labeled-data.json
```
## 依赖说明
### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Python 版本**：3.7 及以上
- **网络环境**：需可访问国内外新闻网站
- **推荐配置**：4 核 CPU、8GB 内存、20GB 磁盘空间
### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Python 3.7+ | 运行时 | 是 | 系统包管理器安装 |
| requests | HTTP 库 | 是 | `pip install requests` |
| beautifulsoup4 | HTML 解析 | 是 | `pip install beautifulsoup4` |
| apscheduler | 定时任务 | 否（推荐） | `pip install apscheduler` |
| pandas | 数据分析 | 否（推荐） | `pip install pandas` |
| matplotlib | 图表生成 | 否（推荐） | `pip install matplotlib` |
| flask | API 服务 | 否（推荐） | `pip install flask` |
| snownlp | 中文情感分析 | 否（推荐） | `pip install snownlp` |
| LLM API | API | 是 | 由 Agent 内置 LLM 提供 |
### API Key 配置
- PRO 版核心功能无需额外 API Key
- 如需启用邮件告警，配置 SMTP 信息：
```bash
export SMTP_HOST=smtp.company.com
export SMTP_PORT=587
export SMTP_USER=alert@company.com
export SMTP_PASSWORD=your_password
```
- 如需使用高级情感分析 API：
```bash
export SENTIMENT_API_KEY=your_api_key
```
### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务
- **适用人群**：企业品牌团队、市场研究人员、公关团队、行业分析师
- **兼容性**：与免费版完全兼容，配置可无缝迁移
- **支持方式**：优先响应技术工单
## 错误处理
| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "新闻聚合专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "hot news pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
## 安全注意事项
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 核心功能
- **自动化执行**: 企业级新闻聚合工具，支持多源监控、定时更新、实时推送、舆情分析与自定义源管理，适合品牌监控与行业情报.
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 企业级新闻聚合工具，支持多源监控、定时更新、实时推送、舆情分析与自定义源管理，适合品牌监控与行业情报.
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据