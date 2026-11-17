## Description:

Evaluates AI Skill execution reliability across data pipeline integrity, code risk, business logic ambiguity, interpretation guardrails, and reportable complexity signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codermoray](https://clawhub.ai/user/codermoray)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit an AI Skill folder before deployment or sharing, checking whether agent execution is reproducible, trustworthy, and supported by clear rules and guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filesystem scanning may reach content the operator did not intend to include, especially when target folders contain symlinks or unexpected nested directories.

Mitigation: Run only against trusted or pre-checked directories, avoid targets with symlinks to sensitive files, and use a sandbox when auditing untrusted skills.

Risk: Report output can be written outside the target folder when an output directory is specified.

Mitigation: Confirm the target path and output directory before execution, and keep report output inside the intended workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codermoray/skills/halucatch)
- [HaluCatch Homepage](https://github.com/CoderMoray/HaluCatch)
- [Publisher Profile](https://clawhub.ai/user/codermoray)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown reports and terminal text generated from local Python execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes professional, standard, and AI action report files to a reports directory unless an output directory is specified.]

## Skill Version(s):

1.8.8 (source: frontmatter, manifest.json, __init__.py, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
