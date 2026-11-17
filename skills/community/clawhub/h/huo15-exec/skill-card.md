## Description:

Guides agents to run focused commands, tests, builds, and reproduction steps to verify code changes while treating destructive operations cautiously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill after code changes or bug fixes to choose the smallest meaningful validation command, run tests, builds, lint, or type checks, interpret failures, and report results honestly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation workflows may include destructive shell, git, database, production, or global dependency commands.

Mitigation: Require explicit review and confirmation before allowing those commands, and prefer reversible or backed-up actions.

Risk: A clean scan does not prove that every proposed validation command is appropriate for the current repository.

Mitigation: Run focused checks first, read failures before retrying, and report skipped or failed verification honestly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-exec)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only; no required external binaries are declared.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
