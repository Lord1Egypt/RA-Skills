## Description: <br>
Provides an agent-assisted code review workflow that evaluates security, performance, quality, and maintainability, then produces scored findings and improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penghang1223](https://clawhub.ai/user/penghang1223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to review pasted code, local files, PRs, or repository changes across security, performance, quality, and maintainability. It helps produce scored review reports, prioritized fixes, and approve/request-changes guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require access to private code, PRs, repositories, documents, or URLs to perform reviews. <br>
Mitigation: Grant only the specific files, PRs, repositories, documents, or URLs needed for the review. <br>
Risk: The package references a performance checklist that is not included. <br>
Mitigation: Verify performance review coverage manually until the missing checklist is supplied. <br>
Risk: Agent-generated review findings can be incorrect or incomplete. <br>
Mitigation: Have a human reviewer validate findings before using them for merge, release, or security decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/penghang1223/oc-code-review) <br>
- [Security checklist](artifact/templates/checklist-security.md) <br>
- [Quality checklist](artifact/templates/checklist-quality.md) <br>
- [Maintainability checklist](artifact/templates/checklist-maintainability.md) <br>
- [Finding template](artifact/templates/finding-template.md) <br>
- [Metrics analysis script](artifact/scripts/analyze-metrics.py) <br>
- [Complexity comparison script](artifact/scripts/compare-complexity.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review reports with scored tables, findings, code examples, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use packaged scripts for metrics and complexity comparison; the performance checklist referenced by the skill text is not included in the package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-04-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
