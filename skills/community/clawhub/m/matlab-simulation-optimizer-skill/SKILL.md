---
name: matlab-simulation-optimizer
description: Audit and optimize MATLAB simulation programs against a corresponding academic paper or specification. Use when Codex needs to compare local MATLAB simulation source code with a paper, verify the system model, algorithm fidelity, parameters, iteration and stopping conditions, metrics, and experiments, directly improve the source code for correctness and runtime while preserving paper-mandated algorithm logic and parameters, and generate a Chinese modification summary document.
---

# MATLAB Simulation Optimizer

Use this skill to turn a local MATLAB simulation into a more faithful and faster implementation of its reference paper. The agent must compare the paper and source code, edit the MATLAB source directly, preserve paper-mandated conditions, verify the changes, and write a summary document recording all modifications.

## Required Inputs

Ask only for missing inputs that block the work:

- Paper source: local PDF, DOCX, Markdown, LaTeX, URL, DOI, or pasted text.
- MATLAB program source: folder, repository, `.m` files, scripts, functions, data, and run command.
- Target results: paper figures/tables/metrics to reproduce or optimize, if any.
- Execution environment: whether MATLAB is available, whether Octave compatibility matters, CPU/GPU/Parallel Toolbox availability, runtime pain points, and allowed dependencies.

If the paper or MATLAB source folder is missing, ask for it before making conclusions or editing files.

## Output Location

Write the final summary document to the MATLAB simulation source root unless the user requests another location. Use `optimization_summary.md` by default. If the source root cannot be identified, ask the user for the target output folder before writing the summary.

## Non-Negotiable Rules

- Directly edit the source code when the user asks for optimization; do not stop at suggestions unless editing is impossible.
- Preserve paper-mandated algorithm logic, system model, channel model, objective functions, constraints, parameters, initialization rules, random process definitions, iteration formulas, stopping criteria, and evaluation metrics.
- Map every simulation result in the paper to one or more MATLAB main scripts, main functions, or runnable experiment entry points. If a paper figure/table/result cannot be mapped to code, record it as an uncovered result instead of assuming it is implemented.
- Remove useless comments, dead code, unused helper functions, unused parameters, obsolete plotting code, duplicate result drawing, stale saved-result logic, and other clutter when they are not needed to generate the simulation results in the paper. Treat content as useless only after confirming it is not used by any mapped paper result or required verification path.
- Separate correctness fixes from performance optimizations. Fix paper-code mismatches before optimizing speed.
- Do not change Monte Carlo count, SNR grid, antenna/user dimensions, convergence tolerance, maximum iterations, or random seed semantics merely to make the program faster unless the user explicitly approves a benchmark-only mode.
- Do not replace the paper algorithm with a different algorithm. Any accelerated variant must be mathematically equivalent or clearly isolated as an optional variant.
- Preserve user changes in a dirty worktree. Read the existing code and patch only the needed files.
- Use Chinese for the summary document unless the user asks otherwise.

## Workflow

1. **Build the paper contract**
   - Extract system model, variables, dimensions, distributions, parameters, assumptions, algorithm steps, update equations, iteration/stopping conditions, complexity claims, simulation settings, metrics, and target figures/tables.
   - Record every hard condition as `paper-explicit`, `caption/table`, `algorithm-box`, `derived`, or `inferred`.
   - For detailed checks, read `references/matlab-audit-checklist.md`.

2. **Map the MATLAB program**
   - Identify entry scripts, function call graph, config files, constants, data files, result directories, plotting scripts, and tests.
   - Identify all runnable main scripts/functions such as `main.m`, `main_*.m`, `run_*.m`, `demo_*.m`, `Fig*.m`, `plot_*.m`, and top-level functions with no required inputs.
   - Run the static scanner when useful:

```bash
python <skill-dir>/scripts/matlab_static_scan.py "<matlab-source-root>" --out "<matlab-source-root>/matlab_static_scan.json"
```

   - Inspect hotspots suggested by the scanner: nested loops, dynamic array growth, repeated inverses, `clear all`, unseeded randomness, hard-coded constants, duplicated simulation loops, repeated file I/O, and plotting inside computation loops.

3. **Compare paper vs. code**
   - Create a traceability table before editing:

```text
Paper item | Paper requirement | Code location | Code behavior | Severity | Planned action
```

   - Create a simulation-result mapping table:

```text
Paper result | Target metric/curve | MATLAB main entry | Called algorithm files | Output file/figure | Status
```

   - For each paper figure, table, numerical result, or named experiment, verify whether it is generated by one or several main scripts/functions. Mark status as `mapped`, `partially mapped`, `missing`, or `unclear`.
   - Pay special attention to:
     - system/channel/noise/interference model;
     - matrix dimensions and indexing;
     - normalization, units, dB/linear conversions, SNR/noise variance mapping;
     - algorithm update equations and initialization;
     - iteration count, tolerance, halting condition, support-size rule, step-size rule;
     - random seed and Monte Carlo averaging;
     - metric definitions, baselines, legends, and figure axes.

4. **Plan safe code edits**
   - For each edit, classify it as:
     - `Correctness`: required to match the paper;
     - `Performance`: mathematically equivalent speed/memory improvement;
     - `Cleanup`: removes comments, code, plotting, output, or helper artifacts that are not used for generating paper simulation results;
     - `Reproducibility`: seed, logging, result saving, deterministic output;
     - `Maintainability`: structure, comments, duplicate removal.
   - Prefer small patches that can be reviewed and verified.
   - Before deleting code or plotting logic, trace whether it is called by any mapped paper result, test, verification command, or shared helper. If uncertain, keep it or mark the uncertainty in the summary.

5. **Optimize MATLAB source**
   - Apply correctness patches first.
   - Remove confirmed-unused simulation branches, stale debug plots, old comparison figures, commented-out experiments, unused variables, duplicate helpers, and comments that no longer explain active paper-result generation.
   - Then optimize runtime while preserving numerical meaning. Prefer:
     - preallocation instead of dynamic array growth;
     - vectorization when it does not obscure or alter the algorithm;
     - replacing `inv(A)*b` with `A\b` and avoiding explicit matrix inverse where equivalent;
     - caching repeated dictionaries, steering matrices, FFT matrices, channel constants, or Monte Carlo-invariant terms;
     - moving plotting and file I/O outside inner loops;
     - using `parfor` only when parallel toolbox availability is known and random streams remain reproducible;
     - using sparse matrices or Cholesky/QR/SVD reuse when mathematically appropriate;
     - reducing redundant recomputation in iterations without changing stopping conditions.

6. **Verify**
   - Run the MATLAB scripts when MATLAB is available. If MATLAB is unavailable, do a static verification and provide exact commands for the user.
   - Compare pre/post outputs on a small deterministic case when possible.
   - Confirm that hard conditions from the paper remain unchanged.
   - If numerical values differ, decide whether the change is an intended correctness fix, harmless floating-point variation, or a regression.

7. **Write the summary document**
   - Save `optimization_summary.md` in the MATLAB source root.
   - Include source files changed, paper-code mismatch fixes, runtime optimizations, cleanup deletions, preserved paper conditions, paper-result-to-main-function mapping, uncovered paper results, verification commands/results, residual risks, and next steps.

## Summary Template

Use this structure for `optimization_summary.md`:

```markdown
# MATLAB 仿真程序优化总结

## 输入材料
- 论文:
- MATLAB 程序目录:
- 主要入口:

## 论文硬性条件核对
| 项目 | 论文要求 | 代码位置 | 处理结果 |
|---|---|---|---|

## 论文仿真结果与主函数对应关系
| 论文结果 | 指标/曲线 | MATLAB 主入口 | 调用的算法文件 | 输出文件/图 | 状态 |
|---|---|---|---|---|---|

## 修改清单
| 文件 | 类型 | 修改内容 | 原因 | 是否改变论文算法 |
|---|---|---|---|---|

## 正确性修复
- ...

## 运行速度优化
- ...

## 无用内容清理
| 文件 | 删除内容 | 判定为无用的依据 | 是否影响论文结果 |
|---|---|---|---|

## 验证结果
- 运行命令:
- 对比结果:
- 剩余差异:

## 保留不变的论文条件
- ...

## 后续建议
- ...
```

## MATLAB Optimization Guardrails

- Keep a `cfg` or parameter struct when the project already has one; do not scatter new constants.
- Preserve vector orientation intentionally. MATLAB row/column mismatches often silently change results.
- For random simulations, keep seed handling explicit and reproducible. In `parfor`, use controlled streams rather than accidental shared randomness.
- Do not use `single` precision unless the paper or user permits it.
- Treat plotting speed as secondary unless plotting dominates runtime.
- Benchmark with `tic/toc`, `timeit`, MATLAB profiler, or reduced-size deterministic runs before claiming speedups.

## Relationship to Other Skills

If the task is only to audit code without editing, `simulation-paper-auditor` may be enough. If the user asks to create MATLAB code from a paper from scratch, use `paper-matlab-reproduction`. Use this skill when the central request is to optimize an existing MATLAB simulation source program while preserving paper fidelity.

## Self-Evolution Mechanism

After each execution of this Skill:

1. Evaluate whether the output achieved the intended goal: **pass / fail**.
2. If it fails, reflect on the cause of failure and append a “failure case + improvement suggestion” to `diary/YYYY-MM-DD.md`.
3. If a certain improvement suggestion is repeatedly mentioned in the most recent three executions, refine it into a formal rule and submit a PR to modify this `SKILL.md`.
