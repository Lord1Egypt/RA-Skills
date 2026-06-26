# OpenClaw Skill 注册表

> 技能组合器的技能索引库 — 列出所有可用技能及其适用场景

---

## 📋 总览

| 分类 | 技能数 | 主要用途 |
|------|--------|----------|
| 内容创作 | 7 | 文章写作、公众号、PPT |
| 信息采集 | 5 | 网页抓取、搜索、爬虫 |
| 媒体处理 | 3 | 视频帧提取、分析 |
| 文档处理 | 5 | PDF、epub、格式转换 |
| 投资分析 | 5 | 股票、加密货币、组合管理 |
| 思维工具 | 3 | 思考框架、决策工具 |
| 技能进化 | 6 | 创建、审查、优化 |
| 知识管理 | 2 | Wiki、笔记整理 |
| 协同工具 | 4 | 场景SOP、质量评估 |
| **总计** | **40** | |

---

## 📝 内容创作类（7）

### 1. writer
```yaml
name: writer
description: 通用写作能力，处理各类文本生成任务
category: content_creation
skills:
  - 文本生成
  - 内容改写
  - 风格调整
trigger_keywords:
  - "写一段"
  - "帮我写"
  - "改写"
output_format:
  result_field: "text"
  word_count_field: "word_count"
compatible_with:
  - web-content-fetcher
  - multi-search-engine
  - wechat-mp-upload
```

### 2. writing-agent
```yaml
name: writing-agent
description: AI写作助手，专注文章创作与优化
category: content_creation
skills:
  - 深度文章创作
  - 结构化写作
  - 内容优化
  - 风格定制
trigger_keywords:
  - "写文章"
  - "创作内容"
  - "深度写作"
output_format:
  result_field: "article_text"
  word_count_field: "word_count"
  tone_field: "tone"
compatible_with:
  - web-content-fetcher
  - epub-to-markdown
  - wechat-mp-upload
```

### 3. content-creator
```yaml
name: content-creator
description: 内容创建器，支持多类型内容生成
category: content_creation
skills:
  - 多形式内容
  - 标题生成
  - 摘要提取
trigger_keywords:
  - "创建内容"
  - "生成内容"
  - "多形式内容"
output_format:
  result_field: "content"
  type_field: "content_type"
compatible_with:
  - multi-search-engine
  - writing-agent
```

### 4. article-writing
```yaml
name: article-writing
description: 专门的文章写作技能
category: content_creation
skills:
  - 长文章撰写
  - 专业技术文章
  - 教程编写
trigger_keywords:
  - "写长文"
  - "专业技术"
  - "教程"
output_format:
  result_field: "article"
  sections_field: "sections"
compatible_with:
  - pdf-extractor
  - web-content-fetcher
```

### 5. wechat-article-creator
```yaml
name: wechat-article-creator
description: 微信公众号文章创作
category: content_creation
skills:
  - 公众号风格
  - 互动引导
  - 排版优化
trigger_keywords:
  - "公众号文章"
  - "微信文章"
  - "公众号风格"
output_format:
  result_field: "wechat_article"
  html_field: "html_content"
compatible_with:
  - writing-agent
  - web-content-fetcher
```

### 6. wechat-mp-upload
```yaml
name: wechat-mp-upload
description: 微信公众号内容上传与排版
category: content_creation
skills:
  - HTML排版
  - 图片上传
  - 封面设置
  - 发布管理
trigger_keywords:
  - "上传到公众号"
  - "微信发布"
  - "排版"
output_format:
  result_field: "formatted_content"
  publish_field: "publish_result"
compatible_with:
  - writing-agent
  - article-writing
```

### 7. jackyshen-write-wechat-article
```yaml
name: jackyshen-write-wechat-article
description: 特定风格的微信公众号写作
category: content_creation
skills:
  - 特定作者风格
  - 深度分析
trigger_keywords:
  - "jackyshen风格"
output_format:
  result_field: "article"
compatible_with:
  - web-content-fetcher
```

---

## 🔍 信息采集类（5）

### 8. web-content-fetcher
```yaml
name: web-content-fetcher
description: 网页内容抓取，支持URL/关键词
category: information_gathering
skills:
  - 网页抓取
  - 内容提取
  - 去广告/标准化
trigger_keywords:
  - "抓取网页"
  - "获取内容"
  - "采集素材"
output_format:
  result_field: "content"
  url_field: "source_url"
  title_field: "title"
compatible_with:
  - writing-agent
  - content-creator
  - epub-to-markdown
```

### 9. multi-search-engine
```yaml
name: multi-search-engine
description: 多引擎搜索，聚合多源结果
category: information_gathering
skills:
  - 多引擎并行搜索
  - 结果去重/排序
  - 摘要提取
trigger_keywords:
  - "搜索"
  - "查一下"
  - "多引擎"
output_format:
  result_field: "search_results"
  count_field: "result_count"
compatible_with:
  - writing-agent
  - investment-agent
  - content-creator
```

### 10. playwright-scraper-skill
```yaml
name: playwright-scraper-skill
description: 浏览器级爬虫，处理动态网页
category: information_gathering
skills:
  - JavaScript渲染页面抓取
  - 登录态抓取
  - 复杂交互页面
trigger_keywords:
  - "动态网页"
  - "需要登录"
  - "复杂页面"
fallback_for: web-content-fetcher
output_format:
  result_field: "content"
  html_field: "raw_html"
compatible_with:
  - writing-agent
```

### 11. agent-reach
```yaml
name: agent-reach
description: 全网搜索能力
category: information_gathering
skills:
  - 全网深度搜索
  - 信息聚合
trigger_keywords:
  - "全网搜索"
  - "深度搜索"
output_format:
  result_field: "results"
compatible_with:
  - writing-agent
  - investment-agent
```

### 12. clawhub
```yaml
name: clawhub
description: Skill市场搜索与安装
category: information_gathering
skills:
  - Skill搜索
  - 安装管理
  - 版本控制
trigger_keywords:
  - "搜索skill"
  - "安装技能"
  - "找工具"
output_format:
  result_field: "skill_info"
  install_field: "install_status"
```

---

## 🎬 媒体处理类（3）

### 13. video-frames
```yaml
name: video-frames
description: 视频帧提取，支持关键帧识别
category: media_processing
skills:
  - 帧提取
  - 关键帧识别
  - 时间戳标注
trigger_keywords:
  - "提取视频帧"
  - "视频截图"
  - "关键帧"
output_format:
  result_field: "frames"
  timestamp_field: "timestamps"
compatible_with:
  - analyze_video
  - writing-agent
```

### 14. analyze_video
```yaml
name: analyze_video
description: AI视频内容分析
category: media_processing
skills:
  - 内容理解
  - 场景描述
  - 关键片段提取
trigger_keywords:
  - "分析视频"
  - "视频内容"
  - "视频拆解"
output_format:
  result_field: "analysis"
  key_moments_field: "key_moments"
compatible_with:
  - video-frames
  - writing-agent
  - investment-agent
```

### 15. video-frames-skill (同 video-frames)
```yaml
name: video-frames-skill
description: 视频帧提取技能（完整版）
category: media_processing
skills:
  - 批量帧提取
  - 场景切分
  - 质量评估
trigger_keywords:
  - "批量提取帧"
  - "视频分段"
output_format:
  result_field: "frames_batch"
  scenes_field: "scenes"
```

---

## 📄 文档处理类（5）

### 16. pdf-extractor
```yaml
name: pdf-extractor
description: PDF文档内容提取
category: document_processing
skills:
  - 文本提取
  - 结构化
  - 表格识别
trigger_keywords:
  - "提取PDF"
  - "PDF内容"
  - "解析PDF"
output_format:
  result_field: "content"
  page_count_field: "page_count"
compatible_with:
  - writing-agent
  - epub-to-markdown
  - content-creator
```

### 17. epub-read
```yaml
name: epub-read
description: 电子书阅读与内容提取
category: document_processing
skills:
  - epub解析
  - 章节提取
  - 元数据读取
trigger_keywords:
  - "读电子书"
  - "epub内容"
  - "电子书解析"
output_format:
  result_field: "content"
  chapters_field: "chapters"
compatible_with:
  - writing-agent
  - epub-to-markdown
```

### 18. epub-to-markdown
```yaml
name: epub-to-markdown
description: 格式转换工具，支持多格式转Markdown
category: document_processing
skills:
  - 格式转换
  - Markdown生成
  - 目录结构保持
trigger_keywords:
  - "转markdown"
  - "格式转换"
  - "生成md"
output_format:
  result_field: "markdown"
  file_path_field: "output_path"
also_used_for:
  - wiki生成
  - 知识库整理
compatible_with:
  - pdf-extractor
  - epub-read
```

### 19. ocr-local
```yaml
name: ocr-local
description: 本地图片OCR识别
category: document_processing
skills:
  - 图片文字识别
  - 表格OCR
  - 手写识别
trigger_keywords:
  - "图片转文字"
  - "OCR"
  - "识别文字"
output_format:
  result_field: "text"
  confidence_field: "ocr_confidence"
```

### 20. pdf-extractor (同16)
```yaml
name: pdf-extractor
description: PDF提取（完整版）
category: document_processing
skills:
  - 深度PDF解析
  - 图表提取
  - 元数据提取
trigger_keywords:
  - "深度解析PDF"
  - "PDF图表"
output_format:
  result_field: "full_content"
  charts_field: "charts"
```

---

## 💰 投资分析类（5）

### 21. investment-agent
```yaml
name: investment-agent
description: AI投资分析师
category: investment_analysis
skills:
  - 市场分析
  - 趋势判断
  - 标的研究
trigger_keywords:
  - "分析投资"
  - "股票分析"
  - "市场研究"
output_format:
  result_field: "analysis_report"
  recommendation_field: "recommendation"
compatible_with:
  - multi-search-engine
  - investment-portfolio
  - analyze_video
```

### 22. investment-analysis-kit
```yaml
name: investment-analysis-kit
description: 投资分析工具包
category: investment_analysis
skills:
  - 财务数据处理
  - 指标计算
  - 报表生成
trigger_keywords:
  - "投资工具"
  - "财务分析"
  - "指标计算"
output_format:
  result_field: "analysis_data"
  metrics_field: "financial_metrics"
compatible_with:
  - investment-agent
  - investment-portfolio
```

### 23. investment-portfolio
```yaml
name: investment-portfolio
description: 投资组合管理
category: investment_analysis
skills:
  - 持仓管理
  - 风险评估
  - 再平衡建议
trigger_keywords:
  - "组合管理"
  - "持仓分析"
  - "风险评估"
output_format:
  result_field: "portfolio_status"
  risk_field: "risk_metrics"
compatible_with:
  - investment-agent
  - multi-search-engine
```

### 24. crypto-investment-strategist
```yaml
name: crypto-investment-strategist
description: 加密货币投资策略
category: investment_analysis
skills:
  - 加密货币分析
  - 链上数据分析
  - DeFi策略
trigger_keywords:
  - "加密货币"
  - "数字货币"
  - "Crypto"
output_format:
  result_field: "crypto_strategy"
  signals_field: "trading_signals"
compatible_with:
  - multi-search-engine
  - investment-portfolio
```

### 25. eastmoney_financial_search
```yaml
name: eastmoney_financial_search
description: 东方财富网金融数据查询
category: investment_analysis
skills:
  - A股数据
  - 基金数据
  - 财报查询
trigger_keywords:
  - "东方财富"
  - "A股"
  - "基金"
output_format:
  result_field: "financial_data"
  stock_field: "stock_info"
```

---

## 🧠 思维工具类（3）

### 26. thinking-toolbox
```yaml
name: thinking-toolbox
description: 思维工具箱，多种思考框架
category: thinking_tools
skills:
  - 第一性原理分析
  - 奥卡姆剃刀
  - 系统思维
  - 决策框架
trigger_keywords:
  - "思考框架"
  - "分析问题"
  - "系统思维"
output_format:
  result_field: "analysis"
  framework_field: "applied_framework"
```

### 27. decision-journal
```yaml
name: decision-journal
description: 决策日志与复盘
category: thinking_tools
skills:
  - 决策记录
  - 结果追踪
  - 复盘分析
trigger_keywords:
  - "记录决策"
  - "决策复盘"
  - "决策追踪"
output_format:
  result_field: "decision_record"
  outcome_field: "outcome"
```

### 28. munger-decision-free
```yaml
name: munger-decision-free
description: 芒格决策模型应用
category: thinking_tools
skills:
  - 多学科模型
  - 逆向思考
  - 误判分析
trigger_keywords:
  - "芒格"
  - "多学科模型"
  - "误判"
output_format:
  result_field: "multi_model_analysis"
  inverse_field: "inverse_analysis"
```

---

## 🔧 技能进化类（6）

### 29. skill-self-evolution-enhancer
```yaml
name: skill-self-evolution-enhancer
description: Skill自进化增强器
category: skill_evolution
skills:
  - 问题分析
  - 最佳实践匹配
  - 版本生成
  - 验证测试
trigger_keywords:
  - "自进化"
  - "优化skill"
  - "技能改进"
  - "修复skill"
output_format:
  result_field: "improved_skill"
  diff_field: "diff_report"
compatible_with:
  - skill-builder
  - skill-vetter
```

### 30. skill-builder
```yaml
name: skill-builder
description: 技能构建器
category: skill_evolution
skills:
  - SKILL.md生成
  - CHAIN.md设计
  - 目录结构创建
trigger_keywords:
  - "创建skill"
  - "构建技能"
  - "新建技能"
output_format:
  result_field: "skill_files"
  path_field: "skill_path"
```

### 31. skill-vetter
```yaml
name: skill-vetter
description: 技能审查器
category: skill_evolution
skills:
  - 质量审查
  - 标准检查
  - 改进建议
trigger_keywords:
  - "审查技能"
  - "质量检查"
  - "技能评审"
output_format:
  result_field: "vet_report"
  issues_field: "issues_found"
```

### 32. skill-health-monitor
```yaml
name: skill-health-monitor
description: 技能健康巡检
category: skill_evolution
skills:
  - 健康度评分
  - 问题诊断
  - 修复建议
trigger_keywords:
  - "巡检"
  - "健康检查"
  - "技能诊断"
output_format:
  result_field: "health_report"
  score_field: "health_score"
```

### 33. skill-self-evolution-enhancer (同29)
```yaml
name: skill-self-evolution-enhancer
description: 技能自进化增强器（完整版）
category: skill_evolution
skills:
  - 深度分析
  - 版本控制
  - 增量优化
trigger_keywords:
  - "自进化流水线"
  - "深度优化"
output_format:
  result_field: "evolution_result"
  version_field: "new_version"
```

### 34. newman
```yaml
name: newman
description: API测试与文档生成
category: skill_evolution
skills:
  - Postman集合运行
  - API测试
  - 文档生成
trigger_keywords:
  - "API测试"
  - "newman"
  - "接口测试"
output_format:
  result_field: "test_results"
  report_field: "test_report"
```

---

## 📚 知识管理类（2）

### 35. epub-to-markdown (重载)
```yaml
name: epub-to-markdown
description: 知识整理与Wiki生成
category: knowledge_management
skills:
  - Wiki格式生成
  - 索引更新
  - 概念图谱
used_for:
  - article-to-wiki流水线
  - 知识沉淀
trigger_keywords:
  - "转wiki"
  - "知识库"
  - "沉淀"
output_format:
  result_field: "wiki_content"
  index_field: "index_update"
```

### 36. context-refine
```yaml
name: context-refine
description: 上下文完善技能
category: knowledge_management
skills:
  - 上下文补全
  - 意图识别
  - 信息完善
trigger_keywords:
  - "完善上下文"
  - "补充信息"
output_format:
  result_field: "refined_context"
```

---

## 🔗 协同工具类（4）

### 37. scenario-sop
```yaml
name: scenario-sop
description: 场景SOP技能库
category: collaborative_tools
skills:
  - 场景匹配
  - SOP执行
  - 流程自动化
trigger_keywords:
  - "SOP"
  - "标准流程"
  - "场景执行"
output_format:
  result_field: "sop_result"
  matched_field: "matched_sop"
```

### 38. sentinel-qa
```yaml
name: sentinel-qa
description: 质量评估与验收
category: collaborative_tools
skills:
  - 质量检查
  - 验收测试
  - 问题发现
trigger_keywords:
  - "质量检查"
  - "QA"
  - "验收"
output_format:
  result_field: "qa_report"
  issues_field: "issues"
```

### 39. evaluate-skills
```yaml
name: evaluate-skills
description: 技能评估工具
category: collaborative_tools
skills:
  - 技能评分
  - 对比分析
  - 推荐排序
trigger_keywords:
  - "评估技能"
  - "技能对比"
  - "选择技能"
output_format:
  result_field: "evaluation"
  scores_field: "skill_scores"
```

### 40. pending-auto-rescue
```yaml
name: pending-auto-rescue
description: 待处理任务自动救援
category: collaborative_tools
skills:
  - 任务恢复
  - 死链检测
  - 自动修复
trigger_keywords:
  - "任务卡住"
  - "恢复任务"
  - "死链"
output_format:
  result_field: "rescue_result"
  fixed_field: "fixed_items"
```

---

## 🎯 技能组合推荐

### 常见场景 → 技能组合

| 场景 | 推荐技能链 |
|------|-----------|
| **文章创作** | web-content-fetcher → writing-agent → wechat-mp-upload |
| **研究报告** | multi-search-engine → writing-agent → content-creator |
| **视频笔记** | video-frames → analyze_video → writing-agent |
| **投资分析** | multi-search-engine → investment-agent → investment-portfolio |
| **PDF摘要** | pdf-extractor → writing-agent → epub-to-markdown |
| **Skill优化** | skill-self-evolution-enhancer (5步流水线) |
| **文章转Wiki** | web-content-fetcher → writing-agent → epub-to-markdown |
| **Get笔记转文章** | web-content-fetcher → writing-agent × 3 → wechat-mp-upload |

---

## 🔍 技能查找指南

### 按用途查找

| 需求 | 推荐技能 |
|------|----------|
| 写文章/内容创作 | writer, writing-agent, content-creator |
| 抓取网页/搜索 | web-content-fetcher, multi-search-engine, playwright-scraper-skill |
| 视频处理 | video-frames, analyze_video |
| PDF/文档处理 | pdf-extractor, epub-read, epub-to-markdown |
| 投资相关 | investment-agent, investment-analysis-kit, investment-portfolio, crypto-investment-strategist, eastmoney_financial_search |
| 思考/决策 | thinking-toolbox, decision-journal, munger-decision-free |
| 技能开发/优化 | skill-builder, skill-vetter, skill-self-evolution-enhancer |
| 知识管理 | epub-to-markdown, context-refine |
| 质量保证 | sentinel-qa, evaluate-skills |

### 按输入类型查找

| 输入 | 推荐技能 |
|------|----------|
| URL/网页 | web-content-fetcher, playwright-scraper-skill |
| 关键词/搜索 | multi-search-engine, agent-reach |
| 视频文件 | video-frames, analyze_video |
| PDF文件 | pdf-extractor |
| 电子书 | epub-read, epub-to-markdown |
| 图片 | ocr-local |
| Get笔记链接 | web-content-fetcher |

---

## 📊 统计信息

- **注册技能总数**: 40
- **覆盖领域**: 10
- **模板支持**: 7
- **最后更新**: 2026-05-01