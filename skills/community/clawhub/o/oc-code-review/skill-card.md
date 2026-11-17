## Description:

OC Code Review helps agents review code, PRs, diffs, repositories, or files across security, performance, quality, and maintainability and produce scored improvement reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penghang1223](https://clawhub.ai/user/penghang1223)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to request quick, deep, or security-focused code reviews and receive prioritized findings, scores, and recommended next actions. It is especially suited to reviewing pasted code, local files, PRs, diffs, and repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewing PRs, repositories, files, or pasted code can expose proprietary code, secrets, or metadata to the agent context.

Mitigation: Invoke the skill only for code the user intends to analyze, and avoid including secrets, credentials, or unnecessary sensitive data.

Risk: The skill can suggest local commands or metrics scripts for deeper analysis.

Mitigation: Run helper scripts only against intended local files and review any generated commands before execution.

Risk: The artifact references a performance checklist file that is not included, which can make performance review less consistent.

Mitigation: Use the performance criteria listed in SKILL.md or add the missing checklist before relying on standardized performance scoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/penghang1223/skills/oc-code-review)
- [Security checklist](artifact/templates/checklist-security.md)
- [Quality checklist](artifact/templates/checklist-quality.md)
- [Maintainability checklist](artifact/templates/checklist-maintainability.md)
- [Finding template](artifact/templates/finding-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review reports with scoring tables, findings, recommendations, and optional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mostly Chinese-language output; supports quick review, deep review, and security audit modes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
