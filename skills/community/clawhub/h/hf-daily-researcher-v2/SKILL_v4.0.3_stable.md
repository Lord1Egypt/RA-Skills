---
name: hf-daily-deep-researcher
version: 4.0.3
description: |
  HuggingFace Daily Papers + arXiv 多Agent深度研究系统。
  采用编排器+专业Agent架构，自动追踪、精读、分析、报告生成、质量检查。
  支持动态配置、自适应关键词、周期版本控制。
---

# HF Daily Deep Researcher v4 — 多Agent编排版

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    编排器 (Orchestrator)                          │
│                   — 主Agent执行，非独立脚本                        │
├──────────┬──────────┬──────────┬──────────┬──────────────────────┤
│ Searcher │  Deep    │  Deep    │  Analyst │  Writer   │  Checker │
│  (搜索)  │ Reader 1 │ Reader N │ (分析)   │ (撰写)    │ (质检)   │
└──────────┴──────────┴──────────┴──────────┴──────────┴───────────┘
```

**为什么用多Agent？**
- 搜索需要频繁调用 kimi_search，单Agent上下文会被搜索结果淹没
- 精读每篇论文需要大量 token，并行处理多论文会截断
- 分析需要跨论文对比，需要所有论文数据就位后才能开始
- 质量检查必须是独立视角，不能和撰写共享上下文

## 数据传递模式（⚠️ 重要）

子 Agent 通过 `sessions_spawn` 启动，**环境隔离导致它们无法直接写入主 Agent 的文件系统**。工作流采用以下模式：

```
子 Agent 执行任务 → 将结果输出到回复/announce
主 Agent 接收 completion event → 提取内容（容错解析）
主 Agent 写入 .tmp/ 文件 → 后续阶段读取
```

**关键设计原则：信息准确 > 格式统一**

- 搜索信息来源多样（arXiv、HuggingFace、GitHub、gist 等），格式不可能标准化
- 子 Agent 负责搜索和整理，**主 Agent 负责解析和结构化**
- 不要求子 Agent 输出固定格式（如 JSON），只要求信息完整
- 主 Agent 从子 Agent 的输出中提取关键字段，组织成结构化数据

**主 Agent 负责**：
1. 启动子 Agent 并等待 completion event
2. 从 completion event 的返回内容中**容错提取**数据（正则、关键词匹配、结构化解析）
3. 将数据写入 `.tmp/` 目录供后续阶段使用
4. 在子 Agent 任务描述中明确告知："不要写入文件，直接输出内容到回复"
5. 如果子 Agent 输出格式不完整，主 Agent 补充提取或手动补充搜索

### Phase 1: 搜索 (Searcher Agent)

**输入**: config.json + keywords.json
**输出**: 子 Agent 在回复中输出搜索结果 → 主 Agent 提取并解析为 `papers_raw.json`

**任务定义**:
```
你是一名论文搜索Agent。任务：
1. 读取 config.json 和 keywords.json
2. 根据 research_focus 和 keywords，使用 kimi_search 搜索 arXiv 和 HuggingFace Daily Papers
3. 计算优先级，过滤黑名单
4. 在回复中直接输出搜索结果的完整文本（不要写入文件）
   - 输出格式不限（列表、摘要、原始结果均可）
   - 但每篇论文必须包含：arXiv ID、标题、作者、机构、摘要、日期、优先级
```

**主 Agent 解析逻辑**:
```python
# 从子 Agent 的回复中提取论文信息
# 策略：正则匹配、关键词提取、结构化解析
# 容错：如果子 Agent 返回原始搜索结果，主 Agent 手动提取关键字段
papers = []
for line in result.split('\n'):
    # 提取 arXiv ID
    if match := re.search(r'arxiv[:/]?(\d{4}\.\d+)', line):
        arxiv_id = match.group(1)
    # 提取标题、作者、日期等...
```

**调用方式**:
```python
# 主 Agent 通过 sessions_spawn 启动 Searcher
searcher = sessions_spawn(
    task="读取 config.json 和 keywords.json，搜索论文，在回复中输出完整搜索结果",
    label="HF-Searcher"
)
# 等待 completion event
# 从 event 中提取搜索结果，解析并写入 .tmp/papers_raw.json
papers = parse_search_result(searcher_result)
save_json(".tmp/papers_raw.json", papers)
```

### Phase 2: 深度精读 (Deep Reader Agents — 并行)

**输入**: 单篇论文 arXiv ID + 已有工作上下文
**输出**: 子 Agent 在回复中输出分析 → 主 Agent 提取并保存为 `paper_analysis_{arxiv_id}.md`

**任务定义**:
```
你是一名论文精读Agent。任务：
1. 下载论文 arXiv HTML 实验版（完整无截断）
2. 分段提取核心内容（方法、公式、实验数据）
3. 数据三级验证（自检 → 交叉核对 → 标注验证级别）
4. 在回复中直接输出完整的 Markdown 分析报告（不要写入文件）
```

**调用方式**:
```python
# 主 Agent 并行启动多个 Deep Reader（每篇 P0 论文一个）
reader1 = sessions_spawn(task="精读 SCPO 论文，在回复中输出完整分析", label="HF-DeepReader-SCPO")
reader2 = sessions_spawn(task="精读 OPID 论文，在回复中输出完整分析", label="HF-DeepReader-OPID")
# 等待所有 completion events
# 从每个 event 中提取分析内容并写入 .tmp/paper_analysis_*.md
```

**并行策略**:
- P0 论文：每篇一个独立 Deep Reader Agent（并行）
- P1 论文：每2-3篇一个 Agent（减少并行数）
- P2/P3：不精读，仅记录基本信息

### Phase 3: 综合分析 (Analyst Agent)

**输入**: 主 Agent 提供论文分析文件路径（或内容摘要）
**输出**: 子 Agent 在回复中输出分析 → 主 Agent 提取并保存为 `analysis_summary.md`

**任务定义**:
```
你是一名研究分析Agent。任务：
1. 读取所有论文分析内容（主 Agent 会在任务描述中提供）
2. 识别方法簇、分析趋势变化
3. 评估对当前研究项目的潜在影响
4. 在回复中直接输出结构化分析（不要写入文件）
```

**调用方式**:
```python
# 主 Agent 启动 Analyst
analyst = sessions_spawn(
    task="分析以下论文的关联和趋势...",
    label="HF-Analyst"
)
# 从 event 中提取分析内容并写入 .tmp/analysis_summary.md
```

### Phase 4: 报告撰写 (Writer Agent)

**输入**: 主 Agent 提供论文列表 + 分析内容 + 报告模板
**输出**: 子 Agent 在回复中输出报告 → 主 Agent 提取并保存为报告文件

**任务定义**:
```
你是一名报告撰写Agent。任务：
1. 根据提供的论文列表和分析内容
2. 按统一模板组织完整报告
3. 在回复中直接输出完整报告内容（不要写入文件）
```

**调用方式**:
```python
# 主 Agent 启动 Writer
writer = sessions_spawn(
    task="撰写报告，输入数据...",
    label="HF-Writer"
)
# 从 event 中提取报告内容并保存到 reports/weekly_report_YYYY-MM-DD.md
```

**报告模板**（保留在 `templates/report_template.md`）:
```markdown
# 论文追踪报告

**生成时间**: {date}
**追踪区间**: {start_date} 至 {end_date}
**研究领域**: {research_focus}
**追踪关键词**: {keywords}
**总计发现**: {count} 篇相关论文

---

## 1. 执行摘要

## 2. 新论文统计与优先级分布

## 3. P0 论文深度分析

### 3.x {论文标题}

#### 基本信息
#### 核心动机
#### 核心方法
#### 实验结果（三级验证）
#### 与已有工作对比
#### 判断

## 4. P1 论文概述

## 5. 方法簇识别与趋势变化

## 6. 对当前研究项目的潜在影响

## 7. 值得关注的新方向

## 8. 数据验证声明

## 9. 附录：与历史报告的去重对比
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

**调用方式**:
```python
# 主 Agent 启动 Checker
checker = sessions_spawn(
    task="检查以下报告质量...",
    label="HF-Checker"
)
# 从 event 中提取检查结果
```

**不通过时的处理**:
- 主 Agent 读取检查结果
- 根据 issues 的严重程度：
  - critical: 返回到对应 Agent 重新执行
  - warning: 记录并继续
  - info: 记录，不影响发布

## 执行流程（编排器逻辑）

```python
# 伪代码，实际由主Agent按步骤执行

def run_pipeline(days=7, mode="deep"):
    # Step 1: 读取配置
    config = load_config()
    focus = config["user_profile"]["research_focus"]
    
    # Step 2: 启动 Searcher
    searcher = sessions_spawn(
        task="读取 config.json 和 keywords.json，搜索论文，在回复中输出完整搜索结果",
        label="HF-Searcher"
    )
    # 等待 completion event，提取搜索结果并解析为结构化数据
    papers = parse_search_result(searcher_result)
    save_json(".tmp/papers_raw.json", papers)
    
    # Step 3: 并行启动 Deep Readers
    p0_papers = [p for p in papers if p["priority"] >= 0.8]
    p1_papers = [p for p in papers if 0.6 <= p["priority"] < 0.8]
    
    reader_tasks = []
    for paper in p0_papers:
        task = f"精读论文 {paper['arxiv_id']}，在回复中输出完整 Markdown 分析"
        reader_tasks.append(sessions_spawn(task=task, label=f"HF-DeepReader-{paper['arxiv_id']}"))
    
    # 等待所有 completion events
    for task in reader_tasks:
        content = extract_content_from_completion(task)
        save_file(f".tmp/paper_analysis_{paper['arxiv_id']}.md", content)
    
    # Step 4: 启动 Analyst
    analysis_task = "分析以下论文的关联和趋势..."
    analyst = sessions_spawn(task=analysis_task, label="HF-Analyst")
    analysis_content = extract_content_from_completion(analyst)
    save_file(".tmp/analysis_summary.md", analysis_content)
    
    # Step 5: 启动 Writer
    writer_task = "撰写报告..."
    writer = sessions_spawn(task=writer_task, label="HF-Writer")
    report_content = extract_content_from_completion(writer)
    
    # Step 6: 启动 Checker
    checker_task = "检查以下报告质量..."
    checker = sessions_spawn(task=checker_task, label="HF-Checker")
    check_result = extract_content_from_completion(checker)
    
    if "FAILED" in check_result:
        # 根据问题返工
        pass
    
    # Step 7: 保存报告
    save_report(report_content, mode=mode, days=days)
    
    return report_content
```

## 目录结构

```
hf-daily-deep-researcher/
├── SKILL.md                    # 本文件（编排器定义）
├── init.py                     # 初始化配置（从环境提取）
├── config.json                 # 用户配置（动态生成）
├── keywords.json               # 关键词权重表
├── adaptive.py                 # 关键词自适应模块
├── report_manager.py           # 报告保存、版本控制
├── tracker.py                  # 编排器入口（读取配置，准备环境）
│
├── agents/                     # Agent 任务定义模板
│   ├── searcher_prompt.md      # Searcher Agent 任务定义
│   ├── deep_reader_prompt.md   # Deep Reader Agent 任务定义
│   ├── analyst_prompt.md       # Analyst Agent 任务定义
│   ├── writer_prompt.md        # Writer Agent 任务定义
│   └── checker_prompt.md       # Checker Agent 任务定义
│
├── templates/                  # 报告模板
│   └── report_template.md      # 标准报告模板
│
├── reports/                    # 输出报告（本地）
├── history/                    # 扫描历史
│   └── scan_history.json
│
└── .tmp/                       # 临时文件（Agent间传递）
    ├── papers_raw.json         # Searcher 输出（主 Agent 解析后写入）
    ├── paper_analysis_*.md     # Deep Reader 输出（主 Agent 写入）
    ├── analysis_summary.md     # Analyst 输出（主 Agent 写入）
    └── check_result.md         # Checker 输出（主 Agent 写入）
```

## 快速开始

### 1. 初始化（首次使用）

```bash
python3 ~/.openclaw/workspace/skills/hf-daily-deep-researcher/init.py
```

这会从 `USER.md` / `MEMORY.md` 自动提取你的研究方向和关键词。

### 2. 手动运行（主Agent执行）

```
# 在对话中要求执行
"运行 hf-daily-deep-researcher，扫描过去7天"
```

主Agent会：
1. 读取配置
2. 启动 Searcher Agent（等待 completion event，解析搜索结果）
3. 启动 Deep Reader Agents（等待 completion events，提取分析内容）
4. 启动 Analyst + Writer + Checker（等待 completion events，提取内容）
5. 保存报告到本地和飞书

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

### 为什么不用纯 Python 脚本？

`tracker.py` 只做配置读取和环境准备。实际的搜索（kimi_search）、精读（读取 arXiv HTML）、报告上传（飞书 API）都需要 OpenClaw 工具，Python 脚本无法直接调用。

多 Agent 工作流的核心价值在于：
- 每个 Agent 有独立的上下文窗口，不会被其他任务的数据淹没
- 并行执行提高效率
- 质量检查有独立视角

### 为什么子 Agent 不直接写文件？

`sessions_spawn` 启动的子 Agent 运行在隔离环境中，无法直接访问主 Agent 的文件系统。因此采用 "子 Agent 输出到 announce → 主 Agent 提取并写入文件" 的模式。

每个 Agent 的任务描述中明确包含：
> "不要写入文件，直接在回复中输出内容。主 Agent 会接收并保存。"

### 为什么不要求子 Agent 输出固定格式？

**信息准确 > 格式统一**。搜索信息来源多样（arXiv、HuggingFace、GitHub、gist 等），格式不可能标准化。子 Agent 负责搜索和整理，主 Agent 负责解析和结构化。

- Searcher：返回搜索结果（任何格式），主 Agent 提取关键字段
- Deep Reader：返回 Markdown 分析报告（结构化），主 Agent 直接保存
- Analyst：返回 Markdown 分析（结构化），主 Agent 直接保存
- Writer：返回 Markdown 报告（结构化），主 Agent 直接保存
- Checker：返回检查结果（结构化），主 Agent 解析判断

### 错误处理

每个 Agent 执行任务时：
1. 如果搜索失败（如 kimi_search 返回空），记录错误并继续
2. 如果论文 HTML 下载失败，尝试 PDF 版本
3. 如果数据验证不通过，标注「待确认」而非填入估算值
4. 如果 Checker 发现 critical 问题，编排器会返工
5. 如果子 Agent 未在回复中输出内容，主 Agent 会检测并自行处理（如手动搜索/分析）

## 版本历史

- **v4.0.3** (2026-06-29): 修正设计理念：信息准确 > 格式统一。Searcher 不再要求 JSON 输出，主 Agent 负责解析各种格式的搜索结果。简化所有 Agent prompt，移除过度约束。
- **v4.0.2** (2026-06-29): 修复子 Agent 输出格式不稳定问题。增强 Searcher/Deep Reader/Writer/Analyst/Checker 的 prompt 约束，明确 JSON/Markdown 格式要求，增加自检清单。修复 P2 论文零分析问题。增加主 Agent 层容错处理说明。
- **v4.0.0** (2026-06-29): 重写为多Agent编排架构。新增：Searcher/Deep Reader/Analyst/Writer/Checker 5个专业Agent，独立质量检查关卡，报告模板标准化。
- **v3.1.0** (2026-06-28): 新增报告管理模块，动态配置初始化
- **v3.0.1** (2026-06-27): 数据验证机制，修正 cron 配置
- **v3.0.0** (2026-06-27): 完善联动体系
- **v2.0.0** (2026-06-27): 新增深度精读方法论
- **v1.0.0** (2026-06-27): 初始版本
