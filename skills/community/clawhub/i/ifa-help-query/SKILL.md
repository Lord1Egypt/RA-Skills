---
name: ifa-help-query
description: "Search and extract iFA Evolution help system documentation �� function descriptions, interface pa..."
tags: [domain-specific, plc, template-based, file-based, cli]
version: 1.0.0

# iFA Help Query

## 目标
�?iFA 帮助系统当作结构化知识库使用：先定位主题，再读取正文，最后输出用户真正关心的信息，而不是机械复述整�?HTML�?
## 帮助系统路径
`C:\Inovance\iFA Evolution\Repository\Help\zh-CN\`

## �?快速查询流程（优先使用�?
### 步骤 1：查索引文件�?0.5s�?读取 `D:\MyData\wangwl121\.agents\skills\ifa-help-query\ifa-topic-index.json`，这是一�?JSON 对象，key 是主题名，value 是对应的 HTML 文件名数组�?
```powershell
# 精确查找
$json = Get-Content "D:\MyData\wangwl121\.agents\skills\ifa-help-query\ifa-topic-index.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$json.'MC_MoveAbsolute'  # 返回: T2026022701912.html T2026031801893.html T2026042702032.html ...

# 模糊查找（关键词匹配�?$json | Get-Member -MemberType NoteProperty | Where-Object { $_.Name -like "*Move*" } | Select-Object Name
```

### 步骤 2：选择最佳版�?同一主题可能有多个版本文件，选择规则�?- **优先�?T20260427* 开头的文件**（最新版本）
- 其次�?T20260318* �?T20260227* �?其他

### 步骤 3：直接读�?HTML
```
C:\Inovance\iFA Evolution\Repository\Help\zh-CN\{文件名}
```

## 兜底流程（索引未命中时）
1. �?`PS000000.html` 中搜索关键词（Select-String�?2. 在所�?T*.html 中搜索关键词
3. �?`references/search-fallbacks.md` 规则进一步搜�?
## 输出格式
�?`references/output-template.md` 中的模板组织输出，优先输出：
- 对应主题名、对�?HTML 文件�?- 功能说明、接口参数、调用格�?- 返回值或错误码、注意事�?- 与相近指令或功能块的区别

不要大段复刻 HTML。要把表格内容整理成用户易读的中文说明�?
## 对比查询
如果用户要求区别、对比、和谁不同，�?`references/comparison-checklist.md` 维度并行读取相关主题页，输出差异总结�?
## 参考文�?根据需要查阅（不必全读）：
- `references/lookup-workflow.md` �?快速路径回�?- `references/output-template.md` �?输出模板
- `references/comparison-checklist.md` �?多主题对比检查清�?- `references/search-fallbacks.md` �?兜底搜索策略
