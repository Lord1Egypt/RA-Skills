## Description:

Audits installed skills to report system-resource access, including network use, subprocess execution, file I/O, environment variables, and unsafe operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers, security reviewers, and workspace administrators use this skill to audit Agent Skills-compatible workspaces, review permission categories, and generate status or matrix reports before trusting installed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes high-impact commands that can quarantine or permanently remove installed skills.

Mitigation: Run audit, report, or status modes first, and use quarantine or revoke only after reviewing the target path and confirming the intended skill.

Risk: The server scan reports a revoke path-handling flaw that can reach outside the intended skills directory.

Mitigation: Do not trust revoke in a real workspace until path validation and explicit confirmation safeguards are reviewed or added.

Risk: Security verdict is suspicious even though no network exfiltration, remote code loading, credential theft, or hidden persistence was found.

Mitigation: Review the skill locally before installation and restrict execution to test workspaces until the high-impact behaviors are accepted.

## Reference(s):

- [Openclaw Arbiter on ClawHub](https://clawhub.ai/atlaspa/skills/openclaw-arbiter)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown tables with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3 and no external dependencies.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
