---
name: nlp-api-hub
description: NLP与语言数据API枢纽 — 整合自然语言处理模型/评估/语料。数据集: HuggingFace(模型)/GLUE(理解评估)/SQuAD(QA)/FLORES(翻译200+语言)/FineWeb(网页文本)/C4(Common Crawl)/The Pile(开源LLM训练)/MMLU(多任务语言理解)。注意数据合规性(用户需确保不侵犯版权/内容审查)。
author: ai-gaoqian
version: 1.0.0
---

# NLP与语言数据API枢纽

整合NLP模型、评估与语料。

## 数据集

### 1. HuggingFace模型
HuggingFace Hub开放模型>50万。含BERT/GPT/LLaMA/Whisper/T5/StableDiff/Diffusion/语音/视觉/多模态。API端点：/api/hf/model→get用model_id→获取card/config/weights。调用需密钥(HF_TOKEN)。

### 2. GLUE理解评估
通用语言理解评估(GLUE)9项任务：CoLA/MNLI/MRPC/QNLI/QQP/RTE/SST-2/STS-B/WNLI。API端点：/api/glue/evaluate→get用model_name/task。

### 3. SQuAD问答
Stanford QA数据集v2(100k+问答对)。含原文+问题+答案。API端点：/api/squad/qa→get用context/question。输出答案。

### 4. FLORES翻译200+语言
Meta FLORES-200翻译基准3003 lang对。支持178+语言翻译，含低资源语言。API端点：/api/flores/translate→get用source_lang/target_lang/text。

### 5. FineWeb网页文本
HuggingFace FineWeb训练语料(15T tokens)。过滤/去重/高质量网页文本。可提取按语言、主题、质量的子集。API端点：/api/fineweb/extract→get用language/topic/content_query。

### 6. C4语料
Common Crawl Cleaned Common Crawl 约>300GB英文。含网页文本，广泛应用于语言模型预训练。API端点：/api/c4/search→get用domain/topic/content_query。

### 7. The Pile训练语料
The Pile-800GB开源大模型预训练语料。含22个多样化子集(书籍/代码/论文/对话/维基/新闻报道等)。API端点：/api/thepile/extract→get用subset/content_query。

### 8. MMLU多任务语言理解
多项选择评测基准57个科目(STEM/社科/人文/其他)。API端点：/api/mmlu/evaluate→get用model/subject→返回准确率。

## 使用方式
"法语翻译成中文，用FLORES"。"BERT在GLUE各任务上表现如何？"
