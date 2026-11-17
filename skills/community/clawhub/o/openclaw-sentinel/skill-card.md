## Description:

OpenClaw Sentinel scans agent skills for supply-chain risks before and after installation, including obfuscation, suspicious install behavior, dependency-confusion patterns, metadata inconsistencies, and known-bad signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to inspect and monitor Agent Skills-compatible workspaces and decide whether skills should be installed, reviewed, quarantined, or rejected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and modify a local skills workspace, including disabling or moving other skills.

Mitigation: Run scan and inspect first, use a low-privilege account, keep backups of the skills directory, and reserve quarantine or protect for reviewed cases.

Risk: The security evidence reports an unvalidated reject path that can delete directories outside the intended workspace.

Mitigation: Avoid reject until path validation and confirmation safeguards are added; verify resolved workspace and skill paths before running destructive commands.

## Reference(s):

- [Openclaw Sentinel on ClawHub](https://clawhub.ai/atlaspa/skills/openclaw-sentinel)
- [AtlasPA publisher profile](https://clawhub.ai/user/atlaspa)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples, plus CLI text and JSON reports from the Sentinel script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3 and filesystem access to the skills workspace; quarantine, reject, and protect commands can rename, move, or remove skill directories.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
