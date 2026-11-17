---
name: hf-daily-deep-researcher
version: 5.2.9
description: |
  HuggingFace Daily Papers + arXiv 多Agent深度研究系统。
  采用编排器+专业Agent架构，支持两种模式：
  1. 轻量扫描模式：周期性追踪（周/月），发现新论文
  2. 深度调研模式：全时间范围调研，产出全面深入的研究报告
  支持动态配置、自适应关键词、周期版本控制、跨平台搜索工具适配。
---

# HF Daily Deep Researcher v5.2.9 — 多Agent编排版

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
    v5.2.3 关键改进：搜索阶段从"主次 fallback"改为"并行互补"，
    web_fetch 追新 + kimi_search 主题补充，结果合并去重，彻底避免遗漏。
    """
    all_results = []
    
    # === 工具可用性检测（v5.2.3 保留）===
    available_tools = {"kimi_search": False, "web_fetch": False, "browser": False}
    
    # 尝试 kimi_search（Kimi 平台特有）
    try:
        test_result = kimi_search("test query")
        available_tools["kimi_search"] = True
    except Exception:
        available_tools["kimi_search"] = False
    
    # 尝试 web_fetch（标准 OpenClaw 工具，最广泛可用）
    try:
        test_result = web_fetch("https://export.arxiv.org/api/query?search_query=all:test&max_results=1")
        available_tools["web_fetch"] = True
    except Exception:
        available_tools["web_fetch"] = False
    
    # 尝试 browser（部分环境可用）
    try:
        available_tools["browser"] = available_tools["web_fetch"]
    except Exception:
        available_tools["browser"] = False
    
    print(f"可用工具: kimi_search={available_tools['kimi_search']}, web_fetch={available_tools['web_fetch']}")
    
    # === v5.2.3 核心改动：并行互补搜索，而非主次 fallback ===
    # web_fetch 负责追新（arXiv API 按日期排序，时间精确，不漏最新论文）
    # kimi_search 负责主题补充（找 GitHub、博客、HuggingFace 讨论等跨平台资源）
    # 两套并行跑，结果合并去重
    
    for focus in focus_keywords:
        # --- 分支 1: web_fetch 追新（只要可用，必跑）---
        if available_tools["web_fetch"]:
            web_queries = generate_web_fetch_queries(focus, mode=mode)
            for query in web_queries:
                api_url = f"https://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=50"
                raw = web_fetch(api_url)
                results = parse_arxiv_api_results(raw)
                all_results.extend(results)
        
        # --- 分支 2: kimi_search 主题补充（仅当可用时跑）---
        if available_tools["kimi_search"]:
            kimi_queries = generate_kimi_search_queries(focus, mode=mode)
            for query in kimi_queries:
                results = kimi_search(query)
                all_results.extend(results)
    
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
- 来源：
  - **arXiv API**（主力追新，按提交日期排序）
  - **HuggingFace Daily Papers（GitHub 镜像 JSON）**（核心 curated 数据源，与 arXiv 并列。社区 upvote 筛选 + star 数参考）
  - **GitHub**（代码资源）

**HF Daily Papers 数据源（v5.2.9 更新）**：

本 Skill 通过 **GitHub 镜像 JSON** 获取 HuggingFace Daily Papers 的 curated 内容，替代直接访问 HF 官方 API。

**数据源**：
```
https://raw.githubusercontent.com/AtharvaDomale/Daily-HuggingFace-AI-Papers/main/data/latest.json
```

**为什么用 GitHub 镜像？**
- **稳定可靠**：GitHub raw content CDN 全球可用，不受 HF 网络封锁影响
- **一次请求拿全量**：无需逐页翻，一次 `curl` 拉取最近几天的全部 curated 论文
- **结构化数据**：JSON 格式，包含标题、摘要、作者、arXiv ID、HF star 数、GitHub 链接
- **自动更新**：上游 repo 每日通过 GitHub Actions 自动同步

**使用方法**：
1. 搜索阶段通过 `exec "curl ..."` 拉取完整 JSON
2. 本地按 `scraped_date` 筛选目标日期范围
3. 对标题+摘要做关键词匹配，按研究方向过滤
4. HF star 数高的论文优先保留（社区 curated 的高质量内容）
5. 与 arXiv API 结果按 arXiv ID 合并去重

**降级策略**（GitHub 镜像不可用时）：
1. 尝试官方 HF API：`https://huggingface.co/api/daily_papers?date=YYYY-MM-DD`
2. 如果官方 API 也不可用 → 执行 arXiv 补偿搜索（增加 4 组额外查询）
3. 在搜索报告中明确标注数据源状态和降级原因

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
        label=f"HF-DeepReader-{paper['arxiv_id']}",
        runTimeoutSeconds=900  # 15 分钟
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
            label=f"HF-DeepReader-{paper['arxiv_id']}",
            runTimeoutSeconds=900
        )
        reader_tasks.append((paper['arxiv_id'], task))
    
    for arxiv_id, task in reader_tasks:
        content = extract_content_from_completion(task)
        if not check_reader_completeness(content):
            content = perform_backup_reading(arxiv_id)
        save_file(f".tmp/paper_analysis_{arxiv_id}.md", content)
    
    # Step 4: Analyst（趋势分析）
    analyst = sessions_spawn(
        task="分析趋势...",
        label="HF-Analyst",
        runTimeoutSeconds=600
    )
    analysis_content = extract_content_from_completion(analyst)
    save_file(".tmp/analysis_summary.md", analysis_content)
    
    # Step 5: Writer（周报）
    writer = sessions_spawn(
        task="撰写周报...",
        label="HF-Writer",
        runTimeoutSeconds=900
    )
    report_content = extract_content_from_completion(writer)
    
    # Step 6: Checker（单一质检）
    checker = sessions_spawn(
        task="检查周报质量...",
        label="HF-Checker",
        runTimeoutSeconds=600
    )
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
            label=f"HF-DeepReader-{paper['arxiv_id']}",
            runTimeoutSeconds=900
        )
        reader_tasks.append((paper['arxiv_id'], task))
    # 重要的 improvement 也要精读
    for paper in improvement_papers[:10]:
        task = sessions_spawn(
            task=f"精读改进论文 {paper['arxiv_id']}...",
            label=f"HF-DeepReader-{paper['arxiv_id']}",
            runTimeoutSeconds=900
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
        label="HF-SubAnalyst-Benchmark",
        runTimeoutSeconds=600
    )
    gap_analyst = sessions_spawn(
        task="识别研究空白与可做方向...",
        label="HF-SubAnalyst-Gap",
        runTimeoutSeconds=600
    )
    code_analyst = sessions_spawn(
        task="检查代码开源情况...",
        label="HF-SubAnalyst-Code",
        runTimeoutSeconds=600
    )
    authority_analyst = sessions_spawn(
        task="验证论文权威性与引用准确性...",
        label="HF-SubAnalyst-Authority",
        runTimeoutSeconds=600
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
        label="HF-Synthesis-Analyst",
        runTimeoutSeconds=600
    )
    synthesis_result = extract_content_from_completion(synthesis)
    save_file(".tmp/synthesis.md", synthesis_result)
    
    # Step 6: Deep Writer（深度报告）
    deep_writer = sessions_spawn(
        task="撰写深度调研报告...",
        label="HF-DeepWriter",
        runTimeoutSeconds=1200
    )
    report_content = extract_content_from_completion(deep_writer)
    
    # Step 7: Multi-Checker（多维度质检）
    multi_checker = sessions_spawn(
        task="从14个核心维度+2个可选维度检查报告...",
        label="HF-MultiChecker",
        runTimeoutSeconds=600
    )
    check_result = extract_content_from_completion(multi_checker)
    
    # Step 8: 迭代修订（如需要）
    revision_round = 0
    max_revisions = 3
    while "FAILED" in check_result and revision_round < max_revisions:
        critical_issues = extract_critical_issues(check_result)
        deep_writer = sessions_spawn(
            task=f"根据质检反馈修订报告...",
            label=f"HF-DeepWriter-Revision-{revision_round}",
            runTimeoutSeconds=1200
        )
        report_content = extract_content_from_completion(deep_writer)
        multi_checker = sessions_spawn(
            task="重新检查修订后的报告...",
            label=f"HF-MultiChecker-Revision-{revision_round}",
            runTimeoutSeconds=600
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

### 1. 安装

```bash
# 从 ClawHub 安装
openclaw skills install @tomfoxxxx/hf-daily-deep-researcher
```

安装后，Skill 会出现在你的 workspace 的 `skills/` 目录下。

---

### 2. 研究方向是什么

**研究方向 = 一个研究领域 + 一组相关关键词**

每个方向不是单个关键词，而是一组相关概念的集合。系统会用这组关键词去搜索和追踪论文。

**示例**：

| 方向名称 | 包含的关键词 |
|---------|-------------|
| **Credit Assignment** | multi-agent credit assignment, hindsight credit, stepwise reward, turn-level advantage, process reward model, hierarchical credit |
| **OPD** | token importance, OPD RL joint training, online preference distillation, preference optimization |
| **多模态** | visual perception, image reasoning, multimodal understanding, multimodal agent, vision language model |

你可以配置多个方向。每个方向独立追踪，也可以合并搜索。

---

### 3. 首次使用配置

**方式一：对话触发（推荐）**

直接在对话中对主 Agent 说：
```
运行 hf-daily-deep-researcher，扫描过去7天
```

主 Agent 会：
1. 读取 `config.json`
2. 如果 `research_focus` 为空（首次使用），**引导你配置研究方向**：
   > "请配置你的研究方向。每个方向需要一个名称和一组相关关键词。"
   > 
   > "示例："
   > "- 方向1 'Credit Assignment'：multi-agent credit assignment, hindsight credit, stepwise reward..."
   > "- 方向2 'OPD'：token importance, OPD RL joint training..."
   > "- 方向3 '多模态'：visual perception, image reasoning..."
   > 
   > "请输入你的方向（格式：方向名: 关键词1, 关键词2, 关键词3）"
3. 你回复后，主 Agent 自动保存配置，开始搜索

**方式二：手动运行 init.py**

```bash
python3 ~/.openclaw/workspace/skills/hf-daily-deep-researcher/init.py
```

这会尝试从你的 `USER.md` / `MEMORY.md` 自动提取研究方向。如果提取不到，config.json 中的 `research_focus` 将为空，首次运行时主 Agent 仍会询问。

**配置完成后**，后续运行直接读取 `config.json`，不再重复询问。

**config.json 中的方向格式**：
```json
{
  "user_profile": {
    "research_focus": [
      {
        "name": "Credit Assignment",
        "keywords": ["multi-agent credit assignment", "hindsight credit", "stepwise reward"]
      },
      {
        "name": "OPD",
        "keywords": ["token importance", "OPD RL joint training", "online preference distillation"]
      }
    ]
  }
}
```

---

### 4. 运行方式

配置多个方向后，有三种运行方式：

**方式一：合并搜索（默认）**
```
运行 hf-daily-deep-researcher，扫描过去7天
```
所有方向的关键词合并去重，一次性搜索，生成一份综合报告。

**方式二：指定方向**
```
运行 hf-daily-deep-researcher，扫描过去7天，方向：Credit Assignment
```
只取该方向的关键词集合搜索，生成该方向的独立报告。

**方式三：每个方向单独生成报告**
```
运行 hf-daily-deep-researcher，扫描过去7天，每个方向单独生成报告
```
依次为每个方向独立运行完整工作流，最终产出多篇独立报告。

---

### 5. 深度调研

```
运行 hf-daily-deep-researcher，深度调研 Credit Assignment
```
主 Agent 自动判断为深度模式，全时间范围搜索该方向，产出深度调研报告。

---

### 6. 飞书文档输出

本 Skill 支持将报告上传到飞书文档。**强烈建议安装飞书插件并关联飞书文档**，报告会自动上传到飞书，阅读体验远优于本地 Markdown。

> 本地 Markdown 需要手动打开文件，无格式渲染、无目录导航、不便分享。飞书文档支持富文本、表格、协作评论和链接分享。

**配置方式**：安装飞书插件后，在对话中授权关联飞书文档即可。首次配置需要完成 OAuth 授权，后续报告会自动上传。

---

### 7. 自动追踪（Cron）

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

---
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

## Multi-Agent 调度与超时策略

### 核心原则：区分"在干活"与"卡死"

子 Agent 超时不等于失败。可能是：
- **正常慢**：论文下载慢、PDF 解析慢、长论文内容多
- **网络问题**：arXiv 连接超时、工具调用失败
- **真卡死**：陷入循环、遇到无法处理的输入

**不应直接接管"在干活"的子 Agent**——会丢失中间成果。应采用**阶段性超时 + 弹性检测**策略。

### 阶段性超时配置

| 阶段 | 建议超时 | 理由 |
|------|----------|------|
| Phase 1 搜索 | 无（主Agent直接执行） | 无子Agent |
| Phase 2 Deep Reader | **15 分钟** | 论文下载+精读，长论文需要 |
| Phase 3 Analyst | **10 分钟** | 分析已有内容，不涉下载 |
| Phase 4 Writer | **15-20 分钟** | 深度报告撰写量大 |
| Phase 5 Checker | **10 分钟** | 检查报告，纯分析 |
| 迭代修订 | **同 Writer** | 修订与撰写同量级 |

**代码示例**：
```python
# Deep Reader — 论文精读，给充足时间
sessions_spawn(
    task="精读论文 arXiv:2605.25507...",
    label="HF-DeepReader-2605.25507",
    runTimeoutSeconds=900  # 15 分钟
)

# Deep Writer — 深度报告撰写
sessions_spawn(
    task="撰写深度调研报告...",
    label="HF-DeepWriter",
    runTimeoutSeconds=1200  # 20 分钟
)
```

### 弹性超时：不直接接管

**超时后的处理流程**：

```python
def handle_subagent_timeout(task, expected_stage="deep_read"):
    """
    子Agent超时后的弹性处理
    """
    # Step 1: 检查是否有部分输出
    partial_output = check_partial_result(task)
    
    if partial_output and len(partial_output) > 500:
        # 有实质性部分输出 → 标记为"部分完成"，不接管
        print(f"⚠️ 子Agent超时，但有{len(partial_output)}字部分输出，保留等待或延长超时")
        return {"status": "partial", "content": partial_output}
    
    # Step 2: 检查是否有进度汇报
    progress = check_progress_report(task)
    if progress and progress.get("stage"):
        print(f"⏳ 子Agent进度: {progress['stage']}，延长超时")
        return {"status": "extend", "progress": progress}
    
    # Step 3: 真的卡死/无输出 → 主Agent兜底
    print(f"❌ 子Agent无实质性输出，主Agent接管")
    return {"status": "fallback", "content": perform_backup_task(expected_stage)}
```

**关键设计**：
1. **有输出就不接管**：子 Agent 已产出部分分析，应回收而非丢弃
2. **有进度就延长**：子 Agent 报告了进度（如"已读完方法部分，正在提取实验数据"），延长超时
3. **完全无输出才兜底**：确认子 Agent 确实卡死，主 Agent 才接管

### 子 Agent 进度汇报机制

在子 Agent Prompt 中增加进度要求：

```
# 在 deep_reader_prompt.md / writer_prompt.md 等中增加：

⚠️ 超时保护：本任务可能超时。为避免被主Agent误判为卡死：
- 如果执行时间预计超过5分钟，在开始后2分钟输出一次进度汇报：
  "进度汇报：当前正在[具体阶段]，预计还需[X]分钟"
- 如果下载论文耗时较长，先输出："正在下载论文，请稍候..."
- 如果分析已部分完成（如方法已读完，实验待提取），输出：
  "进度汇报：已完成[已完成部分]，剩余[剩余部分]"
```

### 分片策略：控制单 Agent 工作量

避免单个 Agent 任务过重导致超时：

| Agent 类型 | 单任务工作量 | 超时依据 |
|-----------|-------------|---------|
| Deep Reader | 1 篇论文 | 论文长度决定 |
| Analyst | 3-5 篇论文分析 | 内容复杂度 |
| Sub-Analyst | 单一维度（如仅Benchmark） | 分析范围可控 |
| Writer | 完整报告 | 报告长度决定 |

**原则**：宁可多启动几个 Agent（并行），也不把太多工作塞进一个 Agent。

### 工具依赖与跨平台适配（v5.2.0/5.2.1 重要更新）

本 Skill 设计目标是**在任何标准 OpenClaw 环境中都能正常运行**，不依赖特定平台的专属工具。

#### 核心原则：运行时检测 + 并行互补（v5.2.3 修正）

**v5.2.0 之前的问题**：默认假设 `kimi_search` 一定存在。在非 Kimi 平台中，这些工具直接不存在，导致 Skill 无法运行。

**v5.2.0 的修复**：主 Agent 在搜索阶段**先检测当前环境有哪些工具可用**，然后选择最优工具链。

**v5.2.3 的改进**：从"主次 fallback"升级为"并行互补"。
- **实验发现**：`kimi_search` 在"追新"方面存在系统性遗漏（日期过滤失效），而 `web_fetch`（arXiv API）在时间精确度上显著更优
- **新策略**：
  - **web_fetch 追新**：arXiv API 按 `submittedDate` 排序，时间精确，不漏最新论文
  - **kimi_search 主题补充**：找 GitHub、博客、HuggingFace 讨论等跨平台资源
  - **两套并行跑，结果合并去重**

#### 工具链职责分工（v5.2.3）

| 工具 | 职责 | 适用平台 | 搜索能力 | 获取论文能力 |
|--------|------|----------|----------|-------------|
| **web_fetch** | **追新主力**（必跑） | 任何 OpenClaw | 中（arXiv API 按日期排序） | 中（arXiv API / arXiv HTML） |
| **kimi_search** | **主题补充**（可选） | Kimi/OpenClaw | 强（语义搜索） | 强（直接获取 HTML） |
| **browser** | 兜底 | 部分环境 | 弱（页面抓取） | 弱（页面渲染） |

**最低要求**：`web_fetch` 必须可用。如果 `web_fetch` 和 `kimi_search` 都没有，Skill 会报错并提示用户。

#### 各平台预期表现

| 平台 | web_fetch | kimi_search | browser | Skill 可用性 |
|------|-----------|-------------|---------|-------------|
| **Kimi/OpenClaw** | ✅ | ✅ | ✅ | 完整功能（双轨并行） |
| **开源 OpenClaw** | ✅ | ❌ | 视配置 | 核心功能正常（web_fetch 单轨） |
| **Claude Code** | ✅ | ❌ | ✅ | 核心功能正常（web_fetch 单轨） |
| **CodeX** | ✅ | ❌ | 视配置 | 核心功能正常（web_fetch 单轨） |

#### web_fetch 方案详述（跨平台主力 + 追新主力）

**搜索论文**：
```python
# arXiv API（Atom XML 格式）
web_fetch("https://export.arxiv.org/api/query?search_query=all:KEYWORD&sortBy=submittedDate&sortOrder=descending&max_results=50")

# HuggingFace Daily Papers
web_fetch("https://huggingface.co/papers?date=YYYY-MM-DD")
```

**获取论文全文**：
```python
# arXiv 原生 HTML（最可靠的全文获取方式）
web_fetch("https://arxiv.org/html/2606.XXXXX")

# arXiv 抽象页（备用）
web_fetch("https://arxiv.org/abs/2606.XXXXX")
```

**解析要求**：主 Agent 需要能解析 arXiv API 返回的 Atom XML（提取 title, summary, author, published, id），以及 arXiv HTML（提取论文正文）。

#### kimi_search 方案详述（主题补充）

当 kimi_search 可用时，作为**补充轨道**并行运行：

**搜索职责**：
- 找 arXiv 之外的资源（GitHub 仓库、技术博客、HuggingFace 讨论）
- 语义搜索发现标题/摘要中未直接出现关键词的相关论文
- 验证 web_fetch 找到的论文的社区讨论热度

**不承担的职责**：
- 不作为"追新"的唯一来源（日期过滤不可靠）
- 不替代 web_fetch 的 arXiv API 搜索

#### 错误处理

每个阶段：
1. **Phase 1（搜索）**：
   - web_fetch 轨道：始终执行（只要可用），负责追新
   - kimi_search 轨道：并行执行（如果可用），负责主题补充
   - 两套结果合并去重，确保不遗漏
2. **Phase 2（精读）**：子 Agent 的 Deep Reader Prompt 中已包含工具检测逻辑（见 `deep_reader_prompt.md`）。优先尝试 `web_fetch` → `kimi_fetch` → `browser`。
3. **Phase 3-5**：不直接依赖搜索工具，正常执行。
4. **飞书上传**：`feishu_create_doc` 是可选功能。如果不可用，报告保存到本地 `reports/` 目录。

## 版本历史
- **v5.2.9** (2026-08-25): **HF 数据源重构 — GitHub 镜像替代直接 API**。解决 HF 官方 API 在网络受限环境中的可用性问题：
  - 将 HF Daily Papers 数据源从直接访问 `huggingface.co/api/daily_papers` 改为 **GitHub 镜像 JSON**（`raw.githubusercontent.com/AtharvaDomale/Daily-HuggingFace-AI-Papers/main/data/latest.json`）
  - 新增 `exec`（curl）工具链支持，一次请求拉取全量 curated 论文数据
  - searcher_prompt.md: 重写 HF 数据源获取逻辑（A4 步骤），增加 JSON 解析和关键词过滤说明
  - deep_searcher_prompt.md: 更新工具检测和自检清单，GitHub 镜像作为可选补充
  - SKILL.md: 重写 HF Daily Papers 数据源说明，移除网络可用性警告，改为 GitHub 镜像使用指南
  - 所有文件版本号统一为 5.2.9

- **v5.2.8** (2026-08-06): **深度调研模式增强**。提升深度调研的广度和报告质量：
  - deep_searcher_prompt.md: 搜索查询从 12 组增加到**强制 15 组**，新增引用链扩展搜索和关键作者追踪
  - deep_reader_prompt.md: milestone 论文超时延长至 **25 分钟**，新增引用关系分析（依赖工作/技术路线位置）
  - deep_report_template.md: 新增技术演进时间线、饱和度分级（🔴🟡🟢🔵）、方法簇覆盖度矩阵
  - sub_analyst_benchmark.md: 新增方法×Benchmark 交叉覆盖分析、时间维度饱和度趋势
  - sub_analyst_gap.md: 新增基于饱和度的方向推荐、方法簇覆盖度矩阵
  - 所有文件版本号统一为 5.2.8

- **v5.2.7** (2026-08-06): **P0 质量修复 + 隐私清理**。修复搜索覆盖不足和数据验证缺失问题：
  - searcher_prompt.md: 8 组 arXiv + 6 组 kimi_search 从"建议"升级为**强制下限**
  - deep_reader_prompt.md: 每个实验数据强制标注 [V]/[C]/[U] 验证级别
  - writer_prompt.md: 每篇 P0/P1 论文强制列出 benchmark 名称和具体分数
  - checker_prompt.md: 新增阻塞性问题定义（未标注验证级别 = FAILED）
  - dist 去隐私化清理：name="User", research_focus=[], folder_token=""
  - 所有文件版本号统一为 5.2.7

- **v5.2.5** (2026-08-05): **网络诊断增强 + 质量改进**。解决 HuggingFace 在中国大陆网络环境被 DNS 污染 + SNI 阻断的问题：
  - searcher_prompt.md 增加 HF 可用性检测和网络诊断逻辑
  - SKILL.md 增加 HF API 网络可用性说明和用户解决方案
  - config.json 增加 `network.proxy` 配置段，支持用户配置代理
  - multi_checker_prompt.md 增加历史已知问题检查点（3SPO 数据错误、ARPO ID 错误、模型规模混用等）
  - deep_writer_prompt.md 强化数据验证标准和历史教训
  - 所有文件版本号统一为 5.2.5

- **v5.2.3** (2026-08-04): **搜索策略重要修正**。从"主次 fallback"升级为"并行互补"：
  - web_fetch（arXiv API）提升为**追新主力**，始终执行
  - kimi_search 降级为**主题补充**，并行运行但不承担追新主责
  - 实验数据支撑：7/29 对比实验中，kimi_search 只找到 1 篇 7 月论文，web_fetch 找到 7 篇，两方案零交集
  - 彻底避免 kimi_search 日期过滤失效导致的信息遗漏

- **v5.2.0** (2026-07-29): **跨平台兼容性重大改进**。解决 Skill 在非 Kimi 平台（开源 OpenClaw、Claude Code、CodeX）无法运行的问题：
  - 搜索阶段增加运行时工具可用性检测（kimi_search → web_fetch → browser），不再假设 kimi_search 一定存在
  - web_fetch + arXiv API 被提升为跨平台主力方案，详细文档化
  - 各 Prompt 文件（searcher/deep_reader/deep_searcher）统一更新工具选择逻辑
  - 明确最低要求：web_fetch 或 kimi_search 至少一个可用
  - 新增平台兼容性矩阵（Kimi/开源 OpenClaw/Claude Code/CodeX）

- **v5.1.2** (2026-07-24): 简化首次配置体验。飞书文档输出说明精简为"安装飞书插件并关联飞书文档"。多方向概念重新梳理：`research_focus` 是多个研究方向的列表，每个方向是一组相关关键词的集合，支持指定方向运行和批量生成所有方向的独立报告。

- **v5.1.1** (2026-07-24): 新增 Multi-Agent 调度与超时策略章节。明确阶段性超时配置（Deep Reader 15min / Writer 20min）。增加弹性超时处理：超时后不直接接管，先检查部分输出和进度汇报。完善首次使用配置流程：对话触发 → 自动询问研究方向 → 保存配置 → 后续直接读取。所有子 Agent 调用示例补充 `runTimeoutSeconds` 参数。

- **v5.1.0** (2026-07-24): 全局版本号统一（SKILL.md / tracker.py / prompt / checklist / _meta.json / skill-card）。补全版本历史记录。清理 checklist.md 硬编码文档ID。修复 deep_writer_prompt / multi_checker_prompt 版本标注滞后。清理 ClawHub 分发包个人报告残留。

- **v5.0.0** (2026-07-18): 用户工作状态同步（留在华为）。云盘归档完成。Skill 本地/远程版本同步流程建立。_meta.json 和 skill-card.md 版本更新。
- **v4.5.0** (2026-07-14): 强化质检体系。Multi-Checker 从 8 维扩展到 14 维核心 + 2 维可选维度，新增：技术洞察力、未来预判合理性、实操路径可行性、数学与理论严谨性、数据效率分析、组合矩阵覆盖度。新增独立 `agents/checklist.md` 文件供人工复核。修复安全规范强化：禁止空头承诺，唯一可靠路线为下载→本地修复→overwrite覆盖。

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
