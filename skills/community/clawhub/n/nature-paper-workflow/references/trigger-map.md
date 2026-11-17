# 阶段触发关键词完整表

> 配套主 skill: [SKILL.md](../SKILL.md)
> v2.0.0 新增：经济学分支触发词

## STEM 分支触发关键词

| 阶段 | 关键词 | 路由目标 |
|---|---|---|
| 0a 读论文 | 读论文 / 精读 / 中英对照 / paper reader | `nature-reader` |
| 0b 文献调研 | 文献调研 / 综述 / 找文献 / literature review / PubMed / Scopus | `nature-academic-search` + `academic-researcher` |
| 0b 论文下载 | 论文下载 / 下载 paper | `nature-downloader` |
| 0b 论文卡片 | 论文卡片 / 整理文献 / paper card | `nature-paper-card` |
| 1a 项目初始化 | 项目初始化 / 新论文 / bootstrap / 项目目录 | `paper-bootstrap` |
| 1b 期刊选择 | 期刊选择 / venue / Nature Methods / 投哪本 | `nature-portfolio-playbook` |
| 2a 起草 | 起草 / 写摘要 / 写引言 / 写方法 / 写讨论 / 投稿包 / cover letter | `nature-writing` |
| 2b 结构修复 | 结构修复 / 证据链漂移 / manuscript optimizer | `manuscript-optimizer` |
| 2c Results 修订 | Results 修订 / results section / 结果叙述 | `results-section-revision` |
| 3a 图规划 | 图规划 / 一图一主张 / panel role / figure planner | `figure-planner` |
| 3b 出图 | 出图 / 科研绘图 / 论文 figure / 论文 plot / 图形摘要 / 示意图 | `nature-figure` |
| 3c 图检查 | 图检查 / figure style / 图形正确性 | `figure-style` |
| 4a 统计审计 | 统计审计 / stats audit / p值 / 样本量 / n值 / 多重比较 | `stats-reporting-audit` |
| 4b 统计分析 | 统计分析 / 数据分析 / statistics / data analysis | `nature-statistics` + `nature-data` |
| 5a 引用核验 | 引用核验 / citation verifier / 引用造假 / BibTeX 卫生 | `nature-ref-verifier` + `citation-verifier` |
| 5b 引用补充 | 引用补充 / 加引用 / CNS 引用 / Nature 引用 | `nature-citation` |
| 5c 数据声明 | 数据声明 / data availability / FAIR / accession | `data-availability` |
| 6a 润色 | 润色 / polishing / 学术英语 / LaTeX 排版 / 句子精修 | `nature-polishing` + `scientific-prose-style` |
| 6b 投稿预检 | 投稿预检 / submission audit / 投前检查 | `submission-audit` |
| 7a 审稿模拟 | 审稿模拟 / reviewer / 预审 / 审稿意见 | `nature-reviewer` |
| 7b 返修 | 返修 / rebuttal / response / 逐点回复 / cover letter | `nature-response` |
| D1 转 PPT | 转 PPT / 组会汇报 / 文献汇报 | `nature-paper2ppt` |
| D2 转专利 | 转专利 / paper to patent / 国知局 | `nature-paper-to-patent` |
| D3 写基金 | 写基金 / proposal / 申请书 | `nature-proposal-writer` |
| D4 实验记录 | 实验记录 / experiment log | `nature-experiment-log` |
| D5 会议论文 | 会议论文 / NeurIPS / ICML / ICLR / conference | `conference-paper-writing` |

## Econ 分支触发关键词（v2.0.0 新增）

### 学科信号触发词（Pre-Phase 学科识别用）

下列任一词命中且未命中 STEM 信号时，进入 Econ 分支：

#### 方法名信号
| 关键词 | 类别 |
|---|---|
| DiD / 双重差分 | 因果识别 |
| IV / 工具变量 | 因果识别 |
| RDD / 断点回归 | 因果识别 |
| RCT / 随机对照试验 | 因果识别 |
| event study / 事件研究 | 动态效应 |
| synthetic control / 合成控制 | 反事实 |
| panels / 面板数据 | 数据结构 |
| binscatter | 可视化 |

#### 统计概念信号
- 基准回归 / 稳健性检验 / 机制检验 / 异质性分析
- 平行趋势 / 安慰剂 / 弱工具变量 / 第一阶段 / F 统计量
- 聚类标准误 / 固定效应 / 时间固定效应 / 个体固定效应

#### 期刊名信号
- 中文顶刊：经济研究 / 管理世界 / 中国工业经济 / 经济学季刊
- 英文顶刊：AER / QJE / JPE / Econometrica / REStud / AEJ / Journal of Finance / Journal of Public Economics

#### 学术角色信号
- Cochrane / McCloskey / Shapiro / Bellemare / Goldin / Glaeser / Kremer

#### 文件类型信号
- `.dta`（Stata 数据）/ `.do` / `.dofile`（Stata 脚本）
- `.R` / `.Rmd`（R 脚本，需配合经济学上下文）

### E-Phase 阶段触发词

| 阶段 | 关键词 | 路由目标 |
|---|---|---|
| E-0 输入审计 | 经济学论文 / econ paper / 经济学写作 / 写经济学论文 / 输入审计 | `econ-writing-workflow` |
| E-1 全文起草 | 起草 / 写摘要 / 写引言 / 写方法 / 写实证 / 写讨论 / 写结论 / 投稿包 / cover letter | `econ-write`（英）/ `cn-top-econ-writing`（中） |
| E-2 表图设计 | 表图设计 / 三线表 / 回归表 / 事件研究图 / 平行趋势图 / 地图 / 经济学图 | `econ-table-figure-design` |
| E-3 论证审计 | 论证审计 / argument audit / 论证逻辑 / claim 检查 / magnitude check | `econ-writing-workflow` |
| E-4 期刊适配 | 期刊适配 / 投稿体例 / 经济研究体例 / 管理世界体例 / AER 体例 / submission format | `cn-top-econ-writing`（中）/ `econ-write`（英） |
| E-5 审稿+返修 | 审稿模拟 / 预审 / 审稿意见 / 返修 / rebuttal / response / 逐点回复 | `nature-reviewer`（共享）+ `nature-response`（共享） |

## 跨学科共享触发词（两个分支都触发）

| 功能 | 关键词 | 路由目标 | 说明 |
|---|---|---|---|
| 项目初始化 | 项目初始化 / 新论文 / bootstrap / 项目目录 | `paper-bootstrap` | 跨学科通用 |
| 引用核验 | 引用核验 / citation verifier / BibTeX 卫生 | `nature-ref-verifier` + `citation-verifier` + `reference-audit-guide` | 跨学科通用 |
| 投稿预检 | 投稿预检 / submission audit / 投前检查 | `submission-audit` | 跨学科通用 |
| 审稿模拟 | 审稿模拟 / reviewer / 预审 | `nature-reviewer` | 跨学科通用，按学科视角调整 |
| 返修回复 | 返修 / rebuttal / response / 逐点回复 | `nature-response` | 跨学科通用 |

## 触发词设计原则

### STEM 触发词原则
- 单字英文词（如 figure / plot / reviewer / response）必须搭配上下文限定词（如"论文 figure"、"reviewer 审稿"）避免误触发
- 中文触发词优先（更精确）
- 衍生场景触发词包含具体场景名（NeurIPS / ICML / ICLR / 国知局）

### Econ 触发词原则（v2.0.0 新增）
- **方法名优先**：经济学方法名（DiD / IV / RDD / RCT）是强信号，单独出现即可触发
- **期刊名双校验**：经济学期刊名（AER / 经济研究）需配合上下文校验，避免与医学期刊名冲突
- **学科冲突仲裁**：当 STEM 与 Econ 信号同时出现时，按 [discipline-routing.md](discipline-routing.md#信号冲突仲裁) 仲裁

### 冲突消解示例
- "DiD 分析医疗政策" → Econ 分支（方法为主导）
- "投 Nature Methods 讲 DiD 方法学" → STEM 分支（期刊为导向）
- "用经济学方法分析基因数据" → 问 1 个问题确认
