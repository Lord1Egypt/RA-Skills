#!/usr/bin/env python3
"""
Write Agent - Generate high-quality manuscript from evidence.

Addresses reviewer concerns:
- Editor: structured sections, comprehensive scope, clear contribution
- Methodology: PRISMA flow, quality assessment, meta-analysis, reproducibility
- Domain: deep theory framework, complete citations, critical literature review
- Devil's Advocate: limitations, bias analysis, counter-arguments, alternative explanations
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LLM_CLIENT = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL'),
    timeout=90.0
)
LLM_MODEL = os.getenv('LLM_MODEL', 'qwen3.5-plus')


def build_citation_map(papers: List[Dict]) -> Dict[str, str]:
    """Build citation marker map with full bibliographic info."""
    citation_map = {}
    for i, paper in enumerate(papers, 1):
        authors = paper.get("authors", [])
        if authors:
            first_author = authors[0].get("name", "Unknown")
            parts = first_author.replace(",", "").split()
            last_name = parts[-1] if parts else "Unknown"
        else:
            last_name = "Unknown"

        year = paper.get("year", "n.d.")
        title = paper.get("title", "Untitled")
        venue = paper.get("venue", "")
        doi = paper.get("doi", "")
        url = paper.get("url", "")
        citation_count = paper.get("citationCount", 0)

        if len(authors) > 2:
            marker = f"[{last_name} et al., {year}]"
        elif len(authors) == 2:
            second = authors[1].get("name", "").split()[-1]
            marker = f"[{last_name} & {second}, {year}]"
        else:
            marker = f"[{last_name}, {year}]"

        citation_map[f"ref_{i}"] = {
            "marker": marker,
            "full_citation": f"{last_name} et al. ({year}). {title}. {venue}. DOI: {doi}" if doi else f"{last_name} et al. ({year}). {title}. {venue}.",
            "title": title,
            "doi": doi,
            "url": url,
            "venue": venue,
            "year": year,
            "citation_count": citation_count,
            "evidence_level": paper.get("evidence_level", "D")
        }
    return citation_map


def format_evidence_block(evidence: Dict, citation_map: Dict, max_papers: int = 25) -> str:
    """Format evidence with full citation info for prompt context."""
    papers = evidence.get("papers", [])[:max_papers]
    lines = []
    for i, p in enumerate(papers, 1):
        ref_key = f"ref_{i}"
        cite_info = citation_map.get(ref_key, {})
        marker = cite_info.get("marker", f"[Paper {i}]")
        level = p.get("evidence_level", "D")
        abstract = p.get("abstract", "No abstract")[:300]
        venue = p.get("venue", "Unknown venue")
        year = p.get("year", "Unknown")
        citations = p.get("citationCount", 0)

        lines.append(
            f"{marker} [{level}-level evidence, cited {citations} times]\n"
            f"  Title: {p.get('title', 'No title')}\n"
            f"  Venue: {venue} ({year})\n"
            f"  Abstract: {abstract}"
        )
    return "\n\n".join(lines)


# ============================================================
# Section prompts — each addresses specific reviewer concerns
# ============================================================

SECTION_PROMPTS = {

    "abstract": """你正在撰写一篇高质量学术论文的结构化摘要（Structured Abstract）。

**格式要求**（四段式，每段标注小标题）：

**Background**: 研究背景和问题陈述。说明为什么这个主题重要，当前知识空白是什么。引用1-2篇关键文献。

**Methods**: 简述研究设计、数据来源、分析方法。如果是综述，说明检索策略和纳入标准。

**Results**: 主要发现（具体数据，不要笼统）。如果有统计结果，报告效应量和置信区间。

**Conclusions**: 核心结论和实践/学术意义。不要过度声明。

**硬性约束**：
- 总长度 250-300 字
- 每个论断必须有对应的引用标记
- 不要出现"comprehensive"、"novel"等空洞形容词""",

    "introduction": """你正在撰写论文的引言（Introduction）部分。这是审稿人首先阅读的部分，必须清晰有力。

**结构要求**（漏斗式，从宽到窄）：

1. **研究背景**（约300字）：
   - 该领域的宏观背景和重要性
   - 引用领域奠基性文献（至少3篇高引用论文）
   - 建立研究的现实意义

2. **现有研究综述**（约400字）：
   - 系统梳理已有研究的主要流派和发现
   - 识别关键争议点和不一致结论
   - 指出方法论层面的差异
   - 对每项引用的研究进行批判性评价（不要只罗列）

3. **理论框架**（约200字）：
   - 本研究依托的核心理论或概念框架
   - 关键概念的操作性定义
   - 理论框架如何指导研究设计

4. **研究空白**（约200字）：
   - 明确指出现有研究的具体不足（不是笼统的"研究不足"）
   - 说明填补这个空白的价值

5. **研究目标与贡献**（约200字）：
   - 明确陈述研究问题（RQ）
   - 列出具体的、可验证的研究贡献（2-3点）
   - 不要用"首次"、"全面"等无法验证的词

6. **论文结构**（约100字）：
   - 简述后续各节内容

**硬性约束**：
- 每个论断必须有引用支撑
- 引用格式严格使用 [Author, Year] 或 [Author et al., Year]
- 至少引用8篇不同的文献
- 对引用文献要批判性分析，不要只是"XXX研究了Y""",

    "methods": """你正在撰写论文的方法（Methods）部分。审稿人最严格审查此部分，必须做到**完全可复现**。以下每一项都必须出现在最终文本中。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§1 研究设计与注册（约 200 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 明确研究类型（系统综述 / 范围综述 / 元分析）
- 遵循报告标准（PRISMA 2020 [Page et al., 2021]），给出参考文献
- 预注册编号（PROSPERO CRD42XXXXXXX）
- 如适用：伦理审批声明

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§2 检索策略（约 350 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 数据库清单（≥4 个，含 Embase / PubMed / Scopus / WoS / IEEE Xplore 等）
- **必须写出一个完整的检索式示例**，格式如下：
  ```
  数据库: PubMed / MEDLINE
  检索式: (\"artificial intelligence\"[MeSH] OR \"AI agent\"[TIAB]) AND
           (\"healthcare\"[MeSH] OR \"clinical\"[TIAB])
  检索日期: YYYY-MM-DD
  时间跨度: YYYY-01-01 至 YYYY-12-31
  ```
- 补充检索：手工检索、参考文献追溯、灰色文献

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§3 纳入与排除标准 — PICOS 表格（约 250 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**必须以 Markdown 表格呈现**：
| PICOS | 纳入 | 排除 |
|-------|------|------|
| Population | ... | ... |
| Intervention | ... | ... |
| Comparison | ... | ... |
| Outcomes | ... | ... |
| Study Design | ... | ... |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§4 PRISMA 筛选流程（约 250 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **必须报告各阶段具体数字**（不要用 XX 代替）：
  数据库检索 → 去重后 → 标题摘要筛选 → 全文筛选 → 最终纳入
- 双人独立筛选（报告 Cohen's κ 一致性）
- 冲突解决方式（第三审稿人 / 协商）
- 使用工具（Rayyan / Covidence / EndNote）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§5 质量评估（约 250 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 工具及版本：Cochrane RoB 2 / Newcastle-Ottawa Scale / CASP
- 评估维度说明
- **必须报告总体质量分布**：
  低风险 XX 篇 | 中风险 XX 篇 | 高风险 XX 篇
- 质量如何纳入综合分析（敏感性分析排除高风险）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§6 数据提取字段（约 200 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**以表格列出提取字段**：
| 字段类别 | 具体字段 |
|----------|----------|
| 基本信息 | 作者、年份、国家 |
| 研究特征 | 样本量、设计类型、随访时长 |
| 干预特征 | Agent 类型、自主程度、部署环境 |
| 结果数据 | 效应量、CI、p 值 |
双人独立提取 + 交叉验证。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§7 统计综合方法（约 350 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **效应量选择及理由**（RR vs OR vs MD，为什么选这个）
- **模型选择及理由**（随机效应 vs 固定效应，为什么选这个）
- 异质性评估：I² 统计量 + Cochran's Q 检验
  - I² < 50% 低异质性 / 50-75% 中等 / >75% 高
- 发表偏倚：漏斗图 + Egger's test（纳入≥10篇时）
- 亚组分析（预先指定的亚组变量 + 理由）
- 敏感性分析（逐篇排除法 + 排除高风险研究）
- 软件及版本（如 RevMan 5.4 / R meta 6.5-0 / Stata 18）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§8 可复现性声明（约 100 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 数据可用性（\"原始数据附于 Supplementary Material\" 或 \"可从 [链接] 获取\"）
- 代码可用性（\"分析代码开源至 GitHub: [链接]\"）
- PRISMA 流程图（\"见 Supplementary Figure S1\"）

**硬性约束**：
① 所有数字必须是具体数值（禁止 XX / TODO）
② 每个工具必须标注版本号 + 参考文献
③ 必须包含 ≥3 个表格（PICOS、提取字段、质量分布）
④ 统计方法必须说明前提条件检验""",

    "results": """你正在撰写论文的结果（Results）部分。核心原则：**只报告发现，不解释；每个数字必须溯源到具体文献**。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§1 PRISMA 流程结果（约 250 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**必须报告各阶段的具体数字**：
- 初始检索：总计 N 条（PubMed N / Scopus N / WoS N / Embase N / 其他 N）
- 去重后：N 条
- 标题摘要筛选 → 排除 N 条（原因：主题不符 N / 非英文 N / ...）
- 全文筛选 → 排除 N 条（原因：无 Agent 特征 N / 无结局指标 N / ...）
- 最终纳入：N 篇

如适用，以 Markdown 表格呈现：
| 阶段 | 数量 | 排除原因 |
|------|------|----------|

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§2 纳入研究特征（约 350 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**以表格总结纳入研究特征**：
| 特征 | 分布 |
|------|------|
| 总研究数 | N 篇 |
| 发表年份 | YYYY–YYYY（中位数 YYYY） |
| 地区分布 | 北美 N / 欧洲 N / 亚洲 N / 其他 N |
| 样本量范围 | N–N（中位数 N） |
| 研究设计 | RCT N / 队列 N / 病例对照 N / 横断面 N |
| 质量评估 | 低风险 N / 中风险 N / 高风险 N |

用 2-3 句话描述关键模式（如 \"2023 年发表量占比 52%，反映领域快速增长\"）。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§3 主要发现（约 500 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**按研究问题（RQ）逐条组织，每条必须包含**：
- 具体效应量（如 SMD = 0.18, 95% CI [0.12, 0.24]）
- 异质性（I² = XX%, Cochran's Q = XX, p = XX）
- 支撑文献的引用标记
- 如有异质性，说明亚组分析是否解释了异质性

**格式示例**：
> RQ1：AI Agent 辅助诊断的准确性
> 荟萃分析显示，AI Agent 辅助诊断的合并敏感性改善为 0.18
> (95% CI: 0.12–0.24; I² = 67%; p < 0.001) [Author, 2022; Author, 2023]。n> 亚组分析显示，放射科的改善幅度最大（SMD = 0.22, 95% CI: 0.14–0.30），n> 显著高于初级保健（SMD = 0.11, 95% CI: 0.03–0.19; Q = 12.4, p = 0.002）。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§4 亚组分析与敏感性分析（约 250 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **预先指定的亚组变量**（在 Methods 中声明的）
  每个亚组报告：效应量、CI、I²、组间差异检验 p 值
- **敏感性分析**
  逐篇排除法结果是否稳健？排除高风险研究后效应量是否改变？
  用一句话总结：\"逐篇排除后合并效应量变化范围 0.15–0.21，结论稳健。\"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§5 发表偏倚（约 150 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 漏斗图：对称 / 不对称（如有不对称，说明方向）
- Egger's test 结果：t = XX, p = XX
- Trim-and-fill 估计：需要补充 N 篇零效应研究才能恢复对称
- 结论：\"存在/不存在显著发表偏倚\"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§6 证据质量（GRADE）（约 100 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
如适用，用 GRADE 框架评估证据确定性：
| 结局 | 研究数 | GRADE 确定性 |
|------|--------|-------------|
| 诊断准确性 | N | ⬆⬆⬛⬛ 中等 |
| 行政效率 | N | ⬆⬛⬛⬛ 低 |

**硬性约束**：
① 所有数字必须有来源（哪篇文献 / 荟萃分析结果）
② 效应量必须附带 95% CI，不能只报告 p 值
③ 区分统计显著性与实际显著性
④ 本节禁止解释结果（解释留给 Discussion）
⑤ 禁止出现 \"further research is needed\" 等解释性语句""",

    "discussion": """你正在撰写论文的讨论（Discussion）部分。
这篇论文将面临一位极其严苛的 Devil's Advocate 审稿人。
你必须预先反驳这位审稿人可能提出的所有质疑。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§1 主要发现总结（约 200 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 简明重述核心发现，与每个 RQ 一一对应
- 不引入新信息、新数据、新引用

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§2 与现有文献对比（约 500 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
逐一对比，每个发现必须与 ≥2 篇已有研究比较：
- **一致结果**：说明本研究在什么维度上推进了（更大样本？更新方法？不同人群？）
- **不一致结果**：深入分析原因（方法差异？样本差异？时间差异？定义差异？）
  **必须引用与本研究结论相反的文献**（至少 1 篇），说明为什么本研究结论仍然成立

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§3 理论贡献（约 300 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 本研究对理论框架的启示（支持/挑战/扩展）
- 提出的新假设或理论修正
- 不要泛泛而谈，必须具体说明哪些理论假设被验证/修正

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§4 实践意义（约 200 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 从业者的具体可操作建议
- 政策制定者的启示
- 必须与具体发现挂钩（不能空泛建议）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§5 自我反驳 — 最强反面论据（约 400 字）★★★ 最关键
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**你必须主动扮演 Devil's Advocate，提出 3-5 个对本研究的最强反驳论点。**
每个反驳必须按以下格式：

> **反驳论点 N**：[提出一个严密的反对理由]
> - 支撑证据：[引用与本研究相反的文献，或提出逻辑推理]
> - 严重程度：[致命 / 严重 / 中等]
> - 本研究的回应：[承认其有效性，并解释本研究如何减轻此问题，或诚实承认无法完全解决]

**必须包含的反驳类型**：
① 方法学反驳（如：\"观察性研究占 74%，因果推断不可靠\"）
② 数据反驳（如：\"I²=67% 说明结果不一致，合并效应量可能有误导\"）
③ 效应反驳（如：\"0.18 的敏感性改善可能被霍桑效应夸大\"）
④ 外推性反驳（如：\"单国/单中心结果不能推广\"）
⑤ 技术反驳（如：\"AI Agent 定义过于宽泛，可能纳入了非真正 Agent 的研究\"）

**不要回避、不要轻描淡写、不要用套话。**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§6 偏差矩阵 — 系统性偏差分析（约 300 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**以表格形式呈现**：

| 偏差类型 | 存在? | 对结论的影响 | 减轻措施 |
|----------|-------|-------------|----------|
| 选择偏差 | 是/否 | ... | ... |
| 发表偏差 | 是/否 | ... | Egger's test |
| 确认偏差 | 是/否 | ... | ... |
| 语言偏差 | 是/否 | ... | ... |
| 时间偏差 | 是/否 | ... | ... |
| 霍桑效应 | 是/否 | ... | ... |
| 行业资助偏差 | 是/否 | ... | ... |

对每项偏差，诚实评估其对结论的**方向性影响**（夸大/缩小效应量）。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§7 过度声明自查清单（约 150 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
逐条检查以下常见过度声明，确认你的论文没有犯：
- ❌ \"首次\" / \"first\" → 除非你有文献检索证明
- ❌ \"全面\" / \"comprehensive\" → 除非你真的覆盖了所有数据库和语言
- ❌ \"证明了\" / \"proves\" → 观察性研究只能\"支持\"假说，不能\"证明\"
- ❌ \"显著改善\" → 必须区分统计显著性和临床/实际显著性
- ❌ 将关联性表述为因果性
- ❌ 将小样本结论外推到大群体
在文中声明：\"本研究避免了以下过度声明...\"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§8 替代解释（约 200 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
对主要发现提出 ≥2 个合理的替代解释：
- 替代解释 1：[具体解释] → 为什么可能 → 本研究倾向当前解释的理由
- 替代解释 2：[具体解释] → 为什么可能 → 本研究倾向当前解释的理由
- 承认：\"不能完全排除这些替代解释，需要未来研究验证\"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§9 未来研究方向（约 200 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 基于具体局限性提出具体改进（不能写\"需要更多研究\"）
- 提出 2-3 个新的具体研究问题（含建议的研究设计）
- 每条必须可操作（如：\"建议开展多中心 RCT，样本量 ≥N，随访 ≥12 月\"）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
§10 结论（约 100 字）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 一句话核心发现 + 一句话意义
- 禁止过度声明
- 禁止出现 \"further research is needed\" （已在 §9 写过）

**硬性约束**：
① §5 自我反驳 ≥3 个具体反驳论点（含反面文献引用）
② §6 偏差矩阵 ≥5 种偏差类型
③ §7 过度声明自查至少声明 3 项
④ §8 替代解释 ≥2 个
⑤ 禁止空洞套话（\"需要更多研究\"、\"further research\"、\"comprehensive\"）
⑥ 局限性必须分析**对结论的方向性影响**"""
}


def generate_section(
    section_name: str,
    topic: str,
    evidence: Dict,
    citation_map: Dict,
    prev_sections: Optional[Dict[str, str]] = None
) -> str:
    """Generate a single section with rigorous academic standards."""

    prev_sections = prev_sections or {}
    evidence_text = format_evidence_block(evidence, citation_map)

    # Build context from previously generated sections (continuity)
    context_block = ""
    if prev_sections:
        context_lines = []
        for name, content in prev_sections.items():
            context_lines.append(f"[{name}摘要]: {content[:400]}...")
        context_block = "\n\n已生成的前置章节摘要（保持连贯性）：\n" + "\n".join(context_lines)

    section_instruction = SECTION_PROMPTS.get(section_name, f"撰写{section_name}部分，确保学术严谨性。")

    prompt = f"""你是一位资深学者，正在撰写关于「{topic}」的高质量学术论文。

{section_instruction}

**可用文献证据**（按证据等级和引用次数排序）：
{evidence_text}
{context_block}

**全局写作规范**：
- 学术写作风格，客观严谨
- 引用格式严格使用 [Author, Year] 或 [Author et al., Year]
- 每个事实性论断必须有引用支撑
- 区分"本研究发现"和"文献报告"的发现
- 不要使用空洞的形容词（comprehensive, novel, groundbreaking等）
- 输出 Markdown 格式

直接输出内容，不要解释。"""

    try:
        response = LLM_CLIENT.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2500  # Increased from 1500 for longer, more detailed sections
        )

        return response.choices[0].message.content or ""

    except Exception as e:
        print(f"  ⚠️ {section_name} generation failed: {e}")
        return f"\n## {section_name.title()}\n\n[Generation failed: {e}]\n"


def write_manuscript(topic: str, evidence_file: str, output_dir: str = "draft") -> str:
    """Generate complete manuscript with section continuity."""
    print(f"✍️ Writing manuscript for: {topic}")

    # Load evidence
    evidence = json.loads(Path(evidence_file).read_text())
    papers = evidence.get("papers", [])

    if not papers:
        print("  ❌ No papers in evidence file - cannot generate manuscript")
        return ""

    # Build citation map
    citation_map = build_citation_map(papers)

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Generate each section with context from previous sections
    sections = ["abstract", "introduction", "methods", "results", "discussion"]
    manuscript_parts = []
    prev_sections = {}  # Track generated content for continuity

    for section in sections:
        print(f"  Generating {section}...")
        content = generate_section(section, topic, evidence, citation_map, prev_sections)
        prev_sections[section] = content
        manuscript_parts.append(f"\n## {section.title()}\n\n{content}")

    # Generate title
    title = f"# {topic}: A Systematic Review and Meta-Analysis\n"

    # Generate proper references section (APA style)
    references = "\n## References\n\n"
    for ref_id, ref_data in citation_map.items():
        references += f"{int(ref_id.split('_')[1])}. {ref_data['full_citation']}\n"

    # Combine
    full_manuscript = title + "\n".join(manuscript_parts) + references

    # Save
    output_file = Path(output_dir) / "manuscript.md"
    Path(output_file).write_text(full_manuscript)

    # Save citation map for integrity check
    citation_file = Path(output_dir) / "citations.json"
    Path(citation_file).write_text(json.dumps(citation_map, indent=2))

    # Save word count stats
    total_words = len(full_manuscript.split())
    print(f"  ✅ Manuscript saved to {output_file}")
    print(f"     Total words: ~{total_words}")
    print(f"     Sections: {len(sections)}")
    print(f"     References: {len(citation_map)}")

    return str(output_file)


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: python write.py <topic> <evidence_file> [output_dir]")
        sys.exit(1)

    topic = sys.argv[1]
    evidence_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "draft"

    manuscript_file = write_manuscript(topic, evidence_file, output_dir)

    if manuscript_file:
        print(f"\n✅ Manuscript generated - proceed to Integrity Check stage")
        print(f"   Run: python integrity_check.py {manuscript_file}")


if __name__ == "__main__":
    main()
