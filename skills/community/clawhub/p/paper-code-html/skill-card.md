## Description: <br>
Paper Code HTML guides agents to analyze a research paper and its corresponding codebase, then generate an academic-style HTML report covering methodology, experiments, implementation details, and paper-code consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leogoat2004](https://clawhub.ai/user/leogoat2004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to turn a paper plus its implementation into a structured HTML explainer. It helps compare theory, experiments, core code, and paper-code alignment for review or documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow reads user-supplied paper and code paths and writes an HTML report. <br>
Mitigation: Provide only the specific files or directories needed for the report, and avoid broad or confidential paths unless the full workflow is trusted. <br>
Risk: The generated report can include sensitive code details, paper excerpts, or project-specific analysis. <br>
Mitigation: Review the HTML before sharing it and use only papers and codebases you are authorized to analyze. <br>
Risk: Paper and code interpretation may be incomplete or inaccurate. <br>
Mitigation: Verify technical claims, experiment summaries, and code-paper consistency findings against the original paper and source code before relying on the report. <br>
Risk: The skill expects a referenced frontend-design workflow for higher-quality HTML output. <br>
Mitigation: Proceed with a simplified HTML fallback only when acceptable, and inspect the final report for layout and content quality. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leogoat2004/paper-code-html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [HTML report file with structured analytical prose and generated HTML/CSS/JavaScript as needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided paper path, code path, and HTML output path; validates paths before writing and may use a frontend-design skill when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
