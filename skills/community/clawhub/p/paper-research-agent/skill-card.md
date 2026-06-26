## Description: <br>
Autonomous multi-agent paper research system that orchestrates literature search, arXiv PDF download, parallel full-paper analysis, and integrated survey generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changer-changer](https://clawhub.ai/user/changer-changer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical teams use this skill to search for academic papers, analyze full PDFs, compare methods, and generate literature survey materials with cited tables and research-gap findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may change the Python environment by installing dependencies during execution. <br>
Mitigation: Run it in an isolated environment and preinstall or pin required dependencies before use. <br>
Risk: The workflow can download papers and write local research folders. <br>
Mitigation: Choose an explicit output directory and review downloaded files and generated reports before relying on them. <br>
Risk: The workflow may launch many parallel analysis agents without strong user-controlled limits. <br>
Mitigation: Set a small paper count or concurrency limit and review generated agent tasks before execution. <br>


## Reference(s): <br>
- [Paper Research Agent ClawHub release](https://clawhub.ai/changer-changer/paper-research-agent) <br>
- [Paper Analysis Report Standards](references/analysis_standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON summaries, local research files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates per-paper analysis reports, downloaded PDFs, agent task files, a research summary JSON file, and an integrated survey package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
