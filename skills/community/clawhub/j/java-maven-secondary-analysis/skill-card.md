## Description:

Analyze a Java Maven project delivered as a ZIP archive or a GitLab repository URL for secondary-development scope, class counts, module distribution, product customization traces, invasive modifications, and upgrade pollution risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrliugangqiang](https://clawhub.ai/user/mrliugangqiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to produce a Chinese-language first-pass secondary-development analysis report for Java Maven projects. It helps summarize project structure, class and layer distribution, customization traces, invasive-change candidates, and upgrade-risk indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report's invasive-change and upgrade-risk sections are heuristic triage and may miss issues or overstate keyword matches.

Mitigation: Review findings against project context before using them for architecture, upgrade, or security decisions.

Risk: The analyzer reads files in the project directory provided to it.

Mitigation: Run it only against Java Maven project directories or archives that the operator intends to analyze.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrliugangqiang/skills/java-maven-secondary-analysis)
- [Skill definition](artifact/SKILL.md)
- [Report template](artifact/templates/report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with supporting JSON scan output and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written under business/ and should include supporting file-path evidence for important findings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
