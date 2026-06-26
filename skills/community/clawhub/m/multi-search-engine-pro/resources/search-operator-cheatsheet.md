# Search Operator Cheatsheet

## Core operators

- `site:example.com` — 站内检索
- `filetype:pdf` — 文件类型过滤
- `"exact phrase"` — 精确短语
- `-exclude` — 排除词
- `A OR B` — 替代词组

## Recommended combinations

### 查文档
`site:docs.example.com "authentication"`

### 查 PDF
`"retrieval augmented generation" filetype:pdf`

### 查代码仓库
`site:github.com react hooks`

### 排除噪音
`python tutorial -snake -zoo`

## Time scopes used by the script

- `hour`
- `day`
- `week`
- `month`
- `year`

The script only appends time parameters where a known mapping exists.
