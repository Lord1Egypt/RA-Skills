# 使用示例

## 场景 1: 快速文献调研

### 用户请求
"帮我找一些关于 transformer 架构的最新论文"

### 实现步骤
```python
from scripts.google_scholar_search import GoogleScholarSearch

# 初始化（假设已设置 SERP_API_KEY 环境变量）
client = GoogleScholarSearch()

# 搜索最近3年的论文
results = client.search(
    query="transformer architecture",
    num_results=10,
    year_from=2023,
    sort_by="date"
)

# 解析结果
papers = client.parse_results(results)

# 输出格式化结果
print(f"## Transformer 架构最新论文（2023年至今）")
print(f"共找到 {len(papers)} 篇相关论文\n")

for i, paper in enumerate(papers):
    print(f"{i+1}. **{paper['title']}**")
    print(f"   - 作者: {', '.join(paper['authors'][:3])}{'等' if len(paper['authors']) > 3 else ''}")
    print(f"   - 年份: {paper['year']}")
    print(f"   - 引用: {paper['cited_by']}")
    
    if 'pdf_link' in paper:
        print(f"   - PDF: ✅ 可用（{paper['pdf_link']}）")
    else:
        print(f"   - PDF: ❌ 不可用")
    print()
```

## 场景 2: 批量下载特定主题论文

### 用户请求
"下载5篇关于强化学习在游戏中的应用的PDF"

### 实现步骤
```python
from scripts.google_scholar_search import GoogleScholarSearch
import os

# 设置下载目录
download_dir = "./reinforcement_learning_games"
os.makedirs(download_dir, exist_ok=True)

# 执行搜索和下载
client = GoogleScholarSearch()
result = client.search_and_download(
    query="reinforcement learning games",
    download_dir=download_dir,
    max_papers=5
)

# 生成报告
print(f"## 下载完成报告")
print(f"搜索关键词: {result['query']}")
print(f"找到论文总数: {result['total_results']}")
print(f"有PDF的论文: {result['papers_with_pdf']}")
print(f"成功下载: {result['successful_downloads']}")
print()

print("### 下载详情:")
for i, paper in enumerate(result['papers']):
    status = "✅ 成功" if paper.get('download_success') else "❌ 失败"
    print(f"{i+1}. {paper['title'][:60]}... - {status}")
    
    if paper.get('download_path'):
        print(f"   保存位置: {paper['download_path']}")
```

## 场景 3: 学术趋势分析

### 用户请求
"分析机器学习领域近5年的研究趋势"

### 实现步骤
```python
from scripts.google_scholar_search import GoogleScholarSearch
from collections import Counter
import matplotlib.pyplot as plt

# 搜索不同年份的论文
client = GoogleScholarSearch()
keywords = ["machine learning", "deep learning", "neural networks"]

year_stats = {}
for keyword in keywords:
    print(f"搜索: {keyword}")
    
    for year in range(2019, 2025):
        results = client.search(
            query=keyword,
            num_results=20,
            year_from=year,
            year_to=year
        )
        
        papers = client.parse_results(results)
        if keyword not in year_stats:
            year_stats[keyword] = {}
        year_stats[keyword][year] = len(papers)
        
        # 避免频繁请求
        import time
        time.sleep(1)

# 输出统计结果
print("\n## 学术趋势分析（2019-2024）")
print("年份 | 机器学习 | 深度学习 | 神经网络")
print("-----|----------|----------|----------")

for year in range(2019, 2025):
    ml = year_stats.get("machine learning", {}).get(year, 0)
    dl = year_stats.get("deep learning", {}).get(year, 0)
    nn = year_stats.get("neural networks", {}).get(year, 0)
    
    print(f"{year} | {ml:^8} | {dl:^8} | {nn:^8}")
```

## 场景 4: 文献引用网络

### 用户请求
"查找某篇高引用论文的相关研究"

### 实现步骤
```python
from scripts.google_scholar_search import GoogleScholarSearch

def find_related_papers(main_paper_title, depth=2):
    """查找相关论文的引用网络"""
    client = GoogleScholarSearch()
    
    # 搜索主论文
    print(f"搜索主论文: {main_paper_title}")
    main_results = client.search(main_paper_title, num_results=1)
    main_papers = client.parse_results(main_results)
    
    if not main_papers:
        print("未找到相关论文")
        return
    
    main_paper = main_papers[0]
    print(f"找到: {main_paper['title']}")
    print(f"引用次数: {main_paper['cited_by']}")
    
    # 搜索引用该论文的研究
    print(f"\n搜索引用该论文的研究:")
    citation_query = f'"{main_paper_title}" citations'
    citation_results = client.search(citation_query, num_results=10)
    citation_papers = client.parse_results(citation_results)
    
    print(f"找到 {len(citation_papers)} 篇引用文献:")
    for i, paper in enumerate(citation_papers[:5]):
        print(f"  {i+1}. {paper['title'][:80]}... ({paper['year']})")
    
    return {
        'main_paper': main_paper,
        'citations': citation_papers
    }

# 使用示例
related = find_related_papers("Attention Is All You Need")
```

## 场景 5: 命令行批量处理

### 用户请求
"批量搜索多个关键词并保存结果"

### 实现步骤
```bash
#!/bin/bash

# 关键词列表
KEYWORDS=(
    "machine learning"
    "artificial intelligence"
    "deep learning"
    "computer vision"
    "natural language processing"
)

# 创建输出目录
OUTPUT_DIR="./academic_search_results"
mkdir -p "$OUTPUT_DIR"

# 遍历关键词
for keyword in "${KEYWORDS[@]}"; do
    echo "搜索: $keyword"
    
    # 安全处理关键词中的空格
    safe_keyword=$(echo "$keyword" | sed 's/ /_/g')
    
    # 执行搜索
    python scripts/google_scholar_search.py \
        "$keyword" \
        --num 10 \
        --output "$OUTPUT_DIR/$safe_keyword"
    
    echo "结果保存到: $OUTPUT_DIR/$safe_keyword"
    echo
done

echo "批量搜索完成！"
```

## 场景 6: 集成到 OpenClaw 工作流

### 用户请求
"在 OpenClaw 中创建一个学术研究助手"

### 实现思路
1. **环境检查**: 自动检查 SERP_API_KEY 是否设置
2. **命令解析**: 解析用户的自然语言请求
3. **智能搜索**: 根据上下文优化搜索参数
4. **结果格式化**: 生成易读的 Markdown 报告
5. **文件管理**: 自动组织下载的论文

### 示例响应模板
```markdown
## 学术搜索报告

**搜索关键词**: {query}
**搜索时间**: {timestamp}
**找到论文数**: {total_count}
**有PDF的论文**: {pdf_count}

### 推荐阅读（按引用排序）

1. **{paper1_title}** ({paper1_year})
   - 作者: {paper1_authors}
   - 引用: {paper1_citations}
   - PDF: {paper1_pdf_status}
   - 摘要: {paper1_snippet}

2. **{paper2_title}** ({paper2_year})
   - 作者: {paper2_authors}
   - 引用: {paper2_citations}
   - PDF: {paper2_pdf_status}
   - 摘要: {paper2_snippet}

### 操作建议
- 下载所有PDF: `python scripts/google_scholar_search.py "{query}" --num {pdf_count}`
- 搜索相关主题: `python scripts/google_scholar_search.py "related topic"`
- 导出引用信息: 可生成 BibTeX 格式引用
```

## 最佳实践提示

### 1. 搜索优化
- 使用双引号进行精确匹配
- 添加领域限定词（如 "in healthcare"）
- 组合多个相关关键词
- 利用年份过滤获取最新研究

### 2. 结果处理
- 优先处理高引用论文
- 检查PDF可用性再决定下载
- 保存搜索历史避免重复
- 定期整理下载的文献

### 3. 合规使用
- 尊重版权和访问限制
- 合理控制请求频率
- 仅用于个人学术研究
- 引用时注明来源

### 4. 性能优化
- 缓存常用搜索结果
- 批量处理减少API调用
- 使用本地数据库存储元数据
- 定期清理临时文件