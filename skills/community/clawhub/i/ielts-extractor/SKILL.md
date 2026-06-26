# IELTS 试题数据提取 Skill

## 概述

从剑桥雅思 PDF 提取阅读文章和题目。

## 触发条件

用户要求"提取雅思试题"时使用。

## 流程(4步)

### 1. 定位 PDF 和页码

- 查找 "Test X" + "READING PASSAGE Y"
- 记录起始页码

### 2. 提取文章

- **必须连续提取多页**
- 处理两栏布局
- 检查字数: 1500-2500词/篇

详见: `references/pdf-extraction.md`

### 3. 提取题目

- 按大题分组
- 选择正确题型
- 完整选项(单选每题A-D)

详见: `references/question-types.md`

### 4. 保存 JSON

- 使用 content 字段
- 选项格式正确

详见: `references/json-format.md`

## 数据文件

```
ielts-tracker/data/tests/cambridge-{4,5,6}/test-{1-4}/test.json
ielts-tracker/ielts-app/public/images/
```

## 题型速查

| 题型 | type |
|------|------|
| 标题配对 | matching-headings |
| 判断题 | yes-no-not-given |
| 单选 | multiple-choice-single |
| 多选 | multiple-answer |
| 表格 | table-completion |
| 填空 | fill-blank-summary |
