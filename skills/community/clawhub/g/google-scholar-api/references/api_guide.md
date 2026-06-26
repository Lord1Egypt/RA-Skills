# Google Scholar API 使用指南

## 概述

本技能使用 SerpAPI 的 Google Scholar API 来访问学术论文数据。SerpAPI 是一个专业的搜索引擎API服务，提供对 Google Scholar 搜索结果的结构化访问。

## 官方资源

- **官方网站**: https://serpapi.com/search-api
- **Google Scholar API 页面**: https://serpapi.com/google-scholar-api
- **API 端点**: `https://serpapi.com/search?engine=google_scholar`
- **在线演示**: https://serpapi.com/playground?engine=google_scholar

## 获取 API 密钥

### 免费计划
1. 访问 [SerpAPI 官网](https://serpapi.com/)
2. 点击 "Register" 注册账号
3. 完成邮箱验证
4. 在 Dashboard 中获取 API 密钥
5. **免费计划**: 每月 250 次搜索，50次/小时吞吐量

### 付费计划
- **Starter**: $25/月，1000次搜索
- **Developer**: $75/月，5000次搜索  
- **Production**: $150/月，15000次搜索
- **Big Data**: $275/月，30000次搜索
- **Enterprise**: 定制方案

## 环境设置

### 方法1：设置环境变量
```bash
export SERP_API_KEY="your_api_key_here"
```

### 方法2：在代码中直接设置
```python
import os
os.environ['SERP_API_KEY'] = 'your_api_key_here'
```

### 方法3：传递给客户端
```python
from google_scholar_search import GoogleScholarSearch
client = GoogleScholarSearch(api_key='your_api_key_here')
```

## API 参数详解

### 必需参数
- `engine`: 必须设置为 `google_scholar`
- `api_key`: 你的 SerpAPI 密钥
- `q`: 搜索查询（支持高级语法如 `author:` 和 `source:`）

### 搜索查询参数
- `q`: 搜索关键词，支持高级语法：
  - `author:"作者名"` - 按作者搜索
  - `source:"期刊名"` - 按来源搜索
  - `"精确短语"` - 精确匹配
- `cites`: 文章ID，用于搜索引用该文章的其他文章
- `cluster`: 文章ID，用于搜索所有版本

### 时间过滤参数
- `as_ylo`: 起始年份（例如：`2018`）
- `as_yhi`: 结束年份（例如：`2023`）
- 可以单独使用或组合使用

### 排序和过滤
- `scisbd`: 排序方式
  - `0`: 按相关性排序（默认）
  - `1`: 按日期排序，仅包含摘要
  - `2`: 按日期排序，包含所有内容
- `as_sdt`: 搜索类型/过滤器
  - `0`: 排除专利（默认）
  - `7`: 包含专利
  - `4`: 选择案例法（美国法院）
- `as_vis`: 是否包含引用
  - `0`: 包含引用（默认）
  - `1`: 排除引用
- `as_rr`: 是否仅显示综述文章
  - `0`: 显示所有结果（默认）
  - `1`: 仅显示综述文章

### 分页参数
- `num`: 每页结果数（1-20，默认10）
- `start`: 起始位置（用于分页，例如：`0`, `10`, `20`）

### 本地化参数
- `hl`: 语言代码（例如：`en`, `zh-CN`, `ja`）
- `lr`: 语言限制（例如：`lang_zh-CN|lang_en`）

### SerpAPI 特定参数
- `no_cache`: 是否禁用缓存
  - `false`: 允许缓存（默认）
  - `true`: 禁用缓存
- `output`: 输出格式
  - `json`: JSON格式（默认）
  - `html`: 原始HTML
- `async`: 异步模式
  - `false`: 同步请求（默认）
  - `true`: 异步请求

## 结果字段说明

### 搜索元数据
```json
"search_metadata": {
  "id": "搜索ID",
  "status": "Success/Processing/Error",
  "json_endpoint": "JSON结果端点",
  "created_at": "创建时间",
  "processed_at": "处理时间",
  "google_scholar_url": "原始Google Scholar URL",
  "total_time_taken": 总耗时
}
```

### 搜索信息
```json
"search_information": {
  "total_results": 总结果数,
  "time_taken_displayed": 显示耗时,
  "query_displayed": "显示的查询",
  "organic_results_state": "结果状态描述"
}
```

### 有机结果（论文列表）
每个论文结果包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `position` | integer | 结果位置（从0开始） |
| `title` | string | 论文标题 |
| `result_id` | string | 结果唯一ID |
| `link` | string | 论文原始链接 |
| `snippet` | string | 摘要片段 |
| `type` | string | 结果类型（Html/PDF等） |
| `publication_info` | object | 出版信息 |
| `publication_info.summary` | string | 作者、年份、来源摘要 |
| `publication_info.authors` | array | 作者详细信息数组 |
| `resources` | array | 资源链接（PDF/HTML等） |
| `inline_links` | object | 内联链接 |
| `inline_links.cited_by` | object | 引用信息 |
| `inline_links.cited_by.total` | integer | 引用次数 |
| `inline_links.cited_by.link` | string | 引用页面链接 |
| `inline_links.cited_by.cites_id` | string | 引用ID |
| `inline_links.versions` | object | 所有版本信息 |
| `inline_links.versions.total` | integer | 版本数量 |
| `inline_links.versions.cluster_id` | string | 集群ID |
| `inline_links.serpapi_cite_link` | string | SerpAPI引用链接 |
| `inline_links.related_pages_link` | string | 相关页面链接 |

### 资源字段
```json
"resources": [
  {
    "title": "网站域名",
    "file_format": "PDF/HTML",
    "link": "资源链接"
  }
]
```

### 作者字段
```json
"authors": [
  {
    "name": "作者名",
    "link": "作者Google Scholar页面",
    "author_id": "作者ID",
    "serpapi_scholar_link": "SerpAPI作者链接"
  }
]
```

### 其他结果部分
- `related_searches`: 相关搜索建议
- `pagination`: 分页信息
- `citations_per_year`: 每年引用统计（当使用cites参数时）
- `profiles`: 作者档案信息

## PDF 下载说明

### PDF 可用性
- 并非所有论文都有可公开下载的 PDF
- PDF 链接可能指向 arXiv、ResearchGate、期刊网站等
- 某些 PDF 可能需要机构访问权限

### 下载限制
- 尊重版权和访问限制
- 不要大规模批量下载
- 仅用于个人研究目的

## 错误处理

### 常见错误
1. **API 密钥无效**: 检查密钥是否正确，是否有余额
2. **请求限制**: 免费计划每月 100 次搜索
3. **网络问题**: 检查网络连接
4. **PDF 下载失败**: 链接可能失效或需要特殊权限

### 错误代码
```python
try:
    results = client.search("machine learning")
except Exception as e:
    print(f"搜索失败: {e}")
```

## 最佳实践

### 搜索优化
1. 使用具体的关键词组合
2. 添加引号进行精确匹配
3. 使用年份过滤获取最新研究
4. 限制结果数量以提高速度

### 资源管理
1. 缓存搜索结果避免重复请求
2. 分批处理大量搜索
3. 定期检查 API 使用量

### 合规使用
1. 仅用于学术研究
2. 遵守目标网站的 robots.txt
3. 不要过度请求（建议间隔 1-2 秒）
4. 尊重版权和访问条款

## 示例查询

### 基础搜索
- "deep learning neural networks"
- "quantum computing algorithms"
- "climate change mitigation strategies"

### 高级搜索
- "transformer architecture" year_from:2020 year_to:2024
- "reinforcement learning" sort_by:date
- "machine learning in healthcare" num_results:20

## 故障排除

### 问题：API 返回空结果
- 检查查询关键词是否正确
- 尝试简化查询
- 检查网络连接

### 问题：PDF 下载失败
- 检查链接是否有效
- 尝试手动访问链接
- 某些网站可能需要特殊 headers

### 问题：速度慢
- 减少每次请求的结果数量
- 添加请求间隔
- 检查网络状况

## 相关资源

- [SerpAPI 文档](https://serpapi.com/search-api)
- [Google Scholar 高级搜索技巧](https://scholar.google.com/intl/en/scholar/help.html)
- [学术论文下载规范](https://www.coar-repositories.org/activities/supporting-fair-data/)