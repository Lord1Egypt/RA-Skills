# Complete References / 完整引用

## Core Packages / 核心包

| Package | Citation |
|---------|----------|
| **metafor** | Viechtbauer, W. (2010). Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*, 36(3), 1-48. |
| **meta** | Balduzzi, S., Rücker, G., & Schwarzer, G. (2019). How to perform a meta-analysis with R: a practical tutorial. *Evidence-Based Mental Health*, 22(4), 153-160. |
| **dmetar** | Harrer, M., Cuijpers, P., Furukawa, T. A., & Ebert, D. D. (2019). *Doing Meta-Analysis with R: A Hands-On Guide*. Chapman and Hall/CRC. |
| **netmeta** | Rücker, G., et al. (2016). netmeta: Network Meta-Analysis using Frequentist Methods. *BMC Medical Research Methodology*, 16, 1-13. |
| **multinma** | Welton NJ, et al. (2020). Multinma: Bayesian Network Meta-Analysis with Stan. |
| **gemtc** | van Valkenhoef G, et al. (2012). Automated generation of node-splitting models for assessment of inconsistency in network meta-analysis. *Research Synthesis Methods*, 3(4), 316-324. |
| **bayesmeta** | Röver C, et al. (2019). bayesmeta: Bayesian random-effects meta-analysis. |
| **robumeta** | Fisher Z, Tipton E. (2015). robumeta: An R-package for robust variance estimation in meta-analysis. *Methods in Ecology and Evolution*, 6, 115-123. |
| **clubSandwich** | Pustejovsky JE, Tipton E. (2018). Small-sample adjustments for tests of moderators and model fit using robust variance estimation. *Journal of Educational and Behavioral Statistics*, 43(6), 709-736. |
| **esc** | Lüdecke D. (2018). esc: Effect Size Computation for Meta Analysis. R package version 0.5. |
| **dosresmeta** | Crippa A, et al. (2018). dosresmeta: Performing dose-response meta-analyses. |
| **survmeta** | Zoglauer D, et al. (2010). survmeta: R package for survival meta-analysis. |
| **mada** | Doebler P, Holling H. (2015). mada: Meta-analysis of diagnostic accuracy. |
| **metagear** | Lajeunesse MJ. (2016). metagear: Comprehensive Synthesis of Backward-Forward Redundancy. *Methods in Ecology and Evolution*, 7:323-330. R package v0.7 (2021-02-15). |
| **pcmeta** | Proportional cumulative odds meta-analysis for ordered outcomes. |

## Methodological References / 方法学文献

- Cochrane Handbook for Systematic Reviews of Interventions (v6.3, 2022)
- PRISMA 2020: Page MJ, et al. *BMJ*, 372, n71.
- GRADE working group: gradepro.org

## Internal / 内部

- [SKILL.md](../SKILL.md) — Main skill file
- [revman_complete.md](./revman_complete.md) — RevMan→R code mapping
- [esc_robust_meta.md](./esc_robust_meta.md) — Effect size + RVE
- [advanced_analysis.md](./advanced_analysis.md) — Multilevel/IPD/Bayesian
- [interactive_menu.md](./interactive_menu.md) — Full menu tree
- [single_group_meta.md](./single_group_meta.md) — metaprop/metamean/metacor
- [bayesian_nma.md](./bayesian_nma.md) — gemtc (主) / multinma (可选)
- [survival_meta.md](./survival_meta.md) — metafor + KM reconstruction
- [tsa_diagnostics.md](./tsa_diagnostics.md) — TSA + Baujat + Drapery
- [diagnosis_meta.md](./diagnosis_meta.md) — mada::phm
- [review_workflow.md](./review_workflow.md) — PRISMA 流程图 (metagear::plot_PRISMA) + agent 行为层筛选 + 数据提取模板
- [upstream_orchestration.md](./upstream_orchestration.md) — 上游编排（检索→筛选→提取→分析）：复用 ct-literature + 数据提取助手与人工核验闸
- [systematic_review_fullflow.md](./systematic_review_fullflow.md) — 系统综述全流程模式（@skill 入口 playbook）：触发词 + Stage 0 启动确认 + 5 阶段命令链 + 两道人工闸 + 失败/边界处理
- [data_templates.md](./data_templates.md) — Data input templates
- [stata_to_r_mapping.md](./stata_to_r_mapping.md) — Stata equivalents
