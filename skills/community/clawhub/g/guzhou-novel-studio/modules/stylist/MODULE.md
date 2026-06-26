# 风格模块

> **路径**：modules/stylist/
> **来源**：GitHub - novel-style-reference + yunhui-style-writer

## 模块说明

风格模块负责风格提取、管理、保持和进化。

## 子模块

### 1. novel-style-reference

通用风格参考工具，支持从样本文本提取风格DNA。

### 2. yunhui-style

云辉风格专精工具，提供随性自由写作风格支持。

## 核心功能

| 功能 | 说明 | 数据来源 |
|------|------|---------|
| 风格提取 | 从样本文本提取风格DNA | 用户提供的参考作品 |
| 风格保持 | 创作时遵循风格DNA | Style-DNA.json |
| 风格进化 | 根据用户反馈调整风格 | 用户修改记录 |

## Style-DNA 结构

```json
{
  "style_id": "uuid",
  "style_name": "风格名称",
  "created_at": "日期",
  "source_texts": ["文本片段1", "文本片段2"],
  
  "linguistic_features": {
    "sentence_length": "short|medium|long|mixed",
    "paragraph_length": "short|medium|long|mixed",
    "vocabulary_level": "simple|moderate|advanced|mixed",
    "formality_level": "casual|neutral|formal"
  },
  
  "narrative_voice": {
    "perspective": "first|second|third",
    "tone": "serious|humorous|ironic|lyrical",
    "distance": "intimate|neutral|detached"
  },
  
  "dialogue_style": {
    "quotation_marks": "「」|「」|\"\"'",
    "dialogue_tags": "minimal|moderate|heavy",
    "speech_patterns": ["特点1", "特点2"]
  },
  
  "pacing_features": {
    "rhythm": "fast|moderate|slow|varied",
    "scene_transitions": "abrupt|gradual|mixed"
  },
  
  "genre_markers": ["标记1", "标记2"],
  "memorable_phrases": ["经典句式1", "经典句式2"]
}
```

## 触发词

- "风格"
- "提取风格"
- "模仿"
- "像...一样"
- "云辉风格"
