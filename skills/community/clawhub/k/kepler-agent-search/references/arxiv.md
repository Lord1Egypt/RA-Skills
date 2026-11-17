# 学术研究搜索

## 概述

专注于学术论文和研究成果的搜索能力，适用于学术研究和技术调研。

## 支持平台

### arXiv
- **引擎标识**: `"arxiv"`
- **适用场景**: 学术论文、研究预印本、技术前沿
- **特点**: 学术资源丰富，涵盖多个学科领域

```yaml
query: "transformer attention mechanism"
engines: ["arxiv"]
max_results: 10
```

## 学科分类

arXiv 涵盖的主要学科领域：

| 分类代码 | 学科领域 | 说明 |
|----------|----------|------|
| cs.AI | 人工智能 | AI、机器学习、深度学习 |
| cs.CL | 计算语言学 | NLP、语言模型、文本处理 |
| cs.CV | 计算机视觉 | 图像处理、视觉识别 |
| cs.LG | 机器学习 | 学习算法、统计学习 |
| cs.SE | 软件工程 | 软件工程、编程语言 |
| physics | 物理学 | 物理各分支学科 |
| math | 数学 | 数学各分支学科 |
| q-bio | 定量生物学 | 生物信息学、系统生物学 |
| stat | 统计学 | 统计方法、应用统计 |

## 使用技巧

### 搜索优化
1. **关键词**: 使用英文学术关键词
2. **分类筛选**: 可使用分类代码如 `cs.AI`, `cs.CL`, `cs.LG`
3. **作者搜索**: 可搜索特定作者的研究
4. **时间筛选**: 搜索结果可按时间排序

### 论文评估
1. **引用次数**: 反映论文影响力
2. **作者背景**: 知名研究机构和学者
3. **发表时间**: 关注最新研究成果
4. **同行评审**: 注意是否为预印本（未经同行评审）

### URL 读取
- **论文页面**: `arxiv.org/abs/xxxx.xxxxx`
- **PDF下载**: `arxiv.org/pdf/xxxx.xxxxx`
- **作者页面**: 可查看作者其他论文

## 示例

```yaml
# 搜索大语言模型
query: "large language models"
engines: ["arxiv"]

# 搜索特定领域
query: "natural language processing cs.CL"
engines: ["arxiv"]

# 搜索深度学习
query: "deep learning cs.LG"
engines: ["arxiv"]

# 搜索计算机视觉
query: "image recognition cs.CV"
engines: ["arxiv"]
```

## 深度使用

### 读取论文摘要
```yaml
tool: mcp__kepler__web_reader
url: "https://arxiv.org/abs/1706.03762"
format: "markdown"
```

### 读取 PDF 内容
```yaml
tool: mcp__kepler__web_reader
url: "https://arxiv.org/pdf/1706.03762"
format: "markdown"
```

## 应用场景

### 学术研究
- 文献调研
- 研究前沿追踪
- 理论基础学习

### 技术调研
- 了解最新技术进展
- 寻找技术实现参考
- 评估技术可行性

### 论文写作
- 查找参考文献
- 了解研究方法
- 寻找合作引用

## 注意事项
- arXiv 论文为预印本，部分可能未经同行评审
- 学术引用时请注意核实论文来源
- 关注论文的更新版本（v1, v2, v3...）
- 商业应用时注意知识产权
