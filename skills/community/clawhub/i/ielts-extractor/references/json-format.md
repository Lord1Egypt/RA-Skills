# JSON 格式规范

## 基本结构

```json
{
  "id": "reading-p1",
  "title": "文章标题",
  "content": "文章正文...",
  "question_groups": [
    {
      "id": "g1",
      "title": "Questions 1-4",
      "type": "multiple-choice-single",
      "instruction": "Choose correct letter...",
      "questions": [...]
    }
  ]
}
```

## 选项格式

### 共享选项(题组级)
```json
{
  "type": "matching-headings",
  "options": [{"id": "A", "text": "..."}],
  "questions": [{"id": "q1", "answer": "A"}]
}
```

### 独立选项(每题)
```json
{
  "type": "multiple-choice-single",
  "questions": [
    {
      "id": "q1",
      "options": [{"id": "A", "text": "..."}],
      "answer": "A"
    }
  ]
}
```

### 表格题
```json
{
  "type": "table-completion",
  "image": "/images/xxx.png",
  "questions": [{"id": "q1", "answer": "xxx"}]
}
```

### 填空题
```json
{
  "type": "fill-blank-summary",
  "passage_fragment": "原文挖空 [1] [2]",
  "questions": [{"id": "q1", "content": "[1]答案", "answer": "xxx"}]
}
```
