---
name: google-scholar-api
description: 通过 SerpAPI 实现 Google Scholar 学术论文检索和下载。使用场景包括：1) 通过关键词搜索学术论文，2) 获取论文详细信息（标题、作者、摘要、年份、引用次数），3) 下载可用的 PDF 文件，4) 批量检索相关文献，5) 按年份、引用数等条件筛选论文。需要 SerpAPI 密钥（可从 serpapi.com 获取免费额度）。
---

# Google Scholar API 技能

## 概述

本技能提供通过 SerpAPI 访问 Google Scholar 的功能，实现学术论文的智能检索和下载。包含完整的 Python 脚本、配置示例和使用指南。

## 快速开始

### 1. 安装依赖
```bash
pip install google-search-results requests
```

### 2. 设置 API 密钥
```bash
export SERP_API_KEY="your_serpapi_key_here"
```

### 3. 基本搜索示例
```python
from scripts.google_scholar_search import GoogleScholarSearch

# 初始化客户端
client = GoogleScholarSearch()

# 搜索论文
results = client.search("machine learning", num_results=5)
papers = client.parse_results(results)

for paper in papers:
    print(f"标题: {paper['title']}")
    print(f"作者: {paper['authors']}")
    print(f"年份: {paper['year']}")
    if 'pdf_link' in paper:
        print(f"PDF 可用: {paper['pdf_link']}")
```

## 核心功能

### 1. 论文搜索（基于 SerpAPI）
- **基本搜索**: 关键词、短语搜索
- **高级搜索**: 作者搜索 (`author:"姓名"`)、来源搜索 (`source:"期刊"`)
- **时间过滤**: 按年份范围筛选 (`as_ylo`, `as_yhi`)
- **排序选项**: 相关性、日期（仅摘要）、日期（全部内容）
- **引用搜索**: 搜索引用特定文章的文献 (`cites` 参数)
- **版本搜索**: 搜索文章的所有版本 (`cluster` 参数)

### 2. 结果解析
- **完整元数据**: 标题、作者、年份、期刊、摘要
- **引用信息**: 引用次数、引用ID、集群ID
- **作者详情**: 作者姓名、Google Scholar链接、作者ID
- **资源链接**: PDF、HTML、相关页面、引用链接
- **搜索统计**: 总结果数、处理时间、搜索状态

### 3. PDF 下载
- **智能检测**: 自动识别可用的PDF链接
- **批量下载**: 支持批量下载多个论文
- **文件命名**: 按"年份_标题"格式自动命名
- **下载跟踪**: 记录下载状态和路径
- **错误处理**: 网络超时、链接失效等异常处理

### 4. 高级功能
- **作者专搜**: 专门搜索某位作者的所有论文
- **引用分析**: 分析某篇文章的引用网络
- **版本追踪**: 查找文章的所有版本
- **多语言**: 支持多种语言搜索 (`hl` 参数)
- **综述筛选**: 仅显示综述文章 (`as_rr` 参数)

## 工作流程

### 步骤 1: 准备环境
1. 获取 SerpAPI 密钥（免费注册）
2. 安装 Python 依赖
3. 设置环境变量或直接传递密钥

### 步骤 2: 执行搜索
```python
# 基础搜索
client.search("deep learning", num_results=10)

# 高级搜索（带过滤）
client.search(
    query="transformer",
    year_from=2020,
    year_to=2024,
    sort_by="date"
)
```

### 步骤 3: 处理结果
```python
# 解析结果
papers = client.parse_results(search_data)

# 检查 PDF 可用性
for paper in papers:
    if 'pdf_link' in paper:
        print(f"可下载: {paper['title']}")
```

### 步骤 4: 下载文件
```python
# 单个文件下载
client.download_pdf(pdf_url, "paper.pdf")

# 批量搜索和下载
result = client.search_and_download(
    query="reinforcement learning",
    download_dir="./papers",
    max_papers=5
)
```

## 使用示例

### 示例 1: 简单文献调研
```python
# 搜索某个主题的最新论文
client = GoogleScholarSearch()
results = client.search("quantum machine learning", num_results=15, sort_by="date")
papers = client.parse_results(results)

print(f"找到 {len(papers)} 篇相关论文")
for i, paper in enumerate(papers[:5]):
    print(f"{i+1}. {paper['title']} ({paper['year']}) - {paper['cited_by']} 次引用")
```

### 示例 2: 下载特定年份的论文
```python
# 下载 2020-2023 年的论文
result = client.search_and_download(
    query="computer vision",
    download_dir="./cv_papers",
    max_papers=10,
    year_from=2020,
    year_to=2023
)

print(f"成功下载 {result['successful_downloads']} 篇论文")
```

### 示例 3: 命令行使用
```bash
# 直接运行脚本
python scripts/google_scholar_search.py "artificial intelligence" --num 10 --output ./ai_papers
```

## SerpAPI 配置

### API 密钥和计划
- **免费计划**: 每月 250 次搜索，50次/小时吞吐量
- **Starter**: $25/月，1000次搜索，200次/小时
- **Developer**: $75/月，5000次搜索，1000次/小时
- **Production**: $150/月，15000次搜索，3000次/小时
- **Big Data**: $275/月，30000次搜索，6000次/小时

### 重要限制
- **每页结果**: 1-20 条（`num` 参数）
- **分页**: 通过 `start` 参数（0, 10, 20...）
- **缓存**: 默认启用，1小时有效期
- **异步模式**: 支持异步请求 (`async` 参数)
- **输出格式**: JSON（默认）或原始HTML

### 搜索参数详解
- `q`: 搜索查询（支持 `author:`, `source:` 语法）
- `num`: 每页结果数（1-20，默认10）
- `start`: 分页起始位置（0, 10, 20...）
- `as_ylo`/`as_yhi`: 年份范围过滤
- `scisbd`: 排序方式（0=相关性, 1=日期仅摘要, 2=日期全部）
- `hl`: 语言代码（en, zh-CN, ja 等）
- `as_vis`: 是否包含引用（0=包含, 1=排除）
- `as_rr`: 是否仅显示综述文章（0=全部, 1=仅综述）
- `cites`: 搜索引用特定文章的文献
- `cluster`: 搜索文章的所有版本

### 下载设置
- `download_dir`: 下载目录（默认 "./downloads"）
- 自动创建目录
- 文件按论文标题命名

## 错误处理

### 常见问题
1. **API 密钥错误**: 检查密钥是否正确设置
2. **额度不足**: 免费计划每月 100 次搜索
3. **网络问题**: 检查网络连接和代理设置
4. **PDF 不可用**: 并非所有论文都有公开 PDF

### 调试建议
```python
import logging
logging.basicConfig(level=logging.DEBUG)

try:
    results = client.search("test query")
except Exception as e:
    print(f"错误详情: {e}")
    # 检查环境变量
    print(f"API Key: {os.getenv('SERP_API_KEY')}")
```

## 最佳实践

### 搜索优化
1. 使用具体、相关的关键词
2. 添加引号进行精确匹配
3. 合理设置结果数量避免超限
4. 使用年份过滤获取最新研究

### 资源管理
1. 缓存常用搜索结果
2. 分批处理大量请求
3. 定期清理下载目录
4. 备份重要论文

### 合规使用
1. 仅用于个人学术研究
2. 尊重版权和访问条款
3. 不要大规模批量下载
4. 遵守目标网站的 robots.txt

## 资源文件

### scripts/ 目录
包含可执行的 Python 脚本：

1. **google_scholar_search.py** - 核心搜索和下载脚本
   - 主要功能类 `GoogleScholarSearch`
   - 支持搜索、解析、下载完整流程
   - 命令行接口

2. **config_example.py** - 配置和使用示例
   - 基础搜索示例
   - PDF 下载示例
   - 高级搜索示例

3. **requirements.txt** - 依赖包列表
   - `google-search-results`: SerpAPI Python 客户端
   - `requests`: HTTP 请求库

### references/ 目录
包含详细参考文档：

1. **api_guide.md** - API 使用指南
   - SerpAPI 密钥获取
   - 搜索参数详解
   - 结果字段说明
   - 错误处理和最佳实践

## 文件结构
```
google-scholar-api/
├── SKILL.md (本文件)
├── scripts/
│   ├── google_scholar_search.py (核心脚本)
│   ├── config_example.py (配置示例)
│   └── requirements.txt (依赖列表)
└── references/
    └── api_guide.md (API 指南)
```

## 使用提示

### 在 OpenClaw 中使用
当用户请求搜索学术论文时：
1. 检查是否设置了 `SERP_API_KEY` 环境变量
2. 使用 `scripts/google_scholar_search.py` 执行搜索
3. 根据需要下载 PDF 文件
4. 提供格式化的搜索结果

### 常见用户请求模式
- "帮我搜索关于机器学习的论文"
- "下载最近3年关于深度学习的PDF"
- "查找引用次数超过1000的经典论文"
- "批量下载某个研究主题的相关文献"

### 响应格式建议
```markdown
## 搜索结果：机器学习

找到 15 篇相关论文，其中 8 篇有 PDF 可用：

1. **Attention Is All You Need** (2017)
   - 作者：Vaswani et al.
   - 引用：125,000+
   - PDF: ✅ 可用
   - 下载：`python scripts/google_scholar_search.py "Attention Is All You Need"`

2. **Deep Residual Learning for Image Recognition** (2015)
   - 作者：He et al.
   - 引用：85,000+
   - PDF: ✅ 可用
   - 下载：`python scripts/google_scholar_search.py "Deep Residual Learning"`

...
```

## 注意事项

### 限制和约束
1. **API 限制**: SerpAPI 免费计划每月 100 次搜索
2. **PDF 可用性**: 并非所有论文都有公开 PDF
3. **下载速度**: 受网络和服务器响应影响
4. **版权遵守**: 仅用于个人学术研究

### 扩展建议
如需更多功能，可考虑：
1. 集成其他学术数据库（arXiv、PubMed 等）
2. 添加引用管理功能（BibTeX 导出）
3. 实现论文推荐系统
4. 添加文献综述自动生成

---

**技能维护**: 定期检查 SerpAPI 的 API 变化，更新脚本以保持兼容性。
