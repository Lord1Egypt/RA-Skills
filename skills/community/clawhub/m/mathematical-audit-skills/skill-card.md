## Description:

Performs mathematical quality audits of Python code and OpenClaw skills using information theory, graph theory, complexity metrics, statistical analysis, and pattern detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[znsyhandao](https://clawhub.ai/user/znsyhandao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to inspect Python code or skill packages for mathematical complexity, structure, entropy, and maintainability signals. It produces scores, metrics, and recommendations that can support quality review before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can overwrite a user-specified report path, despite documentation that describes the skill as read-only.

Mitigation: Prefer stdout output, avoid `--output` on existing or sensitive paths, and run the skill in a disposable or backed-up workspace.

Risk: The security verdict is suspicious because the documented read-only posture does not fully match the CLI behavior.

Mitigation: Review the package before installation and treat generated reports as untrusted analysis output until validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/znsyhandao/skills/mathematical-audit-skills)
- [Publisher profile](https://clawhub.ai/user/znsyhandao)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Release notes](artifact/RELEASE_NOTES.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text or JSON report with quality scores, metric summaries, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write a report when an output path is supplied.]

## Skill Version(s):

3.6.1 (source: server release metadata, changelog, SKILL.md, skill.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
