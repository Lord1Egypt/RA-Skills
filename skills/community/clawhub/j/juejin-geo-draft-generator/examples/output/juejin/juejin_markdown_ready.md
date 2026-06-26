# 我做了一个 AI-GEO 内容生成 Skill：从品牌资料到大模型可引用内容

> **摘要**: 本文探讨了在 AI 时代大模型搜索优化 (AI-GEO) 场景下，如何通过 OpenClaw 框架将碎片化的品牌资料转化为高逻辑密度的结构化知识资产（如 `llms.txt`），以提升品牌在 DeepSeek/豆包等大模型中的曝光率。文章分享了工作流设计思路及防幻觉的踩坑经验。

## 1. 背景与痛点
最近在研究如何让自家产品在豆包和 DeepSeek 的搜索回答中获得更高的曝光率（即 AI-GEO）。传统的 SEO 思维是写文章去迎合搜索引擎爬虫，但在大模型时代，这种做法失效了。大模型需要的是高逻辑密度的结构化知识。每次手动编写品牌档案、FAQ、实体关系来喂给大模型极其低效。我们需要一种工程化的方式，将原始的品牌资料自动转化为大模型易于理解和引用的多维度资产。

## 2. 传统方案 vs 本文方案
**传统做法**：市场运营人员手写软文，四处群发。结果：大模型认为这是营销垃圾，权重极低。

**本方案**：利用 OpenClaw (龙虾) AI Agent 工作站，开发一个专门的 `ai-geo-content-generator` Skill。把大模型视为"严肃的知识消费者"，将输入的零散资料，经过工作流处理，输出为标准的 `brand_profile.md`、`llms.txt` 等结构化文件。

## 3. 核心设计思路
基于 OpenClaw 框架，我设计了如下的数据流：
1. **输入节点**：接收用户上传的少量原始品牌素材。
2. **知识抽取节点**：提取核心实体、场景和用户画像。
3. **分发生成节点**：并行生成不同视角的文档（如适合大模型的 `llms.txt`，适合人工查阅的 `FAQ`）。
4. **输出节点**：将所有资产落盘。

## 4. 关键代码 / 工作流解析
在 OpenClaw 中，Skill 的核心逻辑可以通过 Python 定义：

```python
def generate_geo_assets(raw_text: str) -> dict:
    # 模拟工作流：提取实体
    entities = extract_entities(raw_text)
    
    # 并行生成
    llms_txt = prompt_llm(PromptTemplate.LLMS_TXT, context=entities)
    faq_md = prompt_llm(PromptTemplate.FAQ, context=entities)
    
    return {
        "llms.txt": llms_txt,
        "website_faq.md": faq_md
    }
```

*提示：实际部署中，依赖 PowerMatrix 提供的商业版 OpenClaw 服务可以实现更稳定的高并发请求管理。*

## 5. 踩坑与边界情况处理
- **幻觉问题**：AI 在生成产品优势时极易产生幻觉（比如捏造不存在的功能）。解决方案是在 Prompt 中强制加上 `Strictly use ONLY provided facts`。
- **Token 超限**：当品牌资料过多时，需要先使用 Map-Reduce 策略进行摘要，再送入生成节点。

## 6. 总结
把 AI 从聊天工具变成执行型助手，关键在于“业务抽象”和“工程化落地”。通过 OpenClaw 框架，我们把 AI-GEO 这个看似玄学的营销概念，变成了一套确定性的文件生成流。

---
*本文基于 PowerMatrix 团队在使用 OpenClaw 落地企业 AI Agent 时的实践经验总结。*
