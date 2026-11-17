# 网页搜索与代码搜索

## 概述

通用搜索引擎，适用于广泛的信息检索需求。

## 搜索引擎

### Bing 搜索
- **引擎标识**: `"bing"`
- **适用场景**: 英文内容、国际资讯、通用查询
- **特点**: 覆盖全球互联网，支持多语言

```yaml
query: "machine learning best practices"
engines: ["bing"]
max_results: 10
```

### Baidu 搜索
- **引擎标识**: `"baidu"`
- **适用场景**: 中文内容、国内资讯
- **特点**: 中文搜索体验好，国内网站覆盖全

```yaml
query: "机器学习 最佳实践"
engines: ["baidu"]
max_results: 10
```

## 使用技巧

### 关键词优化
- **英文内容**: 优先使用 Bing，关键词使用英文
- **中文内容**: 优先使用 Baidu，关键词使用中文
- **精确匹配**: 使用 `"精确短语"`
- **排除词汇**: 使用 `关键词 -排除词`
- **文件类型**: 使用 `关键词 filetype:pdf`

### 搜索策略
1. **通用查询**: 直接使用 Bing 或 Baidu
2. **中英文对比**: 分别用 Bing (英文) 和 Baidu (中文) 搜索
3. **时效性内容**: 优先使用搜索引擎获取最新信息

## 示例

```yaml
# 搜索技术文档
query: "React hooks documentation"
engines: ["bing"]

# 搜索中文教程
query: "React Hooks 教程"
engines: ["baidu"]

# 搜索 PDF 文档
query: "machine learning filetype:pdf"
engines: ["bing"]

# 精确匹配
query: '"React useEffect hook"'
engines: ["bing"]
```
