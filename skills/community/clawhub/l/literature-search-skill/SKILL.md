---
name: literature-search
description: 学术文献搜索技能 - 支持多平台文献搜索、内容提取和分析
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "anyBins": ["python", "curl"] },
      },
  }
---

# 学术文献搜索技能

专业的学术文献搜索和分析工具，支持多个学术平台。

## 支持的学术平台

- **arXiv** - 预印本论文
- **Google Scholar** - 学术搜索引擎
- **PubMed** - 生物医学文献
- **IEEE Xplore** - 工程和计算机科学
- **ACM Digital Library** - 计算机科学

## 使用方法

### 基础搜索
```bash
# 搜索特定主题
web_search query:"[your topic] site:arxiv.org" count:10 freshness:"month"

# 搜索特定期刊
web_search query:"[your topic] site:nature.com" count:5
```

### 高级搜索技巧

#### 时间范围搜索
```bash
# 最近1个月
web_search query:"large language model optimization" freshness:"month"

# 最近1年
web_search query:"quantum computing applications" freshness:"year"
```

#### 多关键词搜索
```bash
# 组合搜索
web_search query:"(machine learning) AND (healthcare) site:arxiv.org" count:10
```

## 文献分析流程

### 1. 文献搜索
搜索相关主题的文献，获取标题、摘要和链接。

### 2. 内容获取
使用 `web_fetch` 获取文献全文内容。

### 3. 内容分析
利用模型能力进行：
- **内容总结** - 提取核心观点
- **创新点识别** - 识别技术突破
- **分类整理** - 按研究方向分类
- **差异对比** - 比较不同方法

### 4. 报告生成
生成结构化的文献综述报告。

## 示例工作流

### 完整的文献调研
```bash
# 1. 搜索文献
web_search query:"transformer optimization techniques" count:8 freshness:"month"

# 2. 获取重点文献全文
web_fetch url:"https://arxiv.org/abs/important-paper"

# 3. 分析总结
# 模型自动进行内容分析和分类
```

## 输出格式

### 文献摘要
- 标题和作者
- 发表时间
- 核心贡献
- 技术方法
- 实验结果

### 分类报告
- 按研究方向分类
- 创新点对比
- 发展趋势分析
- 研究空白识别

## 注意事项

1. **版权尊重** - 仅用于学术研究
2. **引用规范** - 正确引用来源
3. **数据备份** - 保存搜索结果
4. **网络限制** - 部分平台可能有访问限制