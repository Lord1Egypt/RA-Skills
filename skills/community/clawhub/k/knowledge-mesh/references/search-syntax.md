# 搜索语法指南

本文档说明 knowledge-mesh 的搜索查询语法和各平台特有的搜索技巧。

---

## 基本搜索语法

### 关键词搜索

直接输入关键词，空格分隔表示 AND 关系：

```
python async fastapi
```

搜索同时包含 "python"、"async" 和 "fastapi" 的内容。

### 精确匹配

使用双引号包裹短语进行精确匹配：

```
"connection pool" timeout
```

搜索包含完整短语 "connection pool" 且含 "timeout" 的内容。

### 排除关键词

使用减号排除不需要的结果（部分平台支持）：

```
python web framework -django
```

---

## 平台特有语法

### GitHub

```
# 按仓库搜索
repo:owner/name keyword

# 按语言过滤
language:python async

# 按标签过滤
label:bug memory leak

# 按状态过滤
state:open performance issue

# 组合搜索
repo:fastapi/fastapi label:question websocket
```

### Stack Overflow

```
# 按标签搜索
[python] [async] how to

# 搜索已采纳答案
is:answer accepted:yes connection pool

# 按分数过滤
score:10 python decorator

# 按时间范围
created:2026-01.. python 3.12
```

### Confluence (CQL)

```
# 按空间搜索
space=DEV AND text~"api design"

# 按类型过滤
type=page AND title~"architecture"

# 按标签
label=backend AND text~"microservice"

# 按创建者
creator=currentUser() AND text~"meeting notes"
```

### Notion

```
# 基本关键词（Notion API 仅支持简单文本搜索）
project roadmap

# 建议使用具体的页面或数据库标题关键词
sprint planning Q1 2026
```

### Slack

```
# 按频道搜索
in:#engineering python deployment

# 按用户搜索
from:@username production issue

# 按时间范围
after:2026-03-01 before:2026-03-19 release

# 搜索文件
has:link architecture document
```

---

## 搜索技巧

1. **使用具体关键词**：避免过于宽泛的搜索词，如 "问题" 或 "error"，改用具体的错误信息或技术术语。

2. **善用平台优势**：
   - 代码问题 → 优先搜索 Stack Overflow 和 GitHub
   - 团队知识 → 优先搜索 Confluence 和 Notion
   - 实时讨论 → 优先搜索 Discord 和 Slack

3. **迭代优化**：首次搜索结果不理想时，根据返回的标签和关键词调整查询。

4. **结合多个来源**：跨平台搜索可以获得更全面的信息，免费版支持同时搜索 GitHub 和 Stack Overflow。

5. **利用标签过滤**：搜索结果中的标签可以帮助你发现相关主题和更精确的搜索词。

---

## 搜索示例

| 场景 | 推荐查询 | 建议平台 |
|------|----------|----------|
| Python 异步编程 | `python asyncio await best practices` | Stack Overflow, GitHub |
| React 性能优化 | `react performance optimization memo` | Stack Overflow, GitHub |
| 团队 API 设计规范 | `api design guidelines rest` | Confluence, Notion |
| 部署问题排查 | `deployment failed kubernetes pod` | Slack, Discord |
| 开源项目选型 | `python web framework comparison 2026` | GitHub, Stack Overflow |
