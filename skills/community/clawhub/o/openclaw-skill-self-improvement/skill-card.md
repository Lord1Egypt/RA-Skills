## Description:

Health, eval, and regression system for continuously improving OpenClaw skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to audit OpenClaw skill registries, detect duplicate, dark, or stale skills, run routing evaluations, and track daily health changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly reads local OpenClaw skills and Agent transcript files while producing health signals.

Mitigation: Run it only against workspaces you are comfortable scanning locally, preferably with a test workspace or least-privileged account.

Risk: The daily heartbeat script contains unsafe shell command construction according to the authoritative security evidence.

Mitigation: Avoid the daily heartbeat in sensitive environments until command construction is fixed, or only use trusted and simple workspace paths after script review.

## Reference(s):

- [Routing evaluation cases](references/routing-evals.json)
- [Artifact README](README.md)
- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/openclaw-skill-self-improvement)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; scripts emit JSON and plain text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes skill health, routing evaluation, heartbeat summary, and history files under .learnings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
