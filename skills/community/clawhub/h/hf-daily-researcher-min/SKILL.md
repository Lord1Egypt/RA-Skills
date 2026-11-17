---
name: hf-daily-deep-researcher
version: 4.2.0
description: |
  HuggingFace Daily Papers + arXiv 多Agent深度研究系统。
  采用编排器+专业Agent架构，支持两种模式：
  1. 轻量扫描模式：周期性追踪（周/月），发现新论文
  2. 深度调研模式：全时间范围调研，产出全面深入的研究报告
  支持动态配置、自适应关键词、周期版本控制、跨平台搜索工具适配。
---

# HF Daily Deep Researcher v4 — 多Agent编排版

## 架构概览

本 Skill 支持**两种工作模式**，根据用户请求自动判断：

### 模式 1: 轻量扫描（Light Scan）
- **触发条件**: 用户请求时间跨度 ≤30天（如"最近一周"、"本月"）
- **目标**: 周期性追踪新发表论文，及时发现新工作
- **搜索范围**: 按时间窗口分段，追新
- **精读策略**: 只精读 P0/P1 高优先级论文
- **输出**: 周报/月报（`templates/report_template.md`）

### 模式 2: 深度调研（Deep Research）
- **触发条件**: 用户请求时间跨度 >30天，或明确说"研究研究"、"深入调研"、"系统梳理"
- **目标**: 全面覆盖一个研究方向，形成大而全的调研报告
- **搜索范围**: 全时间范围，按方法论/作者/引用链搜索
- **精读策略**: 所有重要工作都要精读，区分 milestone/improvement/application
- **分析维度**: Benchmark 现状、研究空白、代码开源、权威性验证（并行子分析师）
- **输出**: 深度调研报告（`templates/deep_report_template.md`）

```
┌─────────────────────────────────────────────────────────────────┐
│                    编排器 (Orchestrator)                          │
│              — 自动判断模式 → 执行对应工作流                       │
├─────────────────────────────────────────────────────────────────┤
│  轻量扫描模式              │  深度调研模式                        │
│  ├─ Searcher (主Agent)     │  ├─ Deep Searcher (主Agent)         │
│  ├─ Deep Reader (子Agent) │  ├─ Deep Reader (子Agent)           │
│  ├─ Analyst (子Agent)      │  ├─ Sub-Analysts (并行子Agent)     │
│  ├─ Writer (子Agent)       │  │   ├─ Benchmark                   │
│  └─ Checker (子Agent)      │  │   ├─ Gap                         │
│                            │  │   ├─ Code                        │
│                            │  │   └─ Authority                   │
│                            │  ├─ Synthesis Analyst (子Agent)    │
│                            │  ├─ Deep Writer (子Agent)          │
│                            │  ├─ Multi-Checker (子Agent)        │
│                            │  └─ Revision (迭代修订)             │
└────────────────────────────┴─────────────────────────────────────┘
```

> **注意**：Searcher 阶段（红色）由**主 Agent 直接执行**，不再通过 `sessions_spawn` 启动子 Agent。这是 v4.1.2 的关键修复——彻底避免搜索结果被截断的问题。

**模式判断逻辑**（由主 Agent 执行）：
```python
def determine_mode(user_request, days=None):
    deep_signals = ["研究研究", "深入调研", "全面调研", "系统梳理", 
                    "综述", "survey", "深度", "过去一年", "半年", 
                    "long-term", "comprehensive"]
    light_signals = ["最近一周", "最近一个月", "本周", "本月", 
                     "周报", "月报", "跟踪", "scan", "过去7天", "过去30天"]
    
    text = user_request.lower()
    if any(s in text for s in deep_signals):
        return "deep"
    if any(s in text for s in light_signals):
        return "light"
    if days is not None:
        return "deep" if days > 30 else "light"
    return "ask_user"
```

### 为什么用多Agent？
**Searcher 为什么不用子 Agent？**
- `sessions_spawn` 的 announce 机制**不保证**能拿到子 Agent 的完整最终输出
- 搜索阶段调用 `kimi_search` 等工具，主 Agent 完全有能力直接执行
- 主 Agent 直接搜索 = 100% 可控，彻底避免截断问题

**Deep Reader / Analyst / Writer / Checker 为什么用子 Agent？**
- 精读需要处理大量论文内容，独立上下文避免 token 爆炸
- 分析需要多维度并行（Benchmark、Gap、Code、Authority 独立分析后再综合）
- 质检需要独立视角
- 这些阶段的输出是"分析/报告/检查结论"，即使截断也可由主 Agent 检测并补充

## 数据传递模式

子 Agent 通过 `sessions_spawn` 启动，**环境隔离导致它们无法直接写入主 Agent 的文件系统**。工作流采用以下模式：

```
Phase 1: 主Agent直接搜索 → 写入 .tmp/papers_raw.json
Phase 2+: 子Agent执行任务 → 输出到回复/announce
          主Agent接收 completion event → 提取内容
          主Agent写入 .tmp/ 文件 → 后续阶段读取
```

**关键设计原则：信息准确 > 格式统一**

- 搜索信息来源多样（arXiv、HuggingFace、GitHub、gist 等），格式不可能标准化
- 主 Agent 直接执行搜索并整理结果，**确保数据完整性**
- 子 Agent 负责分析/撰写/检查，主 Agent 负责解析和结构化

**⚠️ 子Agent输出截断问题（Deep Reader阶段）**

子Agent在执行过程中可能产生多轮输出。`sessions_spawn` 的 announce 机制可能**只截取其中某一轮的内容**。

**应对措施**：
1. **每篇论文一个独立 Deep Reader Agent**：减少单个 Agent 的输出量，降低截断概率
2. **主Agent检测完整性**：收到子Agent结果后，检查内容是否明显不完整（如字数过少、没有核心方法描述）
3. **主Agent兜底阅读**：如果检测到某篇论文分析不完整，主Agent自行下载并补充分析

### Phase 1: 搜索（主Agent直接执行）

**输入**: config.json + keywords.json
**输出**: 主 Agent 直接写入 `.tmp/papers_raw.json`（轻量）或 `.tmp/deep_papers_raw.json`（深度）

**执行方式**:
```python
def run_search(focus_keywords, days=None, mode="light"):
    """
    主 Agent 直接执行搜索，不再通过 sessions_spawn 启动子 Agent。
    这是 v4.1.2 的关键修复。
    """
    all_results = []
    
    # 对每个研究方向的关键词执行搜索
    for focus in focus_keywords:
        # 生成搜索关键词组合
        search_queries = generate_search_queries(focus, mode=mode)
        
        for query in search_queries:
            # 主 Agent 直接调用 kimi_search
            results = kimi_search(query)
            all_results.extend(results)
            
            # 如果 kimi_search 不可用，降级到 web_fetch
            if not results:
                results = web_fetch(f"https://export.arxiv.org/api/query?search_query={query}&max_results=50")
                all_results.extend(parse_arxiv_api_results(results))
    
    # 去重、过滤黑名单、计算优先级
    papers = deduplicate_and_rank(all_results)
    
    # 主 Agent 直接写入文件
    save_json(f".tmp/{'deep_' if mode == 'deep' else ''}papers_raw.json", papers)
    
    return papers
```

**搜索策略**（主 Agent 参考 `agents/searcher_prompt.md`）:
- **轻量模式**：按时间窗口搜索（过去 N 天），追新
- **深度模式**：不限时间，按方法论/作者/引用链全面搜索
- 关键词组合：research_focus + 自适应关键词 + 时间限定
- 来源：arXiv（主要）、HuggingFace Daily Papers（辅助）、GitHub（代码）

**为什么这样设计？**
- 主 Agent 直接调用 `kimi_search` 等工具，输出完全可控
- 不需要担心 announce 截断——工具返回的结果在主 Agent 的上下文中
- 搜索策略放在 `agents/searcher_prompt.md` 中作为参考，主 Agent 按需读取

### Phase 2: 深度精读 (Deep Reader Agents — 并行)

**输入**: 单篇论文 arXiv ID + 已有工作上下文
**输出**: 子 Agent 在回复中输出分析 → 主 Agent 提取并保存为 `paper_analysis_{arxiv_id}.md`

**任务定义**:
```
你是一名论文精读Agent。任务：
1. 下载论文 arXiv HTML 实验版（完整无截断）
2. 分段提取核心内容（方法、公式、实验数据）
3. 数据三级验证（自检 → 交叉核对 → 标注验证级别）
4. 在最终回复中一次性完整输出 Markdown 分析报告（不要写入文件）
   ⚠️ 不要在中间轮次输出任何文本，只在最终轮输出完整分析
```

**调用方式**:
```python
# 主 Agent 并行启动多个 Deep Reader（每篇 P0 论文一个）
reader_tasks = []
for paper in p0_papers[:3]:  # 最多精读3篇P0
    task = sessions_spawn(
        task=f"精读论文 {paper['arxiv_id']}...",
        label=f"HF-DeepReader-{paper['arxiv_id']}"
    )
    reader_tasks.append((paper['arxiv_id'], task))

# 等待所有 completion events，检测完整性
for arxiv_id, task in reader_tasks:
    content = extract_content_from_completion(task)
    
    # 检测是否完整
    if not check_reader_completeness(content):
        print(f"警告：论文 {arxiv_id} 分析不完整，主Agent自行补充")
        content = perform_backup_reading(arxiv_id)
    
    save_file(f".tmp/paper_analysis_{arxiv_id}.md", content)
```

**并行策略**:
- P0 论文：每篇一个独立 Deep Reader Agent（并行）
- P1 论文：每篇一个 Agent（如果数量多，可分批）
- P2/P3：不精读，仅记录基本信息

**完整性检测**:
```python
def check_reader_completeness(content: str) -> bool:
    """检测论文分析是否完整"""
    if len(content) < 300:
        return False  # 字数过少
    if "核心方法" not in content and "方法" not in content:
        return False  # 缺少方法描述
    if "实验" not in content and "结果" not in content:
        return False  # 缺少实验结果
    return True
```

### Phase 3: 综合分析 (Analyst Agent)

**输入**: 主 Agent 提供论文分析文件路径（或内容摘要）
**输出**: 子 Agent 在回复中输出分析 → 主 Agent 提取并保存为 `analysis_summary.md`

**任务定义**:
```
你是一名研究分析Agent。任务：
1. 读取所有论文分析内容（主 Agent 会在任务描述中提供）
2. 识别方法簇、分析趋势变化
3. 评估对当前研究项目的潜在影响
4. 在最终回复中一次性完整输出结构化分析（不要写入文件）
```

### Phase 4: 报告撰写 (Writer Agent)

**输入**: 主 Agent 提供论文列表 + 分析内容 + 报告模板
**输出**: 子 Agent 在回复中输出报告 → 主 Agent 提取并保存为报告文件

**任务定义**:
```
你是一名报告撰写Agent。任务：
1. 根据提供的论文列表和分析内容
2. 按统一模板组织完整报告
3. 在最终回复中一次性完整输出报告内容（不要写入文件）
```

### Phase 5: 质量检查 (Checker Agent)

**输入**: 主 Agent 提供报告内容
**输出**: 子 Agent 在回复中输出检查结果

**检查清单**:
```
你是一名质量检查Agent。任务：对报告做独立质量审查。
检查维度：内容完整性、数据准确性、研究观点、格式规范、去重
在回复中直接输出检查结果（PASSED/FAILED + 问题清单）
```

## 执行流程（编排器逻辑）

### 轻量扫描模式工作流

```python
def run_light_scan(days=7):
    # Step 1: 读取配置
    config = load_config()
    focus = config["user_profile"]["research_focus"]
    
    # Step 1.5: 确认研究方向
    if not focus or len(focus) == 0:
        user_focus = ask_user("请确认你的研究方向（用逗号分隔）：")
        config["user_profile"]["research_focus"] = [f.strip() for f in user_focus.split(",")]
        save_config(config)
        focus = config["user_profile"]["research_focus"]
    
    # Step 2: 主 Agent 直接搜索（不再启动 Searcher 子 Agent）
    papers = run_search(focus, days=days, mode="light")
    # papers 已自动保存到 .tmp/papers_raw.json
    
    # Step 3: 并行 Deep Readers（只读 top N）
    p0_papers = [p for p in papers if p["priority"] >= 0.8]
    
    reader_tasks = []
    for paper in p0_papers[:3]:  # 最多精读3篇P0
        task = sessions_spawn(
            task=f"精读论文 {paper['arxiv_id']}...",
            label=f"HF-DeepReader-{paper['arxiv_id']}"
        )
        reader_tasks.append((paper['arxiv_id'], task))
    
    for arxiv_id, task in reader_tasks:
        content = extract_content_from_completion(task)
        if not check_reader_completeness(content):
            content = perform_backup_reading(arxiv_id)
        save_file(f".tmp/paper_analysis_{arxiv_id}.md", content)
    
    # Step 4: Analyst（趋势分析）
    analyst = sessions_spawn(task="分析趋势...", label="HF-Analyst")
    analysis_content = extract_content_from_completion(analyst)
    save_file(".tmp/analysis_summary.md", analysis_content)
    
    # Step 5: Writer（周报）
    writer = sessions_spawn(task="撰写周报...", label="HF-Writer")
    report_content = extract_content_from_completion(writer)
    
    # Step 6: Checker（单一质检）
    checker = sessions_spawn(task="检查周报质量...", label="HF-Checker")
    check_result = extract_content_from_completion(checker)
    
    # Step 7: 保存
    save_report(report_content, template="report_template.md", mode="light")
    
    return report_content
```

### 深度调研模式工作流

```python
def run_deep_research(research_topic, days=None):
    """
    深度调研模式：全时间范围，多维度分析，迭代修订
    """
    # Step 1: 读取配置与主题
    config = load_config()
    focus = config["user_profile"]["research_focus"]
    
    # Step 2: 主 Agent 直接深度搜索（不再启动 Deep Searcher 子 Agent）
    papers = run_search(
        focus + [research_topic], 
        mode="deep"
    )
    # papers 已自动保存到 .tmp/deep_papers_raw.json
    
    # Step 3: 并行 Deep Readers（所有重要工作）
    milestone_papers = [p for p in papers if p.get("type") == "milestone"]
    improvement_papers = [p for p in papers if p.get("type") == "improvement"]
    
    reader_tasks = []
    # 所有 milestone 必须精读
    for paper in milestone_papers:
        task = sessions_spawn(
            task=f"精读里程碑论文 {paper['arxiv_id']}...",
            label=f"HF-DeepReader-{paper['arxiv_id']}"
        )
        reader_tasks.append((paper['arxiv_id'], task))
    # 重要的 improvement 也要精读
    for paper in improvement_papers[:10]:
        task = sessions_spawn(
            task=f"精读改进论文 {paper['arxiv_id']}...",
            label=f"HF-DeepReader-{paper['arxiv_id']}"
        )
        reader_tasks.append((paper['arxiv_id'], task))
    
    for arxiv_id, task in reader_tasks:
        content = extract_content_from_completion(task)
        if not check_reader_completeness(content):
            content = perform_backup_reading(arxiv_id)
        save_file(f".tmp/paper_analysis_{arxiv_id}.md", content)
    
    # Step 4: 并行 Sub-Analysts（多维度分析）
    benchmark_analyst = sessions_spawn(
        task="分析该领域 Benchmark 现状与饱和度...",
        label="HF-SubAnalyst-Benchmark"
    )
    gap_analyst = sessions_spawn(
        task="识别研究空白与可做方向...",
        label="HF-SubAnalyst-Gap"
    )
    code_analyst = sessions_spawn(
        task="检查代码开源情况...",
        label="HF-SubAnalyst-Code"
    )
    authority_analyst = sessions_spawn(
        task="验证论文权威性与引用准确性...",
        label="HF-SubAnalyst-Authority"
    )
    
    benchmark_result = extract_content_from_completion(benchmark_analyst)
    gap_result = extract_content_from_completion(gap_analyst)
    code_result = extract_content_from_completion(code_analyst)
    authority_result = extract_content_from_completion(authority_analyst)
    
    save_file(".tmp/sub_benchmark.md", benchmark_result)
    save_file(".tmp/sub_gap.md", gap_result)
    save_file(".tmp/sub_code.md", code_result)
    save_file(".tmp/sub_authority.md", authority_result)
    
    # Step 5: Synthesis Analyst（综合整合）
    synthesis = sessions_spawn(
        task="整合所有子分析结果...",
        label="HF-Synthesis-Analyst"
    )
    synthesis_result = extract_content_from_completion(synthesis)
    save_file(".tmp/synthesis.md", synthesis_result)
    
    # Step 6: Deep Writer（深度报告）
    deep_writer = sessions_spawn(
        task="撰写深度调研报告...",
        label="HF-DeepWriter"
    )
    report_content = extract_content_from_completion(deep_writer)
    
    # Step 7: Multi-Checker（多维度质检）
    multi_checker = sessions_spawn(
        task="从五个维度检查报告...",
        label="HF-MultiChecker"
    )
    check_result = extract_content_from_completion(multi_checker)
    
    # Step 8: 迭代修订（如需要）
    revision_round = 0
    max_revisions = 3
    while "FAILED" in check_result and revision_round < max_revisions:
        critical_issues = extract_critical_issues(check_result)
        deep_writer = sessions_spawn(
            task=f"根据质检反馈修订报告...",
            label=f"HF-DeepWriter-Revision-{revision_round}"
        )
        report_content = extract_content_from_completion(deep_writer)
        multi_checker = sessions_spawn(
            task="重新检查修订后的报告...",
            label=f"HF-MultiChecker-Revision-{revision_round}"
        )
        check_result = extract_content_from_completion(multi_checker)
        revision_round += 1
    
    # Step 9: 保存最终报告
    save_report(report_content, template="deep_report_template.md", mode="deep")
    
    return report_content
```

### 统一入口

```python
def run_pipeline(user_request, days=None, research_topic=None):
    mode = determine_mode(user_request, days)
    
    if mode == "ask_user":
        mode = ask_user("您希望执行哪种模式？\n1. 轻量扫描（周期性追踪，≤30天）\n2. 深度调研（全面调研，>30天或不限时间）")
        mode = "light" if "1" in mode else "deep"
    
    if mode == "light":
        return run_light_scan(days=days or 7)
    else:
        topic = research_topic or ask_user("请输入深度调研的主题/方向：")
        return run_deep_research(topic, days=days)
```

## 目录结构

```
hf-daily-deep-researcher/
├── SKILL.md                          # 本文件（编排器定义）
├── init.py                           # 初始化配置（从环境提取）
├── config.json                       # 用户配置（动态生成）
├── keywords.json                     # 关键词权重表
├── adaptive.py                       # 关键词自适应模块
├── report_manager.py                 # 报告保存、版本控制
├── tracker.py                        # 编排器入口（读取配置，准备环境）
│
├── agents/                           # Agent 任务定义模板
│   ├── searcher_prompt.md            # 搜索策略参考（主Agent直接执行时参考）
│   ├── deep_reader_prompt.md         # Deep Reader Agent（精读单篇论文）
│   ├── analyst_prompt.md             # Analyst Agent（趋势分析）
│   ├── writer_prompt.md              # Writer Agent（周报撰写）
│   ├── checker_prompt.md             # Checker Agent（单一质检）
│   ├── sub_analyst_benchmark.md      # Sub-Analyst: Benchmark 现状
│   ├── sub_analyst_gap.md            # Sub-Analyst: 研究空白
│   ├── sub_analyst_code.md           # Sub-Analyst: 代码开源
│   ├── sub_analyst_authority.md      # Sub-Analyst: 权威性验证
│   ├── synthesis_analyst_prompt.md   # Synthesis Analyst（综合整合）
│   ├── deep_writer_prompt.md         # Deep Writer Agent（深度报告）
│   └── multi_checker_prompt.md       # Multi-Checker Agent（多维度质检）
│
├── templates/                        # 报告模板
│   ├── report_template.md            # 轻量扫描报告模板（周报/月报）
│   └── deep_report_template.md       # 深度调研报告模板
│
├── reports/                          # 输出报告（本地）
├── history/                          # 扫描历史
│   └── scan_history.json
│
└── .tmp/                             # 临时文件（Agent间传递）
    ├── papers_raw.json               # 主Agent搜索输出（轻量）
    ├── deep_papers_raw.json          # 主Agent搜索输出（深度）
    ├── paper_analysis_*.md           # Deep Reader 输出
    ├── analysis_summary.md           # Analyst 输出（轻量）
    ├── sub_benchmark.md              # Sub-Analyst 输出
    ├── sub_gap.md
    ├── sub_code.md
    ├── sub_authority.md
    ├── synthesis.md                  # Synthesis Analyst 输出
    └── check_result.md               # Checker 输出
```

## 快速开始

### 1. 初始化（首次使用）

```bash
python3 ~/.openclaw/workspace/skills/hf-daily-deep-researcher/init.py
```

这会尝试从 `USER.md` / `MEMORY.md` 自动提取你的研究方向。

**重要**：如果无法自动提取研究方向，配置中的 `research_focus` 将为空。**首次运行 skill 时，主 Agent 会询问你确认研究方向**（通过对话交互），无需手动修改配置文件。

### 2. 首次运行（主Agent执行）

```
# 在对话中要求执行
"运行 hf-daily-deep-researcher，扫描过去7天"
```

主Agent会：
1. 读取配置
2. **如果 research_focus 为空，向用户确认研究方向**（对话询问）
3. 根据确认的方向动态生成关键词
4. **主 Agent 直接执行搜索**（调用 kimi_search 等工具，不再启动 Searcher 子 Agent）
5. 启动 Deep Reader Agents（每篇 P0 论文一个子 Agent，等待 completion events）
6. 检测 Deep Reader 输出完整性，如有截断则自行补充阅读
7. 启动 Analyst + Writer + Checker（等待 completion events，提取内容）
8. 保存报告到本地和飞书

### 3. 自动追踪（Cron）

```json
{
  "name": "hf-weekly-research",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "运行 hf-daily-deep-researcher skill，执行完整工作流：搜索过去7天论文，深度精读P0/P1，生成报告并检查质量。追踪领域从 config.json 读取。"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

## 关键设计决策

### 为什么 Searcher 不用子 Agent？（v4.1.2 关键修复）

`sessions_spawn` 的 announce 机制存在根本性问题：**它不保证能拿到子 Agent 的完整最终输出**。

子 Agent 执行过程：thinking → toolCall → thinking → toolCall → 最终文本。announce 可能截取其中任意一轮，导致主 Agent 收到"开始搜索..."而非完整结果。

**v4.1.2 之前**（v4.0.4-v4.1.1）的缓解措施：
- 强化 Searcher Prompt 约束（要求最终轮一次性输出）
- 主 Agent 完整性检测
- 主 Agent 兜底搜索

**问题**：这些只是"缓解"，不是"解决"。Searcher 子 Agent 仍然可能输出截断，主 Agent 兜底搜索是二次工作，效率低。

**v4.1.2 的修复**：Searcher 阶段直接由主 Agent 执行。
- 主 Agent 调用 `kimi_search` 等工具，结果在主 Agent 上下文中
- 100% 避免截断问题
- 不需要完整性检测和兜底搜索
- 搜索策略（关键词组合、来源优先级）放在 `agents/searcher_prompt.md` 中供主 Agent 参考

### 为什么 Deep Reader 仍然用子 Agent？

Deep Reader 的情况不同：
1. **每篇论文一个独立 Agent**：输出量可控（一篇论文的分析）
2. **即使截断，主 Agent 可以检测并自行补充阅读**：单篇论文的阅读成本可控
3. **独立上下文的价值**：论文精读需要大量 token 空间，独立 Agent 避免上下文被其他论文淹没
4. **并行效率**：多篇论文可以并行精读

### 工具依赖与跨平台适配

本 Skill 依赖以下 OpenClaw 工具（按优先级排序）：

| 工具 | 用途 | 是否必需 | 替代方案 |
|------|------|----------|----------|
| `kimi_search` | 语义搜索 arXiv / HF | 否 | `web_fetch` 调 arXiv API |
| `web_fetch` | 获取 arXiv API / HF 页面 | **是** | `browser` 打开网页 |
| `browser` | 浏览器控制（fallback） | 否 | 无（可用性降低） |
| `feishu_create_doc` | 报告上传飞书 | 否 | 本地保存到 `reports/` |
| `sessions_spawn` | 启动子 Agent（Phase 2+） | **是** | 串行执行（效率降低） |

**跨平台使用说明**：
- **Kimi 平台**：完整功能，kimi_search + web_fetch + browser 都可用
- **Claude / GPT 平台**：可能没有 kimi_search，但通常有 web_fetch 和 browser
- **主 Agent 搜索已自动适配**：会根据当前可用工具选择最优搜索策略

### 错误处理

每个阶段：
1. **Phase 1（搜索）**：主 Agent 直接执行，无截断风险。如果搜索失败（如 kimi_search 返回空），尝试降级工具并继续
2. **Phase 2（精读）**：子 Agent 可能截断。主 Agent 检测完整性，如截断则自行下载论文补充分析
3. **Phase 3-5**：子 Agent 输出分析报告/报告/检查结果。如截断，主 Agent 可基于已有数据自行完成
4. **Checker 发现 critical 问题**：返回到对应 Agent 重新执行

## 版本历史

- **v4.1.2** (2026-07-03): **关键修复**：Searcher 阶段不再通过 `sessions_spawn` 启动子 Agent，改由主 Agent 直接执行搜索。彻底解决了子 Agent 输出截断导致的搜索结果不完整问题。Deep Reader 仍保留子 Agent，但每篇论文独立一个 Agent，并增加主 Agent 完整性检测与兜底阅读机制。
- **v4.1.1** (2026-07-02): ClawHub 发布版。修复工具引用一致性（deep_reader_prompt.md curl→browser/web_fetch）、版本号统一、移除未实现参数提示、分发包清理。
- **v4.1.0** (2026-06-30): 新增深度调研模式（Deep Research）。支持双模式自动判断。深度模式新增：Deep Searcher、4个并行 Sub-Analysts、Synthesis Analyst、Deep Writer、Multi-Checker、迭代修订。
- **v4.0.8** (2026-06-30): 清理默认配置残留。config.json folder_token 置空，keywords.json 默认清空，面向多用户分发优化。
- **v4.0.7** (2026-06-30): Deep Reader prompt 修正全文获取方案。Searcher 跨平台工具链明确优先级。
- **v4.0.6** (2026-06-30): 首次运行研究方向确认流程。
- **v4.0.5** (2026-06-30): 增加跨平台搜索工具适配。Searcher Prompt 支持三级降级。
- **v4.0.4** (2026-06-30): 修复子Agent输出截断问题（缓解措施：Prompt约束+完整性检测+兜底搜索）。
- **v4.0.3** (2026-06-29): 修正设计理念：信息准确 > 格式统一。
- **v4.0.2** (2026-06-29): 修复子 Agent 输出格式不稳定问题。
- **v4.0.0** (2026-06-29): 重写为多Agent编排架构。
- **v3.1.0** (2026-06-28): 新增报告管理模块，动态配置初始化
- **v3.0.1** (2026-06-27): 数据验证机制，修正 cron 配置
- **v3.0.0** (2026-06-27): 完善联动体系
- **v2.0.0** (2026-06-27): 新增深度精读方法论
- **v1.0.0** (2026-06-27): 初始版本
