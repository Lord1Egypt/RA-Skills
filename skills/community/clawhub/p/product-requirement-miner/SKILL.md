---
name: product-requirement-miner
version: 1.0.0
description: 从产品评论数据中挖掘和分析迭代需求。支持CSV格式的产品评论数据，自动进行数据清洗、分类、聚类分析和产品优化路线图生成。使用场景：(1) 用户需要从产品评论中提取用户需求 (2) 对产品反馈进行分类整理 (3) 进行需求聚类分析以识别重复或相似需求 (4) 生成产品优化路线图和优先级规划。
metadata:
  openclaw:
    emoji: "📊"
    tags: ["product", "analysis", "requirements", "data-mining"]
---

# Product Requirement Miner

从产品评论中系统化挖掘迭代需求，生成可执行的产品优化路线图。

## 工作流程

### Step 1: 数据读取与分类

**读取CSV数据**

安装脚本依赖：

```bash
python -m pip install -r requirements.txt
```

执行脚本读取评论数据：

```bash
python scripts/read_csv.py <csv_file_path>
```

该脚本会：
- 自动识别CSV编码（UTF-8/GBK）
- 输出每条评论的行号和内容
- 将结果保存到 `raw_reviews.txt`

**关键词分类**

对每条评论进行处理：

1. **去噪清洗**：删除表情符号、无意义语气词、闲聊、重复内容
2. **要素提取**：提取用户信息、痛点描述、涉及功能模块
3. **自动分类**：根据内容判定为以下四种类型之一

**分类标准**（详见 `references/category_guide.md`）：

| 类别 | 定义 | 示例 |
|------|------|------|
| Bug | 产品功能错误、故障、崩溃 | "导出数据时软件闪退" |
| 建议 | 对现有功能的改进意见 | "希望导出支持Excel格式" |
| 需求 | 希望新增的功能 | "需要批量导入用户的功能" |
| 其他 | 咨询、评价、非功能相关 | "客服响应很快" |

**输出格式**：

每条评论分析结果输出为JSON格式：

```json
{
  "is_valid": true,
  "cleaned_text": "清洗后的简洁文本",
  "category": "Bug/建议/需求/其他",
  "module": "涉及的功能模块"
}
```

将所有分类结果保存为 `classified_reviews.json`

### Step 2: 筛选数据

使用 `AskUserQuestion` 工具询问用户需要提取哪一类数据：

```python
AskUserQuestion(
    questions=[{
        "question": "请选择需要提取的数据类型：",
        "header": "数据筛选",
        "options": [
            {"label": "Bug", "description": "产品功能错误和故障"},
            {"label": "建议", "description": "现有功能的改进意见"},
            {"label": "需求", "description": "希望新增的功能"},
            {"label": "全部", "description": "提取所有有效数据"}
        ],
        "multiSelect": false
    }]
)
```

根据用户选择，从 `classified_reviews.json` 中筛选对应分类数据，保存为 `filtered_data.txt`（每行一条）。

### Step 3: 聚类分析

**读取筛选数据**

读取 `filtered_data.txt`，对每条数据进行分析。

**特征扫描**

提取每条数据的：
- **核心意图**：用户想解决什么问题
- **关键对象**：涉及的具体功能/模块
- **独特属性**：与同类需求不同的细节

**聚类分组原则**：

1. **相似度阈值**：语义相似度 > 85% 或核心目标一致的项划分为同一簇
2. **识别细微差别**：目标一致但方案不同的项，标注为"变体"

**去重与整合**：

- **保留原则**：选择信息量最全、表达最清晰的作为"基准项"
- **补全逻辑**：将其他项的独特细节整合进基准项

**输出报告**（模板见 `assets/cluster_report_template.md`）：

保存为 `[产品名称]_聚类分析报告.md`

### Step 4: 生成产品优化路线图

**优先级评估标准**：

| 维度 | 权重 | 说明 |
|------|------|------|
| 用户价值 | 高 | 解决问题的用户覆盖面、痛点深度 |
| 实现成本 | 中 | 开发难度（高/中/低） |
| 战略对齐 | 中 | 是否符合当前产品阶段目标 |

**优先级定义**：

- **P0**（紧急必做）：影响核心功能、高频使用、用户严重不满
- **P1**（重要优先）：高价值、中等成本、符合战略方向
- **P2**（常规优化）：中等价值、常规改进
- **P3**（远期规划）：低价值、高成本、非当前重点

**输出路线图**（模板见 `assets/roadmap_template.md`）：

保存为 `[产品名称]_优化路线图.md`

    ## 输出文件清单

    执行完成后，生成以下文件：

    | 文件名 | 说明 |
    |--------|------|
    | `raw_reviews.txt` | 原始评论数据 |
    | `classified_reviews.json` | 分类结果（JSON格式） |
    | `filtered_data.txt` | 筛选后的数据 |
    | `[产品名称]_聚类分析报告.md` | 聚类分析结果 |
    | `[产品名称]_优化路线图.md` | 产品优化路线图 |

## 参考资料

- `references/category_guide.md` - 详细的分类标准和示例
- `assets/cluster_report_template.md` - 聚类报告模板
- `assets/roadmap_template.md` - 路线图模板
