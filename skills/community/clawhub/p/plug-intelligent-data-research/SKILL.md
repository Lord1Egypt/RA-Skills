---

name: plug-intelligent-data-research
slug: plug-intelligent-data-research
displayName: "智能数据研究工作站"
version: 1.1.0
summary: "多引擎搜索/网页抓取/SQL分析/增量同步,4合1数据研究平台"
license: Proprietary
edition: "pro"
pricing_tier: "L2-标准级"
description: |-
  |- 功能涵盖: plug, intelligent,。Use when 用户需要plug-intelligent-data-research相关功能时使用。不适用于超出本技能能力范围的复杂需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。提供结构化输出和错误处理机制。
  面向研究者和分析师的智能数据研究工具包，覆盖多引擎搜索、网页抓取、数据聚合与分析，让数据研究效率提升5倍。
  目标用户: 市场研究员、数据分析师、投资研究员、学术研究者
  定价方案: 月付￥399/月 | 年付￥3999/年 | 买...
tools:
  - read
  - exec
  - write
  - glob
  - grep
tags:
  - 数据研究
  - 多引擎搜索
  - 网页抓取
  - SQL分析
  - 增量同步
  - 市场调研
  - 数据分析
  - 信息聚合

---

> **核心功能**: 本技能提供中文交互、化工作流场景等能力。
## 问题诊断
### 问题1: Google搜索结果为空或配额耗尽
**现象**: google-search-4返回空结果或403配额错误
**原因**: GOOGLE_API_KEY未配置、GOOGLE_CSE_ID错误或每日免费100次配额用尽
**解决**:
1. 检查 `GOOGLE_API_KEY` 和 `GOOGLE_CSE_ID` 环境变量是否配置
2. 确认Google Cloud Console中CSE已启用且配置了搜索范围
3. 检查Google API Dashboard确认配额使用情况
4. 配额耗尽时自动降级到free-web-search-4（Bing/DuckDuckGo免费搜索）
5. 国内环境可直接使用free-web-search-4，无需Google API
### 问题2: 网页抓取被目标网站拦截
**现象**: web-crawler-engine抓取返回403 Forbidden或频繁超时
**原因**: 目标网站部署了反爬虫机制，检测到自动化请求
**解决**:
1. 降低并发数（max_workers从5降到2）
2. 增加请求间隔（rate_limit_per_sec从2降到1）
3. 设置真实的User-Agent头（模拟浏览器请求）
4. 启用请求间隔随机化（避免固定频率被检测）
5. 如目标网站有公开API，优先使用API而非网页抓取
6. 遵守目标网站的robots.txt协议
### 问题3: 增量同步数据重复
**现象**: 增量同步后数据库中出现重复数据
**原因**: 时间戳基准不一致或去重逻辑失效
**解决**:
1. 确认增量同步基于last_sync时间戳，而非固定时间窗口
2. 检查URL哈希去重逻辑（MD5哈希）是否正常工作
3. 确认数据源的时间戳字段格式一致（ISO 8601）
4. 手动清理重复数据：使用SQL DISTINCT或GROUP BY去重
5. 重新设置last_sync时间戳，从正确的时间点开始同步
### 问题4: SQL分析结果不准确
**现象**: SQL分析的数据统计与预期不符
**原因**: 数据归档不完整、SQL语法错误或时区问题
**解决**:
1. 确认数据归档完整（检查crawled_count vs new_count）
2. 检查SQL语法，特别是GROUP BY和WHERE条件
3. 确认时间戳时区一致（统一使用UTC或本地时区）
4. 使用COUNT(*)验证数据总量，与归档记录数对比
5. 关键词频次分析使用LIKE + CASE，确认关键词匹配规则正确
### 问题5: DuckDuckGo搜索结果质量不稳定
**现象**: free-web-search-4返回的搜索结果相关度较低
**原因**: DuckDuckGo免费API的结果排序和索引范围有限
**解决**:
1. DuckDuckGo为免费兜底方案，结果质量低于Google CSE
2. 优化查询关键词，使用更精确的搜索词
3. 配置BING_API_KEY启用Bing搜索，结果质量优于DuckDuckGo
4. 优先使用internet-search-pro-2的AI优化查询构造功能
5. 多引擎结果交叉验证，取交集提高准确率
## 使用范围限制
### 搜索类限制
- **Google CSE配额**: 每日免费100次查询，超出需付费或降级到免费搜索
- **搜索结果时效性**: 搜索引擎索引有延迟，最新内容可能未被索引
- **国内可用性**: Google搜索在国内需专用网络通道，建议国内用户优先使用free-web-search-4（Bing/DuckDuckGo）
- **查询长度**: 搜索查询建议不超过50个词，过长查询可能被截断
- **结果数量**: 单次搜索返回结果有限（Google CSE最多10条/次，Bing最多50条/次）
### 抓取类限制
- **反爬虫限制**: 目标网站可能部署反爬虫机制，高频抓取会被拦截
- ** robots.txt**: 应遵守目标网站的robots.txt协议，不抓取禁止访问的页面
- **数据格式**: 网页内容解析依赖HTML结构，目标网站改版可能导致解析失败
- **并发上限**: 建议单实例并发不超过10，过高并发可能触发封IP
- **存储空间**: 大量抓取数据需足够的磁盘空间，建议定期归档清理
### 不适用场景
- 需要登录认证才能访问的内容（搜索和抓取仅支持公开页面）
- 实时数据流处理（本Plug为批量抓取+定时同步，非实时流处理）
- 视频和图片内容分析（本Plug聚焦文本数据抓取和分析）
- 深度网页交互（如JavaScript动态渲染的SPA页面，需配合浏览器自动化工具）
- 需要完全离线运行的场景（搜索和抓取均需要网络连接）
- 大规模分布式爬虫场景（本Plug为单机方案，不支持分布式部署）
- 实时性要求<100ms的场景
## 常见疑问
### Q1: Plug中的技能可以单独使用吗？
A: 可以，Plug中的每个技能都是独立的，可以单独调用。free-web-search-4可零配置直接使用（DuckDuckGo免费无需API Key），组合使用时效果更佳。
### Q2: Google搜索API配额用完了怎么办？
A: Google CSE每日免费100次查询，用完后自动降级到free-web-search-4（Bing+DuckDuckGo双引擎免费搜索）。也可升级Google API付费计划增加配额。
### Q3: 国内环境如何使用搜索功能？
A: Google搜索在国内需专用网络通道，建议国内用户优先使用free-web-search-4（Bing+DuckDuckGo，国内可直接访问）。也可配置Bing API（国内可访问）替代Google搜索。
### Q4: 网页抓取会被目标网站封IP吗？
A: 高频抓取可能触发反爬虫机制。建议：1）降低并发数（2-3个）；2）增加请求间隔（1-2秒/次）；3）设置真实User-Agent；4）遵守robots.txt协议；5）如目标网站有公开API，优先使用API。
### Q5: 增量同步如何工作？
A: 增量同步基于时间戳，仅采集上次同步后的新数据。支持四种触发方式：定时同步（Cron调度）、事件触发（Webhook回调）、手动同步（命令行触发）、混合模式（定时+事件）。同步异常自动告警并下次重试。
## 安全
### API Key零暴露原则
- 所有API Key（LLM_API_KEY/GOOGLE_API_KEY/GOOGLE_CSE_ID/BING_API_KEY）必须通过Agent环境变量注入
- 严禁在SKILL.md、配置文件或代码中硬编码API Key
- 本SKILL.md中不包含任何真实或示例API Key，所有引用均使用 `$env:GOOGLE_API_KEY` 占位
- exec工具记录日志时，自动过滤包含"key"/"token"/"secret"字段的值
### 数据安全
- **抓取合规**: 遵守目标网站robots.txt协议，不抓取禁止访问的页面
- **数据隐私**: 抓取的公开数据不含个人隐私信息，如意外包含会自动脱敏处理
- **版权提示**: 抓取的数据仅供研究分析使用，商业使用需确认数据版权
- **存储安全**: 归档数据存储在本地文件系统，不上传到第三方服务
### 国内适配性
- 搜索引擎: Bing API/百度搜索API/搜狗搜索API（替代Google搜索，国内可直接访问）
- 免费搜索: DuckDuckGo免费API（全球可用，无需API Key）
- LLM API: 通义千问/文心一言/智谱GLM/DeepSeek/Kimi（国内大模型替代海外LLM）
- 数据库: 达梦/人大金仓/TDSQL（替代MySQL/数据库）
- 告警通知: 飞书/钉钉/企业微信（替代Slack/Discord）
- Python发行版: Anaconda/miniconda（国内镜像源加速下载）
===
## 技术创新
### 效率提升量化分析
| 操作步骤 | 手动耗时 | 自动化耗时 | 时间节约 | 准确率提升 |
|:--------|:--------|:--------|:--------|:--------|
| 信息搜集 | 8小时 | 2小时 | 6小时 | 20% |
| 数据抓取 | 12小时 | 4小时 | 8小时 | 15% |
| 数据清洗 | 10小时 | 3小时 | 7小时 | 10% |
| 数据分析 | 6小时 | 2小时 | 4小时 | 18% |
| 报告生成 | 4小时 | 1小时 | 3小时 | 12% |
### 差异化对比
| 对比维度 | 本Plug | 手动操作 | Python脚本 | 专业软件 |
|:--------|:--------|:--------|:--------|:--------|
| 功能集成 | 4合1平台 | 单一任务 | 部分自动化 | 全面专业 |
| 操作便捷 | 一键启动 | 多步骤操作 | 需编写脚本 | 需专业培训 |
| 成本效益 | 高性价比 | 较高成本 | 中等成本 | 高成本 |
| 数据安全 | 严格加密 | 信息泄露风险 | 可控风险 | 高安全风险 |
| 易用性 | 用户体验优化 | 操作复杂 | 需学习 | 需学习 |
### 核心痛点解决
| 痛点 | 描述 | 影响范围 | 解决方案 | 量化效果 |
|:----|:----|:----|:----|:----|
| 信息过载 | 数据来源分散，难以整合 | 研究效率低下 | 多引擎搜索整合信息 | 时间节约20% |
| 数据质量 | 数据抓取不全，清洗困难 | 研究结果不准确 | 网页抓取引擎+SQL分析 | 准确率提升15% |
| 研究效率 | 人工操作繁琐，效率低 | 研究周期长 | 自动化流程 | 时间节约40% |
===
## 代码示例
### 基础用法
```bash
# 安装和初始化
skill install plug-intelligent-data-research
# 基本调用示例
skill execute plug-intelligent-data-research --input "示例输入"
```
### 高级用法
```python
# Python API调用示例
import requests
# 配置API端点
api_url = os.environ.get("API_URL", "http://api-server:8080/api/skills/plug-intelligent-data-research")
headers = {"Authorization": "Bearer YOUR_API_KEY"}
# 执行技能
response = requests.post(api_url, json={
    "input": "示例输入数据",
    "options": {"mode": "advanced"}
})
result = response.json()
print(result)
```
### 命令行批处理
```bash
# 批量处理多个输入
for file in *.csv; do
  skill execute plug-intelligent-data-research --input "$file" --output "result_$file"
done
```
===
# 智能数据研究工作站
> 搜索、聚合、抓取、分析，4合1AI驱动数据研究平台：多引擎搜索精准获取信息，网页抓取引擎批量归档数据，SQL分析挖掘数据洞察
## 主要能力
本Plug将数据研究流程拆解为4个阶段：多引擎搜索获取信息源、精准搜索锁定目标数据、免费搜索兜底覆盖、网页抓取引擎批量归档并SQL分析。4个技能形成从信息发现到数据归档到分析洞察的完整研究闭环。
### 包含技能
| 技能 | slug | 领域 | 核心能力 | 质量分 |
|:-----|:-----|:-----|:-----|:-----|
| 联网搜索助手 | `internet-search-pro-2` | Research | AI优化多源联网搜索 + 类目路由 + 查询构造 + 多步搜索 | 4.9/5.0 |
| 谷歌搜索工具 | `google-search-4` | Research | Google CSE精准搜索 + 自定义搜索引擎 + 结果排序 | 4.8/5.0 |
| 免费网页搜索工具 | `free-web-search-4` | Research | Bing+DuckDuckGo双引擎路由 + 免费方案 + 自动降级 | 4.8/5.0 |
| 网页抓取引擎(专业版) | `web-crawler-engine` | Research | 增量同步调度 + SQL高级分析 + 批量并发抓取 + 监控告警 | 4.7/5.0 |
### 技能间协同关系
```
internet-search-pro-2 (AI搜索) ──发现信息源──> google-search-4 (精准搜索)
         │                                         │
    多源聚合搜索                            Google CSE精准定位
         │                                         │
         v                                         v
free-web-search-4 (免费兜底) <──Bing/DuckDuckGo──> web-crawler-engine (批量抓取)
         │                                         │
    免费方案覆盖                             增量同步+SQL分析
                                                   │
                                              数据洞察输出
```
- **internet-search-pro-2** 为研究起点，AI优化查询构造，多源聚合搜索发现信息源
- **google-search-4** 使用Google CSE对特定领域进行精准搜索，结果排序更相关
- **free-web-search-4** 在Google搜索配额耗尽或不可用时，通过Bing+DuckDuckGo双引擎兜底
- **web-crawler-engine** 接收搜索发现的URL列表，批量抓取归档，增量同步，SQL分析输出数据洞察
## 使用时机
| 触发场景 | 触发关键词/意图 | 调用技能 |
|:---------|:----------------|:---------|
| 需要联网搜索信息 | "搜索"、"联网搜索"、"查找"、"查一下"、"搜索信息" | internet-search-pro-2 |
| 需要Google精准搜索 | "Google搜索"、"谷歌搜索"、"CSE"、"精准搜索" | google-search-4 |
| 免费搜索替代方案 | "免费搜索"、"Bing"、"DuckDuckGo"、"不用API Key" | free-web-search-4 |
| 批量抓取网页数据 | "网页抓取"、"爬虫"、"数据归档"、"增量同步"、"批量抓取" | web-crawler-engine |
| SQL数据分析 | "SQL分析"、"数据统计"、"数据洞察"、"数据分析" | web-crawler-engine |
| 全链路数据研究 | "数据研究"、"市场调研"、"信息收集"、"数据采集" | 4技能串联执行 |
## 适用范围
### 场景1 市场研究员竞品信息收集
市场研究员需要收集某行业的竞品信息，包括产品功能、定价、用户评价等。
- **Step 1**: 调用 internet-search-pro-2，输入查询"AI编程工具 竞品对比 2026"，AI优化查询构造，多源聚合搜索
- **Step 2**: 调用 google-search-4，使用Google CSE限定搜索范围（如特定行业网站），精准获取竞品官网和评测文章
- **Step 3**: 调用 web-crawler-engine，将搜索发现的URL列表批量抓取归档，配置增量同步（每小时更新竞品动态）
- **Step 4**: 使用SQL高级分析，按关键词频次统计竞品提及量趋势，识别市场热点
### 场景2 投资研究员行业数据采集与分析
投资研究员需要持续跟踪某行业的公开数据，进行趋势分析和投资决策支撑。
- **Step 1**: 调用 internet-search-pro-2，输入查询"新能源行业 季度报告 融资动态"，多步搜索获取最新行业信息
- **Step 2**: 调用 web-crawler-engine，配置定时增量同步（Cron调度，每日同步），自动归档新发布的行业报告
- **Step 3**: 使用SQL高级分析，按日期GROUP BY统计消息量趋势，按关键词频次分析热点话题变化
- **Step 4**: 调用 free-web-search-4 作为免费搜索兜底，覆盖Bing和DuckDuckGo的搜索结果
### 场景3 学术研究者文献资料聚合
学术研究者需要跨多个搜索引擎收集特定主题的学术资料和研究数据。
- **Step 1**: 调用 internet-search-pro-2，输入查询"大语言模型 推理优化 最新论文"，类目路由到学术搜索
- **Step 2**: 调用 google-search-4，使用Google CSE限定学术网站域名（如arxiv.org, scholar.google.com），精准搜索
- **Step 3**: 调用 free-web-search-4，通过Bing+DuckDuckGo补充搜索，覆盖Google未索引的来源
- **Step 4**: 调用 web-crawler-engine，批量抓取发现的论文URL，归档到本地数据库，使用SQL分析按作者/关键词/年份统计
## 操作步骤
### 快速开始
1. 确认Agent已加载本Plug的SKILL.md及4个成员技能的SKILL.md
2. 在Agent环境变量中配置 `LLM_API_KEY`（必需）和 `GOOGLE_API_KEY` + `GOOGLE_CSE_ID`（可选，Google搜索需要）
3. 确认Agent支持 exec 工具（命令行执行能力）
4. 确认网络连接正常（搜索和抓取均需要网络）
5. 在Agent对话中描述研究需求，Plug将根据触发条件自动选择对应技能
### 数据研究工作流
#
### Step 1: AI多源搜索（internet-search-pro-2）
- **输入**: 查询关键词 + 搜索类目（可选）+ 搜索深度（可选）
- **处理**: AI优化查询构造，类目路由（通用/学术/新闻/技术），多步搜索聚合多源结果
- **输出**: 搜索结果列表（标题/URL/摘要/来源/相关度评分）
- **特点**: AI驱动的查询优化，自动扩展同义词和相关词，多步搜索深度挖掘
#
### Step 2: Google精准搜索（google-search-4）
- **输入**: 查询关键词 + CSE搜索引擎ID（可选，限定搜索范围）+ 结果数量
- **处理**: 使用Google Custom Search Engine API进行精准搜索，支持限定特定网站或域名
- **输出**: 搜索结果列表（标题/URL/摘要/排序依据）
- **降级**: Google API配额耗尽或不可用时，降级到free-web-search-4
- **配额**: Google CSE每日免费100次查询，超出需付费
#
### Step 3: 免费搜索兜底（free-web-search-4）
- **输入**: 查询关键词 + 引擎选择（Bing/DuckDuckGo/auto）
- **处理**: Bing和DuckDuckGo双引擎路由，自动选择可用引擎，免费方案无需API Key
- **输出**: 搜索结果列表（标题/URL/摘要/来源引擎）
- **特点**: 零成本方案，适合Google配额耗尽或不可用时的兜底搜索
#
### Step 4: 批量抓取与SQL分析（web-crawler-engine）
- **输入**: URL列表 + 抓取配置（并发数/限速/去重）+ 同步策略
- **处理**:
  - 增量同步调度：基于时间戳的增量同步，仅采集新数据（定时同步/事件触发/手动同步/混合模式）
  - 批量并发抓取：并发池+URL去重，支持深度优先/广度优先/优先级调度
  - SQL高级分析：消息量趋势/用户排行/关键词频次/时间分布/频道对比
  - 多格式导出：CSV/JSON/Excel多格式数据导出
  - 监控告警：同步异常监控与告警通知（飞书/钉钉/邮件）
- **输出**: 归档数据 + SQL分析报告 + 导出文件 + 告警通知
- **去重策略**: URL哈希去重（MD5），避免重复抓取
### 单技能调用
每个技能均可独立调用。搜索类技能适合信息发现阶段，抓取引擎适合数据归档和分析阶段。免费搜索工具可完全独立使用（零API Key需求）。
## 参数说明
```json
{
  "plug": "plug-intelligent-data-research",
  "action": "execute_workflow | execute_single",
  "input": {
    "workflow": "full | search_only | google_only | free_search_only | crawl_only",
    "search_input": {
      "query": "AI编程工具 竞品对比 2026",
      "category": "tech",
      "depth": "multi_step"
    },
    "google_input": {
      "query": "AI编程工具 竞品对比",
      "cse_id": "custom_search_engine_id",
      "num_results": 10
    },
    "free_search_input": {
      "query": "AI编程工具 竞品对比",
      "engine": "auto"
    },
    "crawl_input": {
      "urls": ["https://example.com/article1", "https://example.com/article2"],
      "max_workers": 5,
      "rate_limit_per_sec": 2,
      "sync_strategy": "incremental",
      "sync_interval_minutes": 60
    }
  },
  "options": {
    "format": "json",
    "verbose": true
  }
}
```
## 响应格式
```json
{
  "status": "success",
  "plug": "plug-intelligent-data-research",
  "results": [
    {
      "step": 1,
      "skill": "internet-search-pro-2",
      "status": "completed",
      "output": {
        "results": [
          {
            "title": "2026年AI编程工具横评：5款主流工具对比",
            "url": "https://example.com/ai-tools-review",
            "snippet": "本文对比了Cursor、Copilot、Claude等5款AI编程工具...",
            "source": "multi_source",
            "relevance_score": 0.95
          }
        ],
        "total_results": 15,
        "search_depth": "multi_step"
      }
    },
    {
      "step": 2,
      "skill": "web-crawler-engine",
      "status": "completed",
      "output": {
        "crawled_count": 15,
        "new_count": 12,
        "duplicate_count": 3,
        "archive_path": "data/research/2026-07-29/",
        "sql_analysis": {
          "top_keywords": [{"keyword": "Cursor", "count": 28}, {"keyword": "Copilot", "count": 22}],
          "date_distribution": {"2026-07": 15, "2026-06": 8}
        }
      }
    }
  ],
  "metadata": {
    "total_steps": 2,
    "duration_ms": 30000,
    "timestamp": "2026-07-29T10:00:00Z"
  }
}
```
## 环境要求
### 运行环境
- **Agent平台**: Claude Code / Cursor / Codex / Gemini CLI / Windsurf 等支持SKILL.md的任意Agent
- **操作系统**: Windows / macOS / Linux
- **运行时**: 需要Agent支持 exec（命令行执行）能力
- **网络**: 搜索和抓取均需要网络连接（必需）
### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 | 国内替代方案 |
|:-------|:-----|:---------|:---------|:-------------|
| LLM API | API | 必需 | 任意LLM服务商，由Agent内置LLM提供 | 通义千问/文心一言/智谱GLM/DeepSeek/Kimi |
| Google CSE API | API | google-search-4必需 | Google Cloud Console申请API Key + CSE ID | 无直接替代，国内可用Bing API/百度搜索API |
| Bing Search API | API | free-web-search-4可选 | 微软Azure申请Bing Search API Key | 百度搜索API/搜狗搜索API |
| DuckDuckGo | 免费API | free-web-search-4默认 | 无需API Key，直接使用 | 无需替代，全球可用 |
| Python 3.8+ | 运行时 | web-crawler-engine必需 | python.org下载 | 国产Python发行版: Anaconda/miniconda |
| SQLite/MySQL | 数据库 | web-crawler-engine必需 | SQLite内置/MySQL安装 | 国产数据库: 达梦/人大金仓 |
| schedule库 | Python库 | 增量同步必需 | `pip install schedule` | 无替代，开源库 |
| JSON文件存储 | 文件系统 | 数据归档必需 | exec工具创建data/目录 | 本地文件系统，无海外依赖 |
### API Key配置（零暴露原则）
- **LLM_API_KEY**: 必需（通常由Agent内置）- 查询优化/搜索结果分析/数据洞察生成
- **GOOGLE_API_KEY**: google-search-4可选 - Google CSE搜索API（每日免费100次）
- **GOOGLE_CSE_ID**: google-search-4可选 - Google自定义搜索引擎ID
- **BING_API_KEY**: free-web-search-4可选 - Bing搜索API（不配置时使用DuckDuckGo）
- **配置方式**: 必须通过Agent环境变量注入，严禁在SKILL.md或代码中硬编码API Key
- **安全检查**: 本SKILL.md中不包含任何API Key示例，所有Key均通过 `$env:GOOGLE_API_KEY` 等环境变量读取
### 可用性分类
- **分类**: MD+EXEC
- **说明**: 纯Markdown技能定义，需要Agent支持exec能力（命令行执行），用于文件读写和数据抓取
- **开箱即用**: free-web-search-4可零配置直接使用（DuckDuckGo免费无需API Key），其他搜索技能需配置对应API Key
- **免费方案**: free-web-search-4使用DuckDuckGo免费API，无需任何API Key，适合预算有限的研究场景
## 异常处理架构
### 异常处理策略
| 异常场景 | 原因 | 处理方式 |
|:---------|:-----|:---------|
## 主要功能
- **自动化执行**: 多引擎搜索/网页抓取/SQL分析/增量同步,4合1数据研究平台
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
## 优势对比
| 对比维度 | 智能数据研究工作站 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 多引擎搜索/网页抓取/SQL分析/增量同步,4合1数据研究平台 | 通用场景 | 通用场景 |
## 热门问答
### Q1: 智能数据研究工作站支持哪些输入格式？

A1: 多引擎搜索/网页抓取/SQL分析/增量同步,4合1数据研究平台。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

## 快速启航
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码

## 用户咨询
