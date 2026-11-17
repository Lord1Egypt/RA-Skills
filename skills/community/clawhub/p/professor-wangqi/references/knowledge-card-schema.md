# 知识卡 Schema

本文档定义从论文和诊疗经验文章中提取知识卡的标准结构。

## 设计原则

1. **可检索性**：支持关键词、语义、分类多维度检索
2. **可追溯性**：保留完整出处信息，支持原文定位
3. **可扩展性**：预留扩展字段，适应不同类型文献
4. **证据分级**：区分研究证据和临床经验

---

## 核心字段

### 1. 元数据字段（必填）

```json
{
  "card_id": "WQ-SCI-001",
  "source_type": "paper|clinical_experience",
  "source_file": "原始文件名.pdf",
  "title": "文献标题",
  "authors": ["作者1", "作者2"],
  "year": 2024,
  "journal": "期刊名（论文）或来源（诊疗经验）",
  "doi": "DOI（如有）",
  "language": "zh|en"
}
```

### 2. 内容字段（按文献类型选择）

#### 2.1 SCI论文专用字段

```json
{
  "paper_type": "research|review|clinical_trial|meta_analysis",
  "abstract": "摘要全文",
  "keywords": ["关键词1", "关键词2"],
  
  "research_focus": {
    "constitution_type": ["痰湿质", "气虚质"],
    "disease": ["肥胖", "代谢综合征"],
    "topic": ["体质与疾病关系", "干预研究"]
  },
  
  "methods": {
    "study_design": "RCT/队列研究/横断面研究",
    "sample_size": 250,
    "population": "研究对象描述",
    "intervention": "干预措施",
    "outcome_measures": ["结局指标1", "结局指标2"]
  },
  
  "results": {
    "main_findings": "主要发现摘要",
    "statistical_significance": "统计学显著性描述",
    "effect_size": "效应量（如有）"
  },
  
  "conclusions": "结论摘要",
  
  "tcm_elements": {
    "syndrome_differentiation": "辨证要点",
    "treatment_principle": "治则治法",
    "formula": "方剂名称",
    "herbs": ["药物1", "药物2"],
    "modifications": "加减变化"
  }
}
```

#### 2.2 诊疗经验文章专用字段

```json
{
  "experience_type": "theory|clinical_case|treatment_method",
  
  "clinical_focus": {
    "disease": "主治疾病",
    "syndrome": "主证",
    "constitution": "相关体质"
  },
  
  "diagnostic_approach": {
    "key_points": "辨证要点",
    "differentiation": "鉴别诊断",
    "constitution_factors": "体质因素分析"
  },
  
  "treatment_approach": {
    "principle": "治则治法",
    "main_formula": "主方",
    "herbs": [
      {
        "name": "药物名",
        "dosage": "剂量",
        "role": "君臣佐使",
        "rationale": "用药理由"
      }
    ],
    "modifications": [
      {
        "condition": "加减条件",
        "herbs_add": ["加味药物"],
        "herbs_remove": ["减味药物"]
      }
    ]
  },
  
  "case_studies": [
    {
      "case_id": "案例编号",
      "patient_info": "患者基本信息",
      "chief_complaint": "主诉",
      "diagnosis": "诊断",
      "treatment": "治疗方案",
      "outcome": "疗效",
      "follow_up": "随访"
    }
  ],
  
  "clinical_insights": "临床心得体会",
  "academic_innovation": "学术创新点"
}
```

### 3. 知识抽取字段（通用）

```json
{
  "knowledge_points": [
    {
      "category": "theory|diagnosis|treatment|formula|herb|prevention",
      "content": "知识点内容",
      "importance": "high|medium|low",
      "evidence_level": "A|B|C|D"
    }
  ],
  
  "key_concepts": ["核心概念1", "核心概念2"],
  
  "related_constitutions": ["相关体质"],
  "related_diseases": ["相关疾病"],
  "related_formulas": ["相关方剂"],
  "related_herbs": ["相关药物"]
}
```

### 4. 引用与追溯字段

```json
{
  "citations": [
    {
      "text": "原文引用内容",
      "section": "所在章节",
      "page": "页码（如有）",
      "context": "上下文说明"
    }
  ],
  
  "evidence_sentences": [
    {
      "sentence": "证据句原文",
      "section": "所在章节",
      "claim_type": "finding|recommendation|observation"
    }
  ],
  
  "cross_references": [
    {
      "card_id": "相关卡片ID",
      "relation": "supports|contradicts|extends|relates"
    }
  ]
}
```

---

## 证据等级定义

| 等级 | 定义 | 适用场景 |
|------|------|----------|
| A | 多项RCT或Meta分析支持 | 核心治疗建议 |
| B | 单项RCT或高质量队列研究 | 重要临床发现 |
| C | 病例系列或专家共识 | 临床经验总结 |
| D | 专家意见或个案报告 | 诊疗思路参考 |

---

## 示例：SCI论文知识卡

```json
{
  "card_id": "WQ-SCI-011",
  "source_type": "paper",
  "source_file": "11 Obese Individuals With and Without Phlegm-Dampness Constitution.pdf",
  "title": "Obese Individuals With and Without Phlegm-Dampness Constitution: A Comparative Study",
  "authors": ["Wang Qi", "et al."],
  "year": 2019,
  "journal": "Journal of Traditional Chinese Medicine",
  "language": "en",
  
  "paper_type": "clinical_trial",
  "abstract": "...",
  "keywords": ["obesity", "phlegm-dampness constitution", "TCM"],
  
  "research_focus": {
    "constitution_type": ["痰湿质"],
    "disease": ["肥胖"],
    "topic": ["体质与疾病关系"]
  },
  
  "methods": {
    "study_design": "横断面研究",
    "sample_size": 500,
    "population": "肥胖人群",
    "outcome_measures": ["体质评分", "代谢指标"]
  },
  
  "results": {
    "main_findings": "痰湿质肥胖者代谢异常指标显著高于非痰湿质肥胖者",
    "statistical_significance": "P<0.05"
  },
  
  "conclusions": "痰湿质是肥胖及相关代谢疾病的重要体质基础",
  
  "knowledge_points": [
    {
      "category": "theory",
      "content": "痰湿质与肥胖密切相关",
      "importance": "high",
      "evidence_level": "B"
    }
  ],
  
  "related_constitutions": ["痰湿质"],
  "related_diseases": ["肥胖", "代谢综合征"],
  
  "evidence_sentences": [
    {
      "sentence": "Phlegm-dampness constitution was significantly associated with obesity...",
      "section": "Results",
      "claim_type": "finding"
    }
  ]
}
```

---

## 示例：诊疗经验知识卡

```json
{
  "card_id": "WQ-EXP-003",
  "source_type": "clinical_experience",
  "source_file": "王琦老师治疗过敏性鼻炎经验_李英帅.pdf",
  "title": "王琦老师治疗过敏性鼻炎经验",
  "authors": ["李英帅", "王琦"],
  "year": 2018,
  "language": "zh",
  
  "experience_type": "treatment_method",
  
  "clinical_focus": {
    "disease": "过敏性鼻炎",
    "syndrome": "肺脾气虚、卫外不固",
    "constitution": ["气虚质", "特禀质"]
  },
  
  "diagnostic_approach": {
    "key_points": "鼻痒、喷嚏、流清涕，遇冷加重，伴气短乏力",
    "constitution_factors": "气虚质易感，特禀质过敏倾向"
  },
  
  "treatment_approach": {
    "principle": "益气固表，调和营卫",
    "main_formula": "玉屏风散加减",
    "herbs": [
      {"name": "黄芪", "role": "君", "rationale": "益气固表"},
      {"name": "白术", "role": "臣", "rationale": "健脾益气"},
      {"name": "防风", "role": "佐", "rationale": "祛风解表"}
    ],
    "modifications": [
      {
        "condition": "鼻痒明显",
        "herbs_add": ["蝉蜕", "僵蚕"]
      }
    ]
  },
  
  "case_studies": [
    {
      "case_id": "CASE-001",
      "patient_info": "女性，35岁",
      "chief_complaint": "反复鼻痒喷嚏3年",
      "diagnosis": "过敏性鼻炎（气虚质）",
      "treatment": "玉屏风散加减",
      "outcome": "症状明显改善"
    }
  ],
  
  "clinical_insights": "过敏性鼻炎当从体质论治，气虚质调体为本",
  
  "knowledge_points": [
    {
      "category": "treatment",
      "content": "玉屏风散为治疗气虚质过敏性鼻炎的主方",
      "importance": "high",
      "evidence_level": "C"
    }
  ]
}
```

---

## 数据处理流程

1. **PDF解析** → 提取全文文本
2. **结构识别** → 识别章节、段落、表格
3. **信息抽取** → 按schema填充字段
4. **质量校验** → 检查必填字段、格式一致性
5. **向量化** → 生成embedding用于语义检索
6. **入库** → 存入向量数据库

---

## 5. 字段元数据（自动生成）

每个知识卡自动包含 `_field_meta` 和 `_review` 字段，用于追踪提取置信度和审核状态。

### 置信度等级

| Level | Score Range | Meaning | Action |
|-------|-------------|---------|--------|
| very_high | ≥0.95 | 明确可见，机器打印 | 自动接受 |
| high | 0.80-0.94 | 清晰，有小问题 | 自动接受 |
| medium | 0.65-0.79 | 需要解释 | 标记审核 |
| low | 0.40-0.64 | 显著清晰度问题 | 强制审核 |
| very_low | <0.40 | 几乎不可读/缺失 | 始终审核 |

### 字段阈值（按重要性分级）

| Field Class | Fields | Threshold |
|-------------|--------|-----------|
| critical_identity | doi, card_id | 0.95 |
| critical_operational | year, title | 0.85 |
| standard | authors, journal, keywords | 0.80 |
| descriptive | abstract, conclusions | 0.70 |

### _field_meta 结构

```json
{
  "_field_meta": {
    "title": {
      "source": "page_1_multiline|metadata|filename|text_pattern|section_heading|llm_extract",
      "confidence": 0.92,
      "level": "high",
      "reasoning": "Title found on first page with proper capitalization",
      "candidates": [
        {"value": "Primary Title", "source": "page_1", "confidence": 0.92, "level": "high"},
        {"value": "Fallback Title", "source": "filename", "confidence": 0.70, "level": "medium"}
      ]
    },
    "authors": {
      "source": "text_pattern",
      "confidence": 0.65,
      "level": "medium",
      "reasoning": "Found explicit marker but names appear generic",
      "candidates": []
    },
    "doi": {
      "source": "text_pattern",
      "confidence": 0.99,
      "level": "very_high",
      "reasoning": "Valid DOI pattern found with proper structure"
    },
    "abstract": {
      "source": "section_heading",
      "confidence": 0.90,
      "level": "high",
      "reasoning": "Abstract section found with explicit heading"
    }
  }
}
```

**候选值规则：**
- 短字段 (title, authors, journal, year, doi, keywords): 保留 Top 3 candidates
- 长字段 (abstract, conclusions): 不保留 candidates（体积过大）

### _review 结构

```json
{
  "_review": {
    "status": "auto_accepted|needs_review|manually_fixed",
    "priority": 0,
    "fields": ["authors"],
    "thresholds_used": {"authors": 0.80},
    "auto_reviewed_at": "2026-04-25T10:00:00",
    "manual_reviewed_at": null,
    "reviewer_notes": ""
  }
}
```

**状态定义：**
- `auto_accepted`: 所有字段 confidence >= 阈值
- `needs_review`: 存在字段 confidence < 阈值
- `manually_fixed`: 存在 override 文件且已应用

**优先级定义：**
- P0 (priority=0): min_confidence < 0.50，紧急
- P1 (priority=1): min_confidence 0.50-0.79，高优先级
- P2 (priority=2): 仅标记字段，正常优先级

---

## 6. 手动覆盖（独立文件）

**位置：** `data/overrides/{card_id}.json`

覆盖文件与原始卡片分离，确保重新提取时不会被覆盖。

```json
{
  "authors": ["Wang Qi", "Li Yingshuai"],
  "title": "Corrected Title",
  "_override_meta": {
    "updated_at": "2026-04-25T10:30:00",
    "updated_by": "manual",
    "reason": "Fixed author extraction error",
    "fields_changed": ["authors", "title"]
  }
}
```

**合并规则：**
1. 加载自动提取的卡片
2. 检查是否存在 override 文件
3. 应用 override 字段值
4. 更新 `_review.status` 为 `manually_fixed`
5. 索引构建仅使用合并后的值

---

## 扩展字段（预留）

```json
{
  "extensions": {
    "tags": ["自定义标签"],
    "notes": "处理备注",
    "quality_score": 0.95,
    "last_updated": "2026-01-15"
  }
}
```
