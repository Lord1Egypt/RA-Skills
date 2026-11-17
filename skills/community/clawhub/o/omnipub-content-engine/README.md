# omnipub-content-engine

> 全平台内容同步发布引擎 — 从选题到复盘的 AI 驱动闭环

## 这是什么

一个 AI 驱动的内容生命周期管理技能，覆盖 10 个阶段：**选题讨论 → 内容生成 → 数据查证 → 图表设计 → 文末模板 → 风格选择 → AI信息图 → GEO优化 → 多平台发布 → 数据复盘**。

与市面工具（融媒宝、易撰等侧重分发效率）不同，本技能的核心差异化在于：
- **Gate 制度**：人工把关不盲发，选题/初稿/文末/发布/复盘每个关键节点都需确认
- **GEO 闭环**：内容优化 + AI 可见度检查，让内容被 ChatGPT/Claude/Gemini 引用
- **数据归因**：4 类诊断树分析为什么没数据/有热度没浏览量，结论回流选题库
- **品牌一致**：禁用词检查 + 语调守卫 + 统一配色体系

## 支持平台

| 平台 | 方案 | 状态 |
|------|------|------|
| 微信公众号 | API 直推草稿箱 | 已实现 |
| 今日头条 | playwright 自动化 | 已实现 |

## 核心功能

- 3 套精选主题（品牌紫/极简灰/暖色人文）+ 主题画廊预览
- AI 信息图提示词生成（8 要素布局 + 4 引擎适配：即梦/LOVART/ChatGPT/Midjourney）
- GEO 就绪度检查器（7 项检查，满分 100）
- 数据复盘分析器（4 类归因诊断 + HTML 报告）
- 微信 CSS 兼容自动清洗（剥离 border-radius/box-shadow/gradient 等无效属性）
- 文末模板组装器（二维码/介绍/推荐阅读/CTA/签名）
- 数据源三源交叉验证

## 快速开始

1. 复制 `config.example.yaml` 为 `config.yaml`，填入品牌信息和平台凭据
2. 运行 `python scripts/cli.py themes` 查看可用主题
3. 运行 `python scripts/cli.py gallery` 预览主题效果
4. 运行 `python scripts/cli.py publish article.md --cover cover.png` 发布到公众号草稿箱

## CLI 命令一览

```
omnipub topic       选题搜索 + HCTFD 评分
omnipub fact-check   数据声明验证
omnipub infographic  AI 信息图提示词
omnipub footer       文末模板组装
omnipub geo-check    GEO 就绪度检查
omnipub convert      HTML 微信兼容转换
omnipub themes       主题列表
omnipub gallery      主题画廊预览
omnipub preview      单篇主题预览
omnipub publish      发布到公众号草稿箱
omnipub toutiao      头条发布准备
omnipub analytics    数据复盘分析
```

## 作者

心明增长实验室 — 16年大健康行业老兵，10年产品人，心明九力知识宇宙体系创始人
