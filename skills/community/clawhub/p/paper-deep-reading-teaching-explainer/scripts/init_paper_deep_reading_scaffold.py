from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "paper-deep-reading"


def ensure_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def normalize_unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        value = value.strip()
        if value and value not in result:
            result.append(value)
    return result


def template_text(filename: str) -> str:
    path = Path(__file__).resolve().parents[1] / "schemas" / filename
    return path.read_text(encoding="utf-8")


def template_json(filename: str) -> dict:
    return json.loads(template_text(filename))


def build_delivery_manifest(
    workspace_root: Path,
    bundle_zip: str = "",
    authoritative_handoff_artifacts: list[str] | None = None,
) -> dict:
    manifest = template_json("delivery_bundle_manifest.template.json")
    manifest["workspace_root"] = str(workspace_root.resolve())
    manifest["delivery_bundle_zip"] = bundle_zip
    if authoritative_handoff_artifacts is not None:
        manifest["authoritative_handoff_artifacts"] = normalize_unique(authoritative_handoff_artifacts)
    manifest["notes"] = normalize_unique(
        list(manifest.get("notes", []))
        + [
            "Restart contract: downstream callers should read delivery_bundle_manifest, routing_status, stage_delivery_handoff, and project_directory_index before scanning the tree.",
            "A fresh session should be able to continue with only this bundle plus the declared status and directory-description artifacts.",
        ]
    )
    return manifest


def refresh_project_directory_index(workspace_root: Path) -> None:
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "update_project_directory_index.py"
    subprocess.run(
        [
            sys.executable,
            str(script_path),
            str(workspace_root),
            "--default-stage",
            "chatgpt_paper_deep_reading_skill_source",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def render_report_stub(paper_title: str, paper_id: str, paper_slug: str, existing_collection_root: str) -> str:
    collection_note = existing_collection_root or "[fill collection root if any]"
    return "\n".join(
        [
            f"# {paper_title} 详细精读",
            "",
            "<!-- 写作要求：不要过于简介，必须紧扣论文本身的具体公式、模块、图表、实验与措辞展开 -->",
            "",
            "## 论文信息",
            "",
            f"- 论文 ID：{paper_id or '[fill paper id]'}",
            f"- 标题：{paper_title}",
            "- 会议 / 年份 / 状态：",
            "- OpenReview / DOI / 主页：",
            "- arXiv / PDF / LaTeX：",
            "- 作者：",
            "- 团队 / 机构线索：",
            f"- 现有 collection root：{collection_note}",
            "- 优先使用的源文件：",
            "- review / rebuttal 来源：",
            "- 当前来源缺口：",
            "",
            "## 论文标题解读",
            "",
            "- 标题关键词逐项解释：",
            "- 标题为什么这样命名：",
            "- 标题与方法、任务设定、主张之间的对应关系：",
            "",
            "## 这篇论文真正解决的是什么",
            "",
            "### 具体问题",
            "",
            "- 论文真正要解决的具体问题：",
            "- 为什么旧 formulation 不够：",
            "",
            "### 更上位的科学问题",
            "",
            "- direction-native problem：",
            "- adjacent parent-field problem：",
            "- broader ML/AI scientific problem：",
            "",
            "### 为什么这不是一个更窄的工程问题",
            "",
            "-",
            "",
            "## 论文中提到的其他论文做了什么、留下了什么空白、与本文是什么关系",
            "",
            "- 反复被提及的关键文献：",
            "- 它们分别解决了什么：",
            "- 它们仍然留下了什么空白：",
            "- 当前论文是继承、对比、融合还是转移了它们：",
            "",
            "## 核心方法到底在干什么",
            "",
            "- 核心判断 / 核心直觉：",
            "- 方法结构拆解：",
            "- key modules：",
            "- 哪些模块设计更像作者的主观取舍，而不是唯一合理方案：",
            "- training pipeline：",
            "- inference / deployment path：",
            "- optimization objectives：",
            "- communication / system path（如果相关）：",
            "- 关键结构图 / 流程图 / 定性图（来自 PDF 或 LaTeX）的解释：",
            "- 图与主张之间的对应关系：",
            "",
            "## 公式保留与逐式解释",
            "",
            "- 必须保留的关键公式列表：",
            "- 公式 1（原文/等价重写）：",
            "  - 每个符号 / 项的含义：",
            "  - 这个公式在方法中的作用：",
            "  - 它对应算法哪一步：",
            "- 公式 2（原文/等价重写）：",
            "  - 每个符号 / 项的含义：",
            "  - 这个公式在方法中的作用：",
            "  - 它对应算法哪一步：",
            "- 哪些公式只是理论分析对象，哪些公式直接进入实现：",
            "- 哪些公式 / 理论对象的选择可能带有作者主观偏好、建模习惯或证明策略：",
            "",
            "## 具体公式、模块与设计假设的不足及可改进空间",
            "",
            "- 公式层面的不足：",
            "  - 哪些项可能过强、过松、欠识别或欠论证：",
            "  - 哪些地方只是启发式拼接：",
            "  - 哪些公式可能带来优化困难、数值不稳定或额外代价：",
            "- 模块层面的不足：",
            "  - 哪些模块可能冗余、脆弱、难扩展、难复用：",
            "  - 哪些模块与论文声称的科学目标并不完全对齐：",
            "- 关键假设层面的不足：",
            "  - 哪些假设过强、隐藏、仅在特定数据/系统下成立：",
            "- 可以怎么改：",
            "  - 可替代公式 / 目标函数 / 正则项：",
            "  - 可替代模块 / 路径 / 机制：",
            "  - 改进后的潜在 trade-off：",
            "",
            "## 创新点、核心主张与证据逐条核对",
            "",
            "- 创新点 1：",
            "  - 对应主张：",
            "  - 支撑证据类型（理论 / 实验 / 可视化 / rebuttal / narrative）：",
            "  - 支撑强度：",
            "- 创新点 2：",
            "  - 对应主张：",
            "  - 支撑证据类型（理论 / 实验 / 可视化 / rebuttal / narrative）：",
            "  - 支撑强度：",
            "- 哪些主张证据不足或只被间接支持：",
            "",
            "## 这篇论文为什么重要 / 为什么值得被接收",
            "",
            "- scientific significance：",
            "- 它挑战了什么假设 / 保留了什么假设：",
            "- 为什么 reviewer / PC 会 care：",
            "",
            "## 实验是如何被设计出来的",
            "",
            "### 实验目的 / 验证链条 1",
            "",
            "-",
            "",
            "### 实验目的 / 验证链条 2",
            "",
            "-",
            "",
            "### 实验目的 / 验证链条 3",
            "",
            "-",
            "",
            "- 主实验在证明什么：",
            "- bridge experiments 在证明什么：",
            "- 哪些 ablation 真正支撑了机制：",
            "- 证据和 claim 之间还差什么：",
            "- 比较算法与引言 / 相关工作里的算法是什么关系：",
            "- 哪些实验现象有趣、反常或有争议：",
            "- 关键表格 / 曲线 / 图像分别在说明什么：",
            "- 每个关键图表的坐标轴、图例、比较条件意味着什么：",
            "- 哪些图表真正支持主张，哪些只是部分支持：",
            "- 哪些图表与主张存在张力或不一致，可能原因是什么：",
            "",
            "## 倒推作者怎么想到这个 idea",
            "",
            "- borrowed algorithm lineage：",
            "- 哪些地方更像作者的主观判断、经验偏好、工程取舍或研究风格，而非客观唯一解：",
            "- idea genesis trace：",
            "- 为什么这个想法会自然出现：",
            "- 可能受哪些论文、方法或更高层问题启发：",
            "- related papers worth linking：",
            "",
            "## 研究方程与缺失机制替代",
            "",
            "- 重要设定 Important Setting：",
            "- 被打破的旧假设 Broken Assumption：",
            "- 被借用但不能直接迁移的工具 Borrowed Tool：",
            "- 新约束 New Constraint：",
            "- easier setting 中可用的理想机制 `Y`：",
            "- 本文构造的替代机制 `Z`：",
            "- 为什么 `Z` 可以近似 / 替代 `Y`：",
            "- 研究方程：`A(P) ∩ ¬C ∩ T ∩ M ⇒ Z ≈ Y`：",
            "",
            "## 作者可能如何发现这个方向",
            "",
            "- valuable field：",
            "- painful assumption：",
            "- emerging / borrowed tool：",
            "- unserved setting：",
            "- blocking constraint：",
            "- conceptual replacement：",
            "- 哪些判断有论文文本证据支撑，哪些只是合理推测：",
            "",
            "## 论文故事线如何搭建",
            "",
            "| Challenge | Failure mode | Design principle | Module | Evidence |",
            "|---|---|---|---|---|",
            "|  |  |  |  |  |",
            "",
            "- narrative escalation：",
            "- additive story 还是 closed-loop story：",
            "- 在模块之间流动的核心对象（pseudo-label / generated data / graph consensus / uncertainty / prototype 等）：",
            "- 哪些故事连接仍然脆弱：",
            "",
            "## 模块级作者思路深读",
            "",
            "| Module | Failure fixed | Ideal unavailable solution | Available proxy | Design choice | Hidden assumption | Risk | Future research point |",
            "|---|---|---|---|---|---|---|---|",
            "|  |  |  |  |  |  |  |  |",
            "",
            "## 关键引用的叙事功能与 Citation-to-Module Map",
            "",
            "| Citation cluster | Narrative function | Assumption inherited | How this paper modifies it | Related module |",
            "|---|---|---|---|---|",
            "|  |  |  |  |  |",
            "",
            "## 实验作为故事证据",
            "",
            "| Experiment block | Claim | Counterfactual | Metric | Stress condition | Module justified | Support judgment |",
            "|---|---|---|---|---|---|---|",
            "|  |  |  |  |  |  |  |",
            "",
            "## 可复用的论文造故事模式",
            "",
            "- old success + new reality -> old assumption breaks：",
            "- replacement story：`Y` unavailable, so design `Z`：",
            "- two-axis empty cell：",
            "- closed-loop contribution pattern：",
            "- 这套模式如何迁移到下一篇论文 / 新选题：",
            "",
            "## 从隐藏假设生成新 idea",
            "",
            "| Hidden assumption `H_i` | Why current method needs it | Setting under `¬H_i` | Required new mechanism | Engineering / cross-domain / boundary-pushing | New research question |",
            "|---|---|---|---|---|---|",
            "|  |  |  |  |  |  |",
            "",
            "## 作者主观判断与研究风格关联分析",
            "",
            "- where choices look author-specific：",
            "- objective necessity vs author choice：",
            "- evidence-backed subjective inference：",
            "- author style or research taste signals：",
            "",
            "## 报告具体性要求：必须紧扣论文中的公式、模块、图表、实验与措辞",
            "",
            "- concrete formula / module / dataset / baseline mentions：",
            "- figure / table / experiment specifics：",
            "- theorem object and assumption specificity：",
            "- 避免空泛抽象总结的自检：",
            "",
            "## 审稿人最关注什么",
            "",
            "- concern 1：",
            "- concern 2：",
            "- concern 3：",
            "- concern 4：",
            "",
            "## 额外审稿视角审计（借鉴 GitHub 热门审稿 skill 的 reviewer 关注点）",
            "",
            "- novelty / significance 审计：",
            "- technical soundness / methodology rigor 审计：",
            "- reproducibility / missing details 审计：",
            "- results-claims alignment 审计：",
            "- missing baselines / controls 审计：",
            "- figure / table clarity 与 limitations honesty 审计：",
            "",
            "## 作者是怎么回复的",
            "",
            "- reply 1：",
            "- reply 2：",
            "- reply 3：",
            "",
            "## 审稿人是否认同作者回复",
            "",
            "- meta-review / decision signal：",
            "- 哪些点被解决了：",
            "- 哪些点仍 unresolved：",
            "",
            "## 审稿意见回复覆盖核对",
            "",
            "- concern -> reply -> resolution：",
            "- concern -> reply -> resolution：",
            "- coverage conclusion：",
            "",
            "## 这篇论文最强的地方",
            "",
            "### 强点 1",
            "",
            "-",
            "",
            "### 强点 2",
            "",
            "-",
            "",
            "### 强点 3",
            "",
            "-",
            "",
            "## 这篇论文的弱点 / 不足",
            "",
            "### 弱点 1",
            "",
            "-",
            "",
            "### 弱点 2",
            "",
            "-",
            "",
            "### 弱点 3",
            "",
            "-",
            "",
            "- 未解决问题：",
            "- failure modes / scope limits：",
            "- structural limitations：",
            "- open risks：",
            "",
            "## 作者团队近年的相关延续",
            "",
            "- follow-up papers / repos / lab agenda：",
            "- 哪个 continuation signal 最重要：",
            "",
            "## 从这篇论文出发，最值得突破的未来边界",
            "",
            "### 方向 1",
            "",
            "-",
            "",
            "### 方向 2",
            "",
            "-",
            "",
            "### 方向 3",
            "",
            "-",
            "",
            "- 哪些方向只是工程延展：",
            "- 哪些方向可能真正推动科学边界：",
            "",
            "## 创新类型判断：这是增量创新、交叉创新，还是边界突破",
            "",
            "- 创新类型判断：",
            "- 为什么属于增量 / 交叉 / 边界突破：",
            "- 是否突破了学科或子领域边界：",
            "- 这种判断的局限：",
            "",
            "## 对选题的直接启示",
            "",
            "- borrowable mechanisms：",
            "- next experiments：",
            "- 什么应该进入 graph stage：",
            "",
            "## 可能的新研究方向或新创新点（尤其是可能推动科学边界的方向）",
            "",
            "- 原生延展：",
            "- 交叉迁移：",
            "- 混合路线：",
            "- 高风险高回报想法：",
            "- 哪些方向最可能推动科学边界，以及为什么：",
            "",
            "## 面向讲解的受众画像与讲解目标",
            "",
            "| Audience | What they know | Likely confusion | What to explain first | Math depth | Evidence that convinces them |",
            "|---|---|---|---|---|---|",
            "| 技术读者 / 跨方向研究生 |  |  |  |  |  |",
            "| 审稿人 / 导师 |  |  |  |  |  |",
            "| 初学者 |  |  |  |  |  |",
            "",
            "## 3 层讲解摘要：30 秒 / 3 分钟 / 10 分钟",
            "",
            "### 30 秒版本",
            "",
            "-",
            "",
            "### 3 分钟版本",
            "",
            "- problem -> broken assumption -> key idea -> evidence -> caveat：",
            "",
            "### 10 分钟版本",
            "",
            "- 加入方法模块、关键公式、主要实验、限制：",
            "",
            "## 讲解主线 Story Spine",
            "",
            "- Before this paper：",
            "- Pain / broken assumption：",
            "- Tempting but blocked path：",
            "- Key replacement `Y -> Z`：",
            "- Mechanism：",
            "- Evidence：",
            "- Caveat：",
            "- Next idea：",
            "",
            "## 听众先修知识与概念铺垫",
            "",
            "- 最少需要知道的任务设定：",
            "- 最少需要知道的符号：",
            "- 最少需要知道的数据集 / benchmark / metric：",
            "- 最容易误解的领域惯例：",
            "- 建议讲解顺序：",
            "",
            "## 公式 / 图表 / 实验的讲解脚本",
            "",
            "### 公式讲解表",
            "",
            "| Formula | What problem it solves | Term-by-term meaning | How to say it aloud | Algorithm role | What can go wrong |",
            "|---|---|---|---|---|---|",
            "|  |  |  |  |  |  |",
            "",
            "### 图表讲解表",
            "",
            "| Visual | First thing to point at | Listener confusion risk | Claim supported | What not to overclaim | Verbal explanation |",
            "|---|---|---|---|---|---|",
            "|  |  |  |  |  |  |",
            "",
            "### 实验讲解单元",
            "",
            "- 实验回答的问题：",
            "- 审稿人 / 听众可能的质疑：",
            "- setup / dataset / baseline / metric：",
            "- 如果论文主张成立，预期应该看到什么：",
            "- 实际结果：",
            "- 它证明了什么：",
            "- 它没有证明什么：",
            "",
            "## 板书推导与小例子演示",
            "",
            "- mini-case 设置：",
            "- 输入 / 状态 / 输出：",
            "- Step 1：",
            "- Step 2：",
            "- Step 3：",
            "- 这个例子揭示了什么：",
            "- 简化例子在哪些地方会误导：",
            "",
            "## 角色扮演式讨论问题",
            "",
            "| Role | What this role checks | Discussion question | Expected answer / evidence |",
            "|---|---|---|---|",
            "| Archaeologist | prior-work ancestry |  |  |",
            "| Bug Hunter | rigor / reproducibility / clarity |  |  |",
            "| Researcher | future direction |  |  |",
            "| Industry Practitioner | cost and deployment |  |  |",
            "| Social Impact Assessor | risk and impact |  |  |",
            "| Author Defender | acceptance logic |  |  |",
            "| Teacher | learnability |  |  |",
            "",
            "## 可能被问到的问题与回答证据",
            "",
            "| Question | Audience | Evidence-backed answer | Confidence | What the paper does not prove |",
            "|---|---|---|---|---|",
            "|  | beginner |  |  |  |",
            "|  | peer |  |  |  |",
            "|  | advisor / reviewer |  |  |  |",
            "|  | practitioner |  |  |  |",
            "",
            "## 易误解点与纠偏",
            "",
            "- 论文没有声称：",
            "- 类比在哪些地方会失效：",
            "- 哪个结果不能泛化到未测试设定：",
            "- 哪个模块容易被误认为是全部贡献：",
            "- 哪个 baseline / ablation 容易被过度解读：",
            "- 讲的时候必须主动说出的限制：",
            "",
            "## PPT / 分享稿结构草案",
            "",
            "| Slide | Title | One-sentence point | Visual / formula | Speaker notes | Transition | Likely question |",
            "|---|---|---|---|---|---|---|",
            "| 1 | Why care? |  |  |  |  |  |",
            "| 2 | Problem setting |  |  |  |  |  |",
            "| 3 | Broken assumption |  |  |  |  |  |",
            "| 4 | Core idea |  |  |  |  |  |",
            "| 5 | Method |  |  |  |  |  |",
            "| 6 | Evidence |  |  |  |  |  |",
            "| 7 | Limitations |  |  |  |  |  |",
            "| 8 | Future directions |  |  |  |  |  |",
            "| 9 | Takeaways |  |  |  |  |  |",
            "",
            "## 听众可带走的三句话",
            "",
            "1. ",
            "2. ",
            "3. ",
            "",
            "## 最后一段通俗故事总结",
            "",
            "- 用通俗、生动的语言重述这篇论文：",
            "",
            "## 参考来源",
            "",
            "- primary sources：",
            "- supporting sources：",
            "",
            "<!-- paper-deepread-structured-appendix:start -->",
            "",
            "## 结构化补充附录",
            "",
            "### 上位科学问题定位的三条证据链",
            "",
            "- paper-explicit path：",
            "- borrowed-algorithm ancestry path：",
            "- new-algorithm bottleneck path：",
            "",
            "### 统一后的更高层 AI/ML 问题",
            "",
            "-",
            "",
            "### 借鉴算法所属上位问题",
            "",
            "-",
            "",
            "### 新算法遇到的问题所对应的上位问题",
            "",
            "-",
            "",
            "### 模块到问题、算法与瓶颈的映射",
            "",
            "- module -> problem：",
            "- module -> algorithm lineage：",
            "- module -> bottleneck：",
            "",
            "### 知识图谱节点与关系候选",
            "",
            "- graph node candidates：",
            "- graph relation candidates：",
            "",
            "### 研究方程与缺失机制替代",
            "",
            "- Important Setting + Broken Assumption + Borrowed Tool + New Constraint + Surrogate Mechanism：",
            "- unavailable ideal `Y`：",
            "- surrogate `Z`：",
            "- `Z ≈ Y` 的证据与不足：",
            "",
            "### Challenge-Failure-Module-Evidence 映射",
            "",
            "| Challenge | Failure mode | Design principle | Module | Evidence |",
            "|---|---|---|---|---|",
            "|  |  |  |  |  |",
            "",
            "### Module-Ideal-Proxy-Assumption-New-Idea 映射",
            "",
            "| Module | Unavailable ideal | Available proxy | Hidden assumption | New idea under violated assumption |",
            "|---|---|---|---|---|",
            "|  |  |  |  |  |",
            "",
            "### Citation-to-Module Map",
            "",
            "| Citation cluster | Narrative function | Related module | Inherited assumption | Paper modification |",
            "|---|---|---|---|---|",
            "|  |  |  |  |  |",
            "",
            "### Experiments-As-Story-Evidence Matrix",
            "",
            "| Experiment | Claim | Counterfactual | Metric | Stress condition | Story role |",
            "|---|---|---|---|---|---|",
            "|  |  |  |  |  |  |",
            "",
            "### Reusable Story-Making Pattern",
            "",
            "- replacement story：",
            "- two-axis empty cell：",
            "- closed-loop contribution：",
            "- boundary-pushing template：",
            "",
            "### Hidden-Assumption-To-Boundary-Direction Table",
            "",
            "| Hidden assumption | Violated setting | New mechanism needed | Boundary-pushing potential |",
            "|---|---|---|---|",
            "|  |  |  |  |",
            "",
            "### 提出算法的模型、架构、训练与推理流程",
            "",
            "- model form：",
            "- architecture summary：",
            "- key modules：",
            "- 哪些模块设计更像作者的主观取舍，而不是唯一合理方案：",
            "- training pipeline：",
            "- inference pipeline：",
            "- optimization objectives：",
            "- communication / deployment path：",
            "",
            "### 公式保留与逐式解释",
            "",
            "- preserved equations：",
            "- term-by-term explanation：",
            "- role of each equation：",
            "- equation -> algorithm step mapping：",
            "",
            "### 具体公式、模块与设计假设的不足及可改进空间",
            "",
            "- formula-level weaknesses：",
            "- module-level weaknesses：",
            "- hidden or strong assumptions：",
            "- optimization / efficiency concerns：",
            "- alternative formulations or modules：",
            "- trade-offs of proposed improvements：",
            "",
            "### 带具体例子的算法步骤演示",
            "",
            "- worked example setup：",
            "- step-by-step state updates：",
            "- example inputs / outputs：",
            "- what the example reveals：",
            "",
            "### 相关论文与关联理由",
            "",
            "-",
            "",
            "### 论文中反复提到的关键文献及其未解空白",
            "",
            "- key repeatedly discussed papers：",
            "- unsolved gaps carried forward：",
            "- why current paper targets those gaps：",
            "",
            "### 创新点与主张的证据审计表",
            "",
            "- claim row：",
            "- evidence columns：",
            "- support strength：",
            "- missing support notes：",
            "",
            "### 审稿覆盖核对",
            "",
            "- review -> reply chain：",
            "- report-level coverage conclusion：",
            "",
            "### 架构图 / 模型图 / 结果图补充",
            "",
            "- important figures / pages：",
            "- what each visual clarifies：",
            "",
            "### 架构图 / 模型图设计方案",
            "",
            "- reusable figure blueprint：",
            "- visual prompt blueprint：",
            "",
            "### 实验图表设计可借鉴点",
            "",
            "-",
            "",
            "### 实验设置与比较算法谱系对应表",
            "",
            "- datasets / metrics / protocols：",
            "- baseline -> related work mapping：",
            "- why each baseline is included：",
            "- intro / related work -> experiment link：",
            "",
            "### 各实验环节的目的、支撑主张与现象总结",
            "",
            "- experiment block purpose：",
            "- claim supported by each block：",
            "- surprising or controversial findings：",
            "- limitations exposed：",
            "",
            "### 可继续追的创新点",
            "",
            "-",
            "",
            "### Teaching-Explainer Appendix",
            "",
            "- audience map：",
            "- story spine：",
            "- formula / visual / experiment teaching scripts：",
            "- role-play discussion pack：",
            "- Q&A and defense bank：",
            "- slide / talk blueprint：",
            "- teachback self-test：",
            "",
            "<!-- paper-deepread-structured-appendix:end -->",
            "",
            "## Scientific Problem, Missing Gap, And Literature Positioning",
            "",
            "- Which scientific problem should actually be stated at the paper's own level?",
            "- Which scientific gap does the paper claim to fill?",
            "- Which adjacent literature threads are the closest comparators?",
            "- Which older methods or borrowed families does the paper inherit from?",
            "- What exactly is improved over those inherited methods?",
            "- Which blank between prior work and this paper became the real entry point for the contribution?",
            "- Which papers are most directly related, which are only loosely related, and why?",
            "",
            "## Claim-Support Matrix",
            "",
            "- List each major claim as a row.",
            "- List the support sources or evidence types as columns.",
            "- Judge support strength for each row.",
            "- Point out any missing or indirect support.",
            "",
            "## Symbols, Definitions, And Core Concepts For Beginners",
            "",
            "- List the main symbols and what they mean.",
            "- Explain the central definitions and assumptions in beginner-friendly language.",
            "- Explain the task setting, objective, and evaluation concepts with a simple example.",
            "- Explain any problem-specific notation, datasets, protocols, and operators that a beginner would otherwise misread.",
            "",
            "## Core Algorithm And Procedure",
            "",
            "- Give the algorithm step by step.",
            "- Clarify inputs, outputs, intermediate states, and update rules.",
            "- Explain which parts are novel and which parts are inherited baselines.",
            "- State the main computational cost, memory cost, and any deployment-critical path.",
            "",
            "## Algorithm Walkthrough With A Concrete Example",
            "",
            "- Define a mini-case with concrete variables or samples.",
            "- Walk through each step and state update.",
            "- Highlight where the novel part changes the trajectory.",
            "- Explain what this example teaches a beginner.",
            "",
            "## Theory, Proofs, And Their Role",
            "",
            "- What propositions / theorems / lemmas are stated?",
            "- Why did the authors need these proofs?",
            "- Which assumptions are crucial for the proofs?",
            "- What is the proof strategy at a high level?",
            "- Which conclusions actually matter for the practical algorithm?",
            "- Which implementation steps or system behaviors correspond to the proved objects?",
            "- Is the implementation exactly matched to the proof target, only a local approximation, or only theory-motivated?",
            "- What theory-to-algorithm gap still remains?",
            "",
            "## 理论、证明与实现步骤对照",
            "",
            "- theorem / lemma / proposition -> algorithm step mapping：",
            "- assumptions -> implementation assumptions：",
            "- exact match / local approximation / loose motivation：",
            "- why these proofs matter in practice：",
            "- where theory stops matching practice：",
            "",
            "## 具体公式、模块与设计假设的不足及可改进空间",
            "",
            "- formula-level weaknesses：",
            "- module-level weaknesses：",
            "- assumption fragility or mismatch：",
            "- optimization / efficiency concerns：",
            "- possible alternatives or reformulations：",
            "- improvement room and trade-offs：",
            "",
            "## Experimental Design Logic And Author Reasoning",
            "",
            "- Why did the authors choose these datasets, baselines, and metrics?",
            "- Which doubt is each major experiment trying to preempt?",
            "- What sequence of reasoning likely led from the idea to this experiment plan?",
            "- Which experiment exists mainly to convince skeptical reviewers rather than only to improve the scoreboard?",
            "",
            "## Probe Models, Bridge Experiments, And Mechanism Checks",
            "",
            "- Which exploratory models, probes, or pilot experiments help bridge the gap from idea to final algorithm?",
            "- Which mechanism checks are convincing and which are still weak?",
            "- Which failed or partial design paths can be inferred from the final experiment layout?",
            "",
            "## Interesting Empirical Phenomena And Lessons",
            "",
            "- Which surprising or counter-intuitive results appeared?",
            "- What do these phenomena teach us about the scientific problem?",
            "- What should a follow-up paper test next because of these findings?",
            "",
            "## Innovation Type And Boundary-Crossing Judgment",
            "",
            "- Is the work mainly incremental, cross-domain, or boundary-breaking?",
            "- Why does that judgment hold?",
            "- Does it truly cross a disciplinary boundary or mainly recombine ideas within one field?",
            "- Which future crossings or hybridizations does it suggest?",
            "",
            "## Author-Team Continuation Notes From Upstream Materials",
            "",
            "- Which upstream materials already exposed author or team context?",
            "- Which authors can be confirmed from the paper itself or the upstream bundle without reopening search?",
            "- If nearby team continuation context is already present upstream, summarize it here.",
            "- If this context is missing, state that it is deferred back to the collection stage rather than searched here.",
            "",
            "## External Retrieval Deferred To Collection Stage",
            "",
            "- State explicitly that no new external retrieval was performed in this deep-read stage.",
            "- Which missing PDFs, review bundles, author-team context, or related-paper leads should be sent back to the collection stage?",
            "- What stage-boundary note should downstream users keep in mind?",
            "",
            "## Routing Appendix",
            "",
            "Current Status",
            "",
            "- Paper deep-read scaffold initialized.",
            f"- Paper slug: `{paper_slug}`",
            "",
            "Possible User Inputs For Next Stage",
            "",
            "- one confirmed research subfield or direction label",
            "- which candidate starting nodes or expansion branches should be activated first",
            "- optional budget / hardware information if the next stage should rank candidate directions",
            "",
        ]
    ) + "\n"

def build_focus_spec(paper_title: str, paper_id: str) -> dict:
    payload = template_json("paper_focus_spec.template.json")
    payload["paper_id"] = paper_id
    payload["title"] = paper_title
    payload["related_papers"] = []
    payload["graph_node_candidates"] = []
    payload["graph_relation_candidates"] = []
    payload["innovation_hooks"] = []
    payload["figure_targets"] = []
    payload["research_generative_reading"] = {
        "research_equation": {},
        "author_side_direction_discovery": {},
        "story_construction": {},
        "module_author_thinking": [],
        "reverse_citation_logic": [],
        "experiments_as_story_evidence": [],
        "reusable_story_making_patterns": [],
        "hidden_assumption_to_new_idea": [],
    }
    payload["teaching_explanation_reading"] = {
        "audience_profile": {},
        "three_layer_summary": {},
        "story_spine": {},
        "formula_teaching": [],
        "visual_teaching": [],
        "experiment_teaching": [],
        "role_play_discussion_pack": [],
        "qa_bank": [],
        "misunderstanding_guardrails": [],
        "slide_blueprint": [],
        "teachback_self_test": [],
        "three_takeaways": [],
    }
    return payload


def build_cross_paper_template(paper_titles: list[str]) -> str:
    bullets = "\n".join(f"- {title}" for title in paper_titles)
    return "\n".join(
        [
            "# Cross-Paper Comparison",
            "",
            "## Papers In Scope",
            "",
            bullets or "- [fill papers]",
            "",
            "## Shared Scientific Problems",
            "",
            "-",
            "",
            "## Shared Parent-Field Problems",
            "",
            "-",
            "",
            "## Shared ML/AI Problems",
            "",
            "-",
            "",
            "## Contrasts In Methods And Evidence",
            "",
            "-",
            "",
            "## What Should Enter The Innovation-Graph Stage",
            "",
            "-",
            "",
        ]
    ) + "\n"


def stage_delivery_template(paper_titles: list[str]) -> str:
    paper_lines = "\n".join(f"- {title}" for title in paper_titles)
    return "\n".join(
        [
            "# Stage Delivery Handoff",
            "",
            "## Stage Status",
            "",
            "- Stage: chatgpt_paper_deep_reading_skill_source",
            "- Status: initialized scaffold only; fill every per-paper authoritative report before handoff.",
            "- Deep-read rule: every paper in `metadata/paper_batch_manifest.json` must receive one authoritative detailed report. Selective reading is not allowed at handoff time.",
            "- Downstream contract style: loose coupling, high cohesion. The next stage should read routing status, stage delivery handoff, the paper batch manifest, and the project directory index before scanning directories.",
            "",
            "## Papers Required In This Batch",
            "",
            paper_lines or "- [fill papers]",
            "",
            "## Authoritative Deliverables",
            "",
            "- `metadata/query_spec.json`",
            "- `metadata/paper_batch_manifest.json`",
            "- `metadata/delivery_bundle_manifest.json`",
            "- `metadata/routing_status.json`",
            "- `metadata/project_directory_index.json`",
            "- `reports/stage_delivery_handoff.md`",
            "- `reports/project_directory_index.md`",
            "- `reports/per_paper/<paper-slug>/<paper-slug>_detailed_cn.md`",
            "- `reports/per_paper/<paper-slug>/<paper-slug>_detailed_cn.pdf`",
            "- `generated/intermediate/<paper-slug>.json`",
        ]
    ) + "\n"


def build_zip(workspace_dir: Path, output_zip: Path) -> None:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(workspace_dir.rglob("*")):
            if path.is_dir():
                continue
            zf.write(path, arcname=path.relative_to(workspace_dir).as_posix())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label", nargs="?", help="Optional batch label. If no --paper-title is provided, treat this as the single paper title.")
    parser.add_argument("--paper-title", action="append", default=[])
    parser.add_argument("--paper-id", action="append", default=[])
    parser.add_argument("--slug")
    parser.add_argument("--root", type=Path, default=Path("artifacts/paper_deep_reads"))
    parser.add_argument("--existing-collection-root", type=Path)
    parser.add_argument("--research-subfield", default="")
    parser.add_argument("--review-context-note", default="")
    parser.add_argument("--output-mode", choices=["codex_local", "chatgpt_bundle"], default="chatgpt_bundle")
    parser.add_argument("--bundle-zip", type=Path)
    args = parser.parse_args()

    paper_titles = normalize_unique(args.paper_title)
    if not paper_titles and args.label:
        paper_titles = [args.label.strip()]
    if not paper_titles:
        parser.error("Provide at least one --paper-title or a positional label.")

    paper_ids = list(args.paper_id)
    while len(paper_ids) < len(paper_titles):
        paper_ids.append("")

    batch_label = args.label.strip() if args.label else paper_titles[0]
    slug = args.slug or slugify(batch_label)
    root = args.root / slug

    for rel in [
        Path("inputs/papers"),
        Path("inputs/review_context"),
        Path("inputs/source_metadata"),
        Path("metadata"),
        Path("metadata/focus_specs"),
        Path("reports"),
        Path("reports/per_paper"),
        Path("generated/intermediate"),
        Path("generated/visuals"),
    ]:
        (root / rel).mkdir(parents=True, exist_ok=True)

    query_spec = {
        "batch_label": batch_label,
        "paper_titles": paper_titles,
        "research_subfield": args.research_subfield,
        "existing_collection_root": str(args.existing_collection_root.as_posix()) if args.existing_collection_root else "",
        "review_context_note": args.review_context_note,
        "input_contract": {
            "paper_sources": "Upload authoritative PDFs or source folders under inputs/papers/.",
            "review_context": "Upload OpenReview or other review exports under inputs/review_context/ when available.",
            "source_metadata": "Upload manifests, source records, and collection-level directory indexes under inputs/source_metadata/ when available.",
            "restartable_upstream_bundle": "Prefer one previous-stage delivery zip that already carries metadata/delivery_bundle_manifest.json, metadata/routing_status.json, metadata/project_directory_index.json, reports/project_directory_index.md, and reports/stage_delivery_handoff.md.",
        },
        "restartable_handoff_contract": {
            "required_upstream_bundle_artifacts": [
                "metadata/delivery_bundle_manifest.json",
                "metadata/routing_status.json",
                "metadata/project_directory_index.json",
                "reports/project_directory_index.md",
                "reports/stage_delivery_handoff.md",
            ],
            "required_upstream_source_record_fields": list(build_focus_spec("", "").get("source_record", {}).keys()),
            "read_before_browsing_tree": [
                "metadata/delivery_bundle_manifest.json",
                "metadata/routing_status.json",
                "metadata/project_directory_index.json",
                "reports/stage_delivery_handoff.md",
            ],
        },
        "authoritative_report_contract": {
            "contract_file": "schemas/detailed_report_contract.md",
            "required_sections_file": "schemas/detailed_report_required_sections.json",
            "preferred_output_layout_file": "schemas/per_paper_output_layout.md",
        },
        "project_directory_index_outputs": {
            "annotations": "metadata/project_directory_annotations.json",
            "json": "metadata/project_directory_index.json",
            "markdown": "reports/project_directory_index.md",
        },
        "expected_outputs": {
            "per_paper_report_root": "reports/per_paper",
            "intermediate_root": "generated/intermediate",
            "visual_root": "generated/visuals",
            "routing_status_json": "metadata/routing_status.json",
            "stage_delivery_handoff_md": "reports/stage_delivery_handoff.md",
            "delivery_bundle_manifest_json": "metadata/delivery_bundle_manifest.json",
            "delivery_bundle_zip": "outputs/zips/<batch-slug>-paper-deep-reading-bundle.zip",
        },
        "deepread_policy": {
            "read_every_paper_in_batch": True,
            "selective_reading_allowed": False,
            "iclr_review_rule": "when local OpenReview review / rebuttal context exists, consume it in the authoritative report instead of treating it as optional scratch context",
            "upstream_context_reuse_rule": "reuse only author-team or continuation context already present in the upstream bundle or in the paper itself; do not reopen external retrieval here",
            "no_new_external_retrieval_rule": "record retrieval gaps for later collection-stage work instead of starting new academic-site or GitHub search inside deep reading",
        },
    }

    manifest_entries: list[dict[str, object]] = []
    key_artifacts = [
        "metadata/query_spec.json",
        "metadata/paper_batch_manifest.json",
        "metadata/delivery_bundle_manifest.json",
        "metadata/project_directory_index.json",
        "reports/stage_delivery_handoff.md",
        "reports/project_directory_index.md",
    ]

    for paper_title, paper_id in zip(paper_titles, paper_ids):
        paper_slug = slugify(paper_title)
        report_dir = root / "reports" / "per_paper" / paper_slug
        report_md = report_dir / f"{paper_slug}_detailed_cn.md"
        focus_spec_path = root / "metadata" / "focus_specs" / f"{paper_slug}.json"
        ensure_file(report_md, render_report_stub(paper_title, paper_id, paper_slug, str(args.existing_collection_root.as_posix()) if args.existing_collection_root else ""))
        ensure_file(focus_spec_path, json.dumps(build_focus_spec(paper_title, paper_id), ensure_ascii=False, indent=2) + "\n")
        manifest_entries.append(
            {
                "paper_title": paper_title,
                "paper_id": paper_id,
                "paper_slug": paper_slug,
                "authoritative_report_md": str(report_md.relative_to(root).as_posix()),
                "authoritative_report_pdf": f"reports/per_paper/{paper_slug}/{paper_slug}_detailed_cn.pdf",
                "focus_spec_json": str(focus_spec_path.relative_to(root).as_posix()),
                "intermediate_json": f"generated/intermediate/{paper_slug}.json",
                "visual_manifest_json": f"generated/visuals/{paper_slug}/visual_manifest.json",
                "status": "pending_deepread",
            }
        )
        key_artifacts.append(str(report_md.relative_to(root).as_posix()))
        key_artifacts.append(str(focus_spec_path.relative_to(root).as_posix()))

    if len(paper_titles) > 1:
        cross_paper_path = root / "reports" / "cross_paper_comparison_cn.md"
        ensure_file(cross_paper_path, build_cross_paper_template(paper_titles))
        key_artifacts.append(str(cross_paper_path.relative_to(root).as_posix()))

    query_spec_path = root / "metadata" / "query_spec.json"
    query_spec_path.write_text(json.dumps(query_spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "metadata" / "paper_batch_manifest.json").write_text(json.dumps({"batch_label": batch_label, "papers": manifest_entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ensure_file(root / "metadata" / "project_directory_annotations.json", template_text("project_directory_annotations.template.json"))

    routing = template_json("routing_status_template.json")
    routing["current_stage"] = "initialized_paper_deep_reading"
    routing["next_stage"] = "awaiting_deepread_execution"
    routing["recommended_next_skill"] = "chatgpt_paper_deep_reading_skill_source"
    routing["required_paper_count"] = len(paper_titles)
    routing["remaining_papers_without_authoritative_reports"] = list(paper_titles)
    routing["resume_from_bundle_only_supported"] = True
    routing["status_artifacts"] = [
        "metadata/routing_status.json",
        "reports/stage_delivery_handoff.md",
    ]
    routing["directory_description_artifacts"] = [
        "metadata/project_directory_index.json",
        "reports/project_directory_index.md",
    ]
    routing["last_assistant_action"] = "Initialized the paper deep-reading workspace scaffold."
    routing["paper_id"] = paper_ids[0] if len(paper_titles) == 1 else ""
    routing["paper_title"] = paper_titles[0] if len(paper_titles) == 1 else batch_label
    routing["key_artifacts"] = normalize_unique(key_artifacts)
    routing["authoritative_handoff_artifacts"] = []
    (root / "metadata" / "routing_status.json").write_text(json.dumps(routing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ensure_file(root / "reports" / "stage_delivery_handoff.md", stage_delivery_template(paper_titles))
    delivery_manifest_artifacts = [
        "metadata/query_spec.json",
        "metadata/paper_batch_manifest.json",
        "metadata/delivery_bundle_manifest.json",
        "metadata/routing_status.json",
        "metadata/project_directory_index.json",
        "reports/stage_delivery_handoff.md",
        "reports/project_directory_index.md",
    ]
    for item in manifest_entries:
        delivery_manifest_artifacts.extend(
            [
                str(item.get("authoritative_report_md", "")).strip(),
                str(item.get("focus_spec_json", "")).strip(),
            ]
        )
    delivery_manifest = build_delivery_manifest(
        root,
        authoritative_handoff_artifacts=delivery_manifest_artifacts,
    )
    routing["authoritative_handoff_artifacts"] = normalize_unique(delivery_manifest_artifacts)
    (root / "metadata" / "routing_status.json").write_text(
        json.dumps(routing, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (root / "metadata" / "delivery_bundle_manifest.json").write_text(
        json.dumps(delivery_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    refresh_project_directory_index(root)

    bundle_zip = None
    if args.output_mode == "chatgpt_bundle":
        bundle_zip = args.bundle_zip or (Path("outputs/zips") / f"{slug}-paper-deep-reading-bundle.zip")
        build_zip(root, bundle_zip)
        delivery_manifest["delivery_bundle_zip"] = str(bundle_zip.as_posix())
        (root / "metadata" / "delivery_bundle_manifest.json").write_text(
            json.dumps(delivery_manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        routing["delivery_bundle_zip"] = str(bundle_zip.as_posix())
        (root / "metadata" / "routing_status.json").write_text(
            json.dumps(routing, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(json.dumps({"workspace_root": str(root.resolve()), "query_spec": str(query_spec_path.resolve()), "paper_batch_manifest_json": str((root / "metadata" / "paper_batch_manifest.json").resolve()), "delivery_bundle_manifest_json": str((root / "metadata" / "delivery_bundle_manifest.json").resolve()), "routing_status_json": str((root / "metadata" / "routing_status.json").resolve()), "project_directory_index_json": str((root / "metadata" / "project_directory_index.json").resolve()), "project_directory_index_md": str((root / "reports" / "project_directory_index.md").resolve()), "stage_delivery_handoff_md": str((root / "reports" / "stage_delivery_handoff.md").resolve()), "bundle_zip": str(bundle_zip.resolve()) if bundle_zip else ""}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
