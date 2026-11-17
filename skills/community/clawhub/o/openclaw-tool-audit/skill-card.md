## Description:

Audit OpenClaw agent tool exposure versus observed use, including broad or unused tool allowances and whether agent tool configs are tighter than necessary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review OpenClaw agent tool permissions against observed tool usage, identify broad or unused allowances, and produce markdown or JSON exposure reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a local audit binary or source checkout that may inspect local OpenClaw configuration and session data.

Mitigation: Use only a trusted local installation or inspected source checkout, and avoid elevated execution unless required.

Risk: Audit reports may include sensitive details from local configuration or session files.

Mitigation: Confirm the local files are appropriate to inspect before running the audit and review generated Markdown or JSON before sharing.

## Reference(s):

- [OpenClaw Tool Audit skill page](https://clawhub.ai/pfrederiksen/skills/openclaw-tool-audit)
- [OpenClaw Tool Audit repository](https://github.com/pfrederiksen/openclaw-tool-audit)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands; invoked CLI can produce Markdown or JSON audit reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local openclaw-tool-audit installation and access to local OpenClaw configuration and session data.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
