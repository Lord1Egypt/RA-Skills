## Description:

Verifies workspace file integrity and scans agent identity, memory, configuration, and installed skill files for prompt-injection indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to create local integrity baselines, verify workspace files, and scan agent-readable files for prompt-injection patterns before trusting a workspace session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Baseline and accept operations can make compromised or unintended file states look trusted if they are run before review.

Mitigation: Create or update baselines only after reviewing the workspace and confirming it is in a known-clean state.

Risk: Protect, restore, rollback, and quarantine operations can overwrite important workspace files or disable installed skills.

Mitigation: Review target paths first, keep backups, and use these commands only when the intended file or skill changes are clear.

Risk: Clean scan results can be incomplete because some security-skill names are exempted by directory name.

Mitigation: Treat clean results as one signal, and manually review high-impact agent identity, memory, and skill files before trusting a workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atlaspa/skills/openclaw-warden)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and local scan findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3 and writes .integrity baseline data in the target workspace.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
