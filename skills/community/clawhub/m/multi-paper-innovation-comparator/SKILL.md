---
name: multi-paper-innovation-comparator
description: Compare innovations across multiple academic papers in a folder and produce a rolling summ document. Use when Codex needs to batch-read up to 20 paper files, summarize each paper's innovations and main work, compare each newly read paper against all previously read papers, reread related papers, and synthesize possible combined research directions or further innovation points.
---

# Multi-Paper Innovation Comparator

Use this skill to process a folder of papers incrementally and produce a `summ.md` document containing:

- every paper's core problem, main work, innovation points, methods, experiments, and workload;
- pairwise or cluster-level similarities and differences across papers;
- reread-based ideas for combining related work into further research directions.

## Hard Rules

- Process one paper at a time unless the user explicitly requests a larger batch.
- Refuse or pause if the folder contains more than 20 supported paper files.
- Treat `summ.md` as the running memory. Update it after every paper and after every reread synthesis.
- Place the generated `summ.md`, `paper_summ_state.json`, and `extracted_text/` in the same folder that contains the user's papers. If the user's paper folder cannot be identified or does not exist, ask the user to provide the paper folder before initializing the run.
- Do not mark a paper as processed until its per-paper summary has been added to `summ.md`.
- When two papers appear similar or combinable, reread the relevant extracted text for both before writing the combined research idea.
- Prefer Chinese output unless the user asks for another language.

Supported source files: `.pdf`, `.txt`, `.md`. For PDFs, use the bundled script to extract text.

## Workflow

1. Initialize a run:

```bash
python <skill-dir>/scripts/paper_summ.py init "<paper-folder>"
```

This validates the paper count, creates `paper_summ_state.json`, extracts text into `extracted_text/`, and creates `summ.md` in `<paper-folder>`.

If a separate output directory is explicitly required by the user, pass `--out "<output-dir>"`; otherwise do not use `--out`.

2. Get the next unread paper:

```bash
python <skill-dir>/scripts/paper_summ.py next "<paper-folder>"
```

Open the returned extracted text path. Read enough of the paper to capture title, problem, method, contributions, experiments, results, and limitations. If extraction is noisy, read the first pages plus sections containing terms such as `contribution`, `proposed`, `method`, `algorithm`, `experiment`, `simulation`, `result`, and `conclusion`.

3. Append the per-paper summary:

```bash
python <skill-dir>/scripts/paper_summ.py add-paper "<paper-folder>" --paper-id P001 --summary-file "<markdown-summary>"
```

The summary should include these headings:

```markdown
### PXXX - Paper Title

- 原文文件:
- 研究问题:
- 主要工作:
- 创新点:
- 方法/模型:
- 实验与结果:
- 工作量评估:
- 局限性:
- 可对比关键词:
```

4. Compare with all processed papers already in `summ.md`.

For the new paper, compare against all earlier summaries. Identify:

- shared problem settings, assumptions, channels, data models, sparsity structures, hardware constraints, or evaluation metrics;
- differences in method family, complexity, estimation/detection target, robustness, and experiment design;
- whether methods can be sequenced, merged, used as baselines, or extended to each other's scenarios.

5. Reread related pairs or clusters.

When overlap is meaningful, open the extracted text files for the new paper and each related prior paper. Then append a synthesis:

```bash
python <skill-dir>/scripts/paper_summ.py add-synthesis "<paper-folder>" --title "<short title>" --papers "P001,P003" --summary-file "<markdown-synthesis>"
```

Use this structure:

```markdown
### Synthesis: short title

- 涉及论文:
- 相似处:
- 关键差异:
- 可结合的工作点:
- 进一步研究的创新点:
- 需要补充验证:
```

6. Repeat `next`, `add-paper`, comparison, and reread synthesis until `next` reports no unread papers.

7. Finalize the document:

```bash
python <skill-dir>/scripts/paper_summ.py finalize "<paper-folder>"
```

Review `summ.md` once more and ensure it contains the final sections for all papers, all cross-paper syntheses, and a concise final research-opportunity ranking.

## Output Guidance

Write `summ.md` as a research notebook, not a generic literature review. Be specific about what each paper actually did, what is new, how much implementation or experimental work it contains, and how its ideas could combine with other papers.

For further research ideas, prefer concrete formulations:

- "把 A 的非平稳信道分区思想用于 B 的低复杂度检测框架";
- "用 C 的稀疏恢复鲁棒性处理 D 中量化观测误差";
- "把 E 的层次化估计策略扩展到 F 的近场/XL-MIMO 场景，并比较复杂度与导频开销".

Avoid vague ideas such as "combine deep learning with the method" unless the source papers justify that direction.

## Self-Evolution Mechanism

After each execution of this Skill:

1. Evaluate whether the output achieved the intended goal: **pass / fail**.
2. If it fails, reflect on the cause of failure and append a “failure case + improvement suggestion” to `diary/YYYY-MM-DD.md`.
3. If a certain improvement suggestion is repeatedly mentioned in the most recent three executions, refine it into a formal rule and submit a PR to modify this `SKILL.md`.
