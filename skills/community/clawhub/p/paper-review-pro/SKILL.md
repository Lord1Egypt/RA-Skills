---
name: paper-reviewer-pro
description: 高精度论文检索与检阅系统，支持多源检索、智能筛选、结构化摘要、BibTeX 导出、CCF 评级与综合评分
license: MIT
clawhub:
  slug: paper-reviewer-pro
  repo: yourname/skills
  repoPath: skills/paper-reviewer-pro
  ref: main
  version: main
  autoEnable: true
---

# Paper Review Pro - 论文检阅系统

## 📖 简介

Paper Review Pro 是一款面向科研工作者的**智能论文检索与分析工具**。它不仅能从 arXiv 和 Semantic Scholar 多源检索论文，还能自动筛选核心文献、生成结构化摘要、评估论文权威性，并输出完整的研究领域分析报告。

**适用场景**：
- 🔍 快速了解一个新研究领域的核心文献
- 📚 系统性文献综述（Systematic Literature Review）
- 💡 探索研究方向，发现潜在创新点
- 📊 追踪领域内最新进展（按年份过滤）
- 📑 一键导出 BibTeX，快速导入 Zotero 等文献管理工具

---

## ✨ 核心优势

| 特性 | 说明 |
|------|------|
| **多源检索** | 同时检索 arXiv + Semantic Scholar，覆盖预印本与正式发表 |
| **智能筛选** | 相关度 + 权威度综合评分，自动识别高价值论文 |
| **CCF 评级** | 内置 CCF（中国计算机学会）推荐目录，自动标注 A/B/C 类 |
| **结构化摘要** | LLM 自动生成：研究问题、方法、结论、创新点 |
| **领域扩展** | 基于 Top-K 论文智能生成扩展检索词，发现相关子领域 |
| **一键导出** | 自动生成 BibTeX 文件，支持 Zotero/Mendeley 导入 |
| **完整报告** | 检索完成后自动生成研究领域分析报告 |
| **健壮性** | 多层错误处理与回退机制，确保稳定运行 |

---

## 🚀 快速开始

### 基本检索

```bash
cd ~/.openclaw/workspace/skills/paper-review-pro
python scripts/config.py
python scripts/review.py --query "LLM reasoning" --retrieve_number 20 --keep_topk 5 --year 2024
```

### 参数说明

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `--query` | ✅ | - | 检索关键词 |
| `--retrieve_number` | ❌ | 10 | 初始检索数量 |
| `--keep_topk` | ❌ | 3 | 保留核心论文数量 |
| `--year` | ❌ | 2025 | 截止年份（检索该年及之后） |
| `--expand_query_number` | ❌ | 2 | 每个扩展词保留的论文数量 |

### 输出内容

检索完成后，你将获得：

1. **Top-K 核心论文列表** - 按综合评分排序，含标题、作者、年份、摘要、链接
2. **扩展检索结果** - 基于扩展词的补充检索结果
3. **BibTeX 文件** - 自动生成，位置：`~/.openclaw/paper-review-pro/papers/bibtex_{query}_{timestamp}.bib`
4. **检索报告** - 完整的研究领域分析，位置：`~/.openclaw/paper-review-pro/reports/`

---

## 📦 功能详解

### 1. 多源检索与去重

**检索源**：
- **arXiv** - 预印本为主，覆盖最新研究
- **Semantic Scholar** - 正式发表为主，含引用信息

**去重机制**：基于论文标题和 DOI 进行本地去重，避免重复结果。

### 2. 综合评分系统

评分公式：
```
综合分数 = 相关度 × (1 - weight) + 权威度 × weight
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| **相关度** | 查询关键词与标题/摘要的匹配度 | - |
| **权威度** | 基于发表状态和 CCF 评级 | - |
| **weight** | 权威度权重 | 0.3 |

**权威度评分标准**：

| 等级 | 说明 | 分数 |
|------|------|------|
| CCF-A | 顶级会议/期刊（NeurIPS, ICML, CVPR, ACL 等） | 1.0 |
| CCF-B | 优秀会议/期刊 | 0.8 |
| CCF-C | 良好会议/期刊 | 0.6 |
| 已发表未评级 | 有 venue 但未匹配 CCF | 0.5 |
| preprint | 预印本（arXiv 等） | 0.3 |

### 3. CCF 评级查询

**数据库规模**：422 个 venue（会议 275 个，期刊 147 个）

**代表性收录**：
- **A 类会议**：NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, ACL, EMNLP, CCS, S&P, SIGMOD, VLDB, KDD 等
- **A 类期刊**：IEEE TPAMI, IJCV, JMLR, IEEE TIFS, TSE, TODS, TKDE 等

### 4. 结构化摘要生成

使用 LLM 自动生成四要素摘要：

| 要素 | 说明 |
|------|------|
| 研究问题 | 论文要解决的核心问题 |
| 方法 | 采用的技术路线/算法 |
| 结论 | 主要发现/实验结果 |
| 创新点 | 与已有工作的区别 |

### 5. 领域扩展检索

基于 Top-K 核心论文的内容分析，生成语义相关的扩展检索词，帮助发现：
- 相关子领域
- 替代技术方案
- 跨领域应用

### 6. BibTeX 导出

**自动生成**，支持一键导入 Zotero/Mendeley。

**导入 Zotero**：
1. 打开 Zotero
2. 文件 → 导入 → 从文件导入
3. 选择生成的 `.bib` 文件

---

## ⚙️ 配置与参数

### 配置文件

位置：`~/.openclaw/paper-review-pro/config.json`

```json
{
  "default_n": 10,
  "default_k": 2,
  "min_year": 2025,
  "default_p": 2,
  "authority_weight": 0.3,
  "llm": {
    "enabled": true,
    "provider": "gateway",
    "gateway_url": "http://localhost:14940",
    "gateway_model": "dashscope/qwen3.5-plus"
  }
}
```

### 快速配置命令

```bash
python scripts/config.py --default_n 20 --default_k 3 --min_year 2024 --authority-weight 0.3
```

### 命令行参数

#### 基本参数
| 参数 | 说明 |
|------|------|
| `--query` | 检索关键词（必需） |
| `--retrieve_number` | 初始检索数量 |
| `--keep_topk` | 保留核心论文数量 |
| `--year` | 截止年份 |
| `--expand_query_number` | 每个扩展词保留数量 |

#### 高级参数
| 参数 | 说明 | 默认 |
|------|------|------|
| `--no-bibtex` | 禁用 BibTeX 导出 | 启用 |
| `--no-authority` | 禁用权威度评分 | 启用 |
| `--authority-weight` | 权威度权重 (0.0-1.0) | 0.3 |
| `--use-api` | 使用在线 API 查询发表状态 | 禁用 |
| `--no-llm` | 禁用 LLM 功能 | 启用 |

---

## 🛡️ 错误处理与回退机制

本系统设计有多层错误处理机制，确保在各种异常情况下仍能稳定运行。

### 1. arXiv 检索回退

```
arXiv API (首选)
    ↓ [失败]
arXiv 网页爬取 (回退)
    ↓ [失败]
跳过 arXiv，仅使用 Semantic Scholar
```

**网页爬取保护**：
- 超时保护：60 秒
- 条目长度限制：50KB/条
- 进度输出：实时显示处理状态

### 2. LLM 功能回退

```
OpenClaw Gateway API (首选)
    ↓ [401/网络错误]
Dashscope API (备用)
    ↓ [失败]
规则提取 Fallback
```

**Fallback 行为**：
- **摘要生成**：从原文提取首尾句作为研究问题/结论，方法/创新点使用模板
- **扩展词生成**：从标题提取名词短语，基于常见学术模式生成

**保证**：即使 LLM 完全不可用，系统也能正常运行，不会中断。

### 3. 发表状态查询回退

```
在线 API 查询 (--use-api)
    ↓ [失败/未启用]
本地数据库匹配
    ↓ [未匹配]
标记为"未评级"
```

### 4. 卡死检测保护

**TimeoutMonitor** 监控所有关键步骤：
- 超时阈值：1200 秒（20 分钟）
- 监控点：检索、过滤、评分、扩展、导出、报告生成
- 超时行为：自动终止程序并输出错误信息

### 5. 网络请求重试

所有外部 API 请求均支持自动重试：
- 重试次数：3 次
- 重试间隔：指数退避（1s, 2s, 4s）

---

## 📋 使用示例

### 示例 1：标准检索
```bash
python scripts/review.py --query "transformer attention" --retrieve_number 20 --keep_topk 5 --year 2020
```

### 示例 2：仅关注内容相关性（忽略权威度）
```bash
python scripts/review.py --query "novel architecture" --keep_topk 5 --no-authority
```

### 示例 3：高权威度优先（系统性综述）
```bash
python scripts/review.py --query "deep learning survey" --keep_topk 10 --authority-weight 0.5
```

### 示例 4：快速检索（禁用 LLM）
```bash
python scripts/review.py --query "quick test" --retrieve_number 5 --no-llm
```

### 示例 5：使用在线 API 获取更准确的发表信息
```bash
python scripts/review.py --query "recent paper" --keep_topk 5 --use-api
```

---

## 🧪 测试与验证

### 测试 CCF 评级模块
```bash
# 运行完整测试套件
python scripts/test_publication_status.py

# 测试特定 venue
python scripts/test_publication_status.py --title "论文标题" --venue "IEEE Transactions on Multimedia"

# 显示数据库统计
python scripts/test_publication_status.py --show-db
```

### 测试 BibTeX 导出
```bash
python scripts/core/bibtex.py --title "Test Paper" --authors "John Doe" --year 2025 --publication "CVPR" --ccf-rank A
```

---

## 📚 参考文档

详细模块说明请参考 `reference/` 目录：

| 文档 | 内容 |
|------|------|
| [`reference/LLM_INTEGRATION.md`](reference/LLM_INTEGRATION.md) | LLM 功能集成（摘要生成、查询扩展） |
| [`reference/BIBTEX_EXPORT.md`](reference/BIBTEX_EXPORT.md) | BibTeX 导出模块说明 |
| [`reference/PUBLICATION_STATUS.md`](reference/PUBLICATION_STATUS.md) | 发表状态与 CCF 评级模块 |
| [`reference/SCORING_SYSTEM.md`](reference/SCORING_SYSTEM.md) | 综合评分系统说明 |
| [`reference/BUGFIXES.md`](reference/BUGFIXES.md) | 重要修复说明 |

---

## ⚠️ 注意事项

1. **CCF 评级数据库**：当前使用本地数据库，覆盖常见计算机领域会议/期刊。如需扩展，请编辑 `scripts/core/publication_status.py` 中的评级字典。

2. **BibTeX 文件位置**：生成的 `.bib` 文件保存在 `~/.openclaw/paper-review-pro/papers/` 目录，文件名格式：`bibtex_{查询关键词}_{时间戳}.bib`。

3. **权威度权重建议**：
   - 探索性研究：0.2-0.3（相关度优先）
   - 系统性综述：0.4-0.5（权威度优先）
   - 纯内容分析：使用 `--no-authority` 禁用

4. **在线 API 查询**：`--use-api` 参数通过 Semantic Scholar API 查询发表信息，更准确但会增加检索时间（约 2-5 秒/篇）。

5. **arXiv 速率限制**：arXiv API 有速率限制，建议检索间隔 ≥3 秒。网页爬取作为回退方案，超时保护 60 秒。

6. **LLM 配置**：首次使用前请确保 OpenClaw Gateway 或 Dashscope API 已正确配置。如未配置，系统自动降级到规则 Fallback。

---

## 📝 更新日志

详见 `CHANGELOG.md`（如有）或项目发布说明。

---

**版本**: 2026-03-29  
**许可**: MIT  
**维护**: OpenClaw Community
