# Phase 1：规划师完整 prompt 模板

## 执行步骤

1. 加载 `F:/agent/chapters/reference_material.txt` 摘要（前3000字）作为 `reference_summary`
2. 将以下模板中 `{xxx}` 替换为实际值
3. 将输出写入 `F:/agent/chapters/plan.json`

## Prompt 模板

```
你是专业项目规划师。用户需要撰写一份【{doc_type}】，主题是「{topic}」。

## 用户提供的背景信息
{background}

## 参考资料摘要（优先参考）
{reference_summary}

请完成以下任务：
1. 制定详细的文档大纲（到三级标题）
2. 为每个章节标注核心撰写要点
3. 识别每个章节RAG检索关键词（≤3个/章）
4. 评估各章节的预期复杂度，标注重点章节
5. 识别章节依赖关系（哪些章节需在前序章节完成后才能撰写）

**章节依赖关系规则**：
- 第1类（无依赖，可最先写）：概述、背景、现状分析、技术选型
- 第2类（依赖第1类）：总体设计、详细功能设计
- 第3类（依赖前面若干章）：实施计划、测试方案、部署方案
- 第4类（可独立写，也可最后写）：培训方案、验收方案、附件、结论

## 参考资料禁止混入的内容
请在规划时主动排除与主题无关的内容（如输液监控系统等）。

请将以下结构化信息写入 F:/agent/chapters/plan.json：
{
  "project_name": "项目名称",
  "doc_type": "文档类型",
  "chapters": [
    {
      "seq": "01",
      "title": "章节标题",
      "brief": "撰写要点",
      "feishu_keywords": ["k1", "k2"],
      "web_keywords": ["k1", "k2"],
      "word_count": 3000,
      "batch": "A",
      "dependencies": [],
      "status": "pending"
    }
  ]
}
```

## plan.json 字段说明

| 字段 | 说明 |
|------|------|
| `seq` | 章节序号，2位数字字符串（"01", "02"） |
| `title` | 章节标题 |
| `brief` | 核心撰写要点（50-100字） |
| `feishu_keywords` | 飞书知识库检索关键词，最多3个 |
| `web_keywords` | 网络检索关键词，最多3个 |
| `word_count` | 目标字数（正文字数，不含标题） |
| `batch` | 批次标签（"A"/"B"/"C"，同批次可并行撰写） |
| `dependencies` | 依赖章节 seq 列表，如 `["01", "02"]` |
| `status` | 状态：`pending`/`writing`/`txt_done`/`confirmed` |

## 执行后操作

```bash
# 1. 生成初始术语表（从参考资料提取）
python integrate_report.py glossary

# 2. 保存大纲快照
python integrate_report.py save-outline

# 3. 展示大纲给用户确认
```
