## Description: <br>
PRISM-Gen Demo helps agents retrieve, filter, sort, merge, score, plot, and summarize bundled PRISM-Gen molecular-screening CSV results locally. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[SenaZeng](https://clawhub.ai/user/SenaZeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to inspect bundled PRISM-Gen molecular screening results, compare candidate molecules across pipeline stages, and generate local summaries or plots without network services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated rankings, scores, and plots summarize bundled demonstration CSV data and may be mistaken for validated laboratory or clinical conclusions. <br>
Mitigation: Treat results as exploratory analysis of pre-calculated data and review candidate claims with qualified domain experts before downstream use. <br>
Risk: Plot commands write to user-specified output paths. <br>
Mitigation: Use a dedicated output folder and safe filenames for generated plots. <br>


## Reference(s): <br>
- [ClawHub PRISM-GEN-DEMO release page](https://clawhub.ai/SenaZeng/prism-gen-demo) <br>
- [PRISM-Gen Zenodo record](https://doi.org/10.5281/zenodo.18764996) <br>
- [Related PRISM-Gen repository](https://github.com/SenaZeng/PRISM-Gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and local text, table, summary, or image-file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on bundled CSV files; plotting writes user-named image files and requires optional matplotlib.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
