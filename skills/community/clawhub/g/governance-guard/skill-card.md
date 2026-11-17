## Description:

Governance Guard provides a PROPOSE, DECIDE, PROMOTE pipeline for structural authority separation before autonomous agent actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devongenerally-png](https://clawhub.ai/user/devongenerally-png)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to evaluate proposed read, write, execute, network, create, and delete actions against policy before execution. It is intended to add deterministic governance decisions and a witness log around autonomous agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The standalone promote command can be used outside the full governance pipeline, which may weaken approval guarantees.

Mitigation: Use the full pipeline command for governed actions and avoid relying on standalone promotion until verdicts are authenticated or kept internal.

Risk: The persistent witness log may contain sensitive prompts, paths, tool parameters, or action details in plaintext.

Mitigation: Restrict filesystem permissions on ~/.openclaw/governance and avoid passing secrets through governed action parameters.

Risk: The security verdict is suspicious despite no visible malicious behavior.

Mitigation: Review the skill before installing and confirm that its governance behavior matches the intended deployment policy.

## Reference(s):

- [Policy File Schema](references/policy-schema.md)
- [OpenClaw](https://openclaw.dev)
- [ClawHub Skill Page](https://clawhub.ai/devongenerally-png/skills/governance-guard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands, YAML policy configuration, and JSON verdict output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npx; installs tsx for TypeScript command execution.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
