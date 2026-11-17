## Description:

Preflight Checks helps agent builders verify that an AI agent applies documented memory and behavioral rules consistently across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanmmm](https://clawhub.ai/user/ivanmmm)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to create scenario-based behavioral checks, expected-answer files, and workspace setup steps that test whether agents follow persistent-memory rules after restarts, updates, or manual diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example content and guidance may encourage persistent memory writes without explicit user control.

Mitigation: Review and customize the checks before installation, remove any unwanted 'no confirmation' rules, and require approval for persistent memory writes.

Risk: Example files include Prometheus/Ivan-specific behavioral expectations that may not match another workspace.

Mitigation: Replace or remove the Prometheus/Ivan example files and hard-coded identifiers before using the skill in a different environment.

Risk: Communication examples may encourage sending files or messages outside the local workspace.

Mitigation: Require user approval before sending files or messages outside the local workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivanmmm/skills/preflight-checks)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [CHECKS template](templates/CHECKS-template.md)
- [ANSWERS template](templates/ANSWERS-template.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown templates and guidance with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces checklists, expected-answer rubrics, setup guidance, and workspace files for behavioral verification.]

## Skill Version(s):

1.0.0 (source: CHANGELOG.md, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
