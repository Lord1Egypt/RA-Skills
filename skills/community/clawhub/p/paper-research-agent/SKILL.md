---
name: paper-research-agent
description: |
  Autonomous multi-agent paper research system. When user wants to research a topic, find related papers, 
  or analyze academic literature, use this skill to orchestrate the full pipeline: intelligent search → 
  PDF download → parallel agent analysis → comprehensive report generation.
  
  Triggers on: "research papers on X", "find related literature", "analyze papers", 
  "调研论文", "查找相关文献", "分析论文", "帮我调研XXX领域"
---

# Paper Research Agent - Autonomous Multi-Agent Research System

## When to Use

Use this skill when the user wants to:
- Research papers on a specific topic
- Find related literature for a research area
- Analyze academic papers in depth
- Build a literature survey
- Identify research gaps
- Compare methods across papers

## Core Workflow

The system autonomously executes the full research pipeline:

```
User Query → Research Probe → PDF Download → Parallel Agent Analysis → Integrated Report
```

### Phase 1: Research Probe (Automated)
- Parse user's research intent from natural language
- Execute vertical deep search or iterative exploration
- Generate research graph with papers at different levels

### Phase 2: PDF Download (Automated)
- Download PDFs from arxiv
- Deduplicate and version management
- Standard naming: {paper_title}-{arxiv_id}.pdf

### Phase 3: Parallel Agent Analysis (Automated - Key)
- Spawn multiple sub-agents (one per paper)
- Each agent reads full PDF using paper-reader
- Generate 6-section detailed analysis
- Agents run in parallel for speed

### Phase 4: Report Integration (Automated)
- Collect all agent analyses
- Generate comparison tables
- Identify research gaps
- Output comprehensive survey

## Agent Analysis Requirements

Each sub-agent MUST generate a 6-section report following the detailed standards in:
**`references/analysis_standards.md`**

SubAgent MUST read this reference file before starting analysis to understand:
- Detailed requirements for each of the 6 sections
- Possible sub-sections to consider (as hints, not rigid requirements)
- Quality checklists
- How to use paper-reader tool
- Report format template

### Summary of 6 Required Sections

### Section 1: Research Background
- Domain context and research lineage
- Key prior works cited (3-5 papers)
- Technical state when this paper was published
- **Goal**: Help user understand the research landscape

### Section 2: Research Problem
- Specific problem being solved
- Limitations of existing methods (cite original text)
- Core assumptions and insights
- **Goal**: Clarify what problem the author identified

### Section 3: Core Innovation
- Detailed method/system architecture
- Technical details (network structure, dimensions)
- Key formulas in LaTeX format
- Comparison table with prior methods
- **Goal**: Understand exactly what the author did

### Section 4: Experimental Design
- Dataset details (name, scale, characteristics)
- Baseline methods used
- Evaluation metrics
- REAL experimental data tables (copy from paper)
- Ablation study results
- **Goal**: Extract real data for comparison

### Section 5: Key Insights
- Core findings from experiments
- Domain insights (what works/doesn't work)
- Practical recommendations
- **Goal**: Learn actionable lessons

### Section 6: Future Work
- Limitations acknowledged by authors
- Unsolved problems
- Potential research directions (at least 3)
- **Goal**: Identify research gaps for user's innovation

**For full details, sub-section hints, and quality standards - READ `references/analysis_standards.md`**

## Quality Enforcement

Agents MUST:
- ✅ Read EVERY section of the PDF (not just abstract)
- ✅ Extract REAL tables with actual data
- ✅ Cite sources with exact locations [Section X.Y]
- ✅ Use paper-reader tool for extraction
- ❌ NEVER fabricate data
- ❌ NEVER skip sections

## Usage

### Agent Execution (When User Requests Research)

**Trigger phrases**: 
- "帮我调研一下XXX的相关论文"
- "Research papers on X"
- "Find related literature about X"
- "分析XXX领域的论文"

**Agent Action**:

Step 1: Execute main pipeline
```python
import subprocess
result = subprocess.run([
    "python3", 
    "~/.openclaw/workspace/skills/paper-research-agent/scripts/research_pipeline.py",
    "--query", "{user_topic}",
    "--mode", "vertical",
    "--max-papers", "10",
    "--output", "./research_{topic}"
], capture_output=True, text=True)

print(result.stdout)
```

Step 2: Read generated agent tasks
```python
import json
with open("./research_{topic}/_agent_tasks.json") as f:
    tasks = json.load(f)
```

Step 3: Spawn parallel sub-agents for analysis (CRITICAL)
```python
# Spawn multiple agents in parallel for each paper
for task_info in tasks:
    sessions_spawn(
        agentId="main",
        mode="run", 
        runtime="subagent",
        task=task_info['task'],
        timeoutSeconds=600  # 10 minutes per paper
    )
```

**Important**: Launch as many agents in parallel as possible for speed.

Step 4: After all agents complete, integrate results
```python
# Collect all analysis reports
# Generate integrated survey
# Present to user
```

## Output Structure

```
research_output/
├── _research_summary.json              # Research metadata
├── probe/
│   ├── _probe_results.json            # Search results
│   └── _probe_report.md               # Human-readable probe report
├── papers/
│   ├── {title}-{arxiv_id}.pdf         # Downloaded PDFs
│   └── ...
├── analysis/
│   ├── {title}-{arxiv_id}_analysis.md # 6-section agent reports
│   └── ...
└── _integrated_survey.md              # Final integrated survey
```

## Key Scripts

- `scripts/research_pipeline.py`: Main orchestration script
- `scripts/research_probe.py`: Intelligent search module
- `scripts/paper_downloader.py`: PDF download module
- `scripts/agent_task_generator.py`: Sub-agent task generator

## Report Format Standards

Each sub-agent analysis report MUST follow this exact 6-section structure:

```markdown
# 📄 {Paper Title}

> **ArXiv ID**: {id}  
> **Authors**: {authors}  
> **Published**: {date}

---

## Section 1: Research Background
- Domain context
- Key prior works (3-5 papers with citations)
- Technical state at publication time
- Citations: [Section X.Y]

## Section 2: Research Problem
- SPECIFIC problem being solved
- SPECIFIC limitations of existing methods (quote original)
- Core assumptions
- Citations: [Section X.Y, "exact quote"]

## Section 3: Core Innovation
- Method/system architecture (detailed)
- Technical details (network structure, dimensions)
- Key formulas in LaTeX: $...$
- Comparison table:
  | Aspect | Prior Work | This Paper | Advantage |
  |--------|-----------|------------|-----------|
- What is genuinely new

## Section 4: Experimental Design
- Dataset: Name, size, characteristics
- Baseline methods: Specific names
- Metrics: Formulas, units
- Results table (REAL data):
  | Method | Metric1 | Metric2 |
  |--------|---------|---------|
  | This | X.XX | X.XX |
  | Baseline | X.XX | X.XX |
- Ablation study results

## Section 5: Key Insights
- Core findings from experiments
- What works/doesn't work
- Design choices and impact
- Practical recommendations

## Section 6: Future Work
- Limitations acknowledged by authors
- Unsolved problems
- Future directions (3+)

---

*Analysis by Paper Research Agent*  
*Date: {timestamp}*
```

**Quality Requirements**:
- Minimum 3000 words
- At least 3 data tables
- At least 10 citations to original text
- All citations must include exact location [Section X.Y] or [Table N]
- No fabricated data - all numbers must come from the actual paper

## Error Handling

If paper download fails:
- Skip and continue with available papers
- Log error in summary

If agent analysis fails:
- Retry once
- If still failing, mark as "analysis_failed" in summary
- Continue with other papers

## Best Practices

1. **For deep research**: Use `--mode vertical` (searches 4 levels deep)
2. **For exploration**: Use `--mode iterative` (progressive discovery)
3. **For specific paper**: Use `--mode horizontal` (find related work)
4. **Parallel agents**: System auto-spawns optimal number based on paper count
5. **Quality check**: Always verify a few random citations manually

## Example Session

**User**: "帮我调研扩散策略在机器人操作中的应用"

**Agent**:
1. Executes research probe with query "扩散策略 机器人操作"
2. Finds 30 related papers across 4 levels
3. Downloads PDFs for top 10 papers
4. Spawns 10 sub-agents in parallel
5. Each agent analyzes one paper with 6-section format
6. Collects all analyses
7. Generates integrated survey with comparison tables
8. Presents final report to user

**Output**: Complete research package with all papers analyzed and integrated survey.

## Dependencies

Required Python packages (auto-installed):
- arxiv
- requests
- pdfplumber (for paper-reader)

## Notes

- Each paper analysis takes 5-10 minutes
- Parallel execution significantly speeds up research
- Always verify critical data points manually
- The system respects arxiv rate limits (3s delay between downloads)
