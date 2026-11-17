## Description:

Local-only semantic context filtering that saves up to 90% in token costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fajarhide](https://clawhub.ai/user/fajarhide)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this OpenClaw skill to run local terminal commands through the OMNI CLI, receive distilled command output, and retrieve archived full logs when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad shell-like local command authority.

Mitigation: Install only in a trusted, sandboxed workspace and rely on the OpenClaw host for approvals and command restrictions before routing destructive or sensitive operations through it.

Risk: Command output may be archived locally and could include secrets or production credentials.

Mitigation: Avoid sending secrets, production credentials, or sensitive operational output through the tool; review local archives according to the workspace's data-handling requirements.

Risk: The skill depends on a local OMNI binary outside the artifact.

Mitigation: Use an audited OMNI binary from a trusted installation path before enabling the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fajarhide/skills/omni-signal-engine)
- [OMNI GitHub Repository](https://github.com/fajarhide/omni)
- [OMNI Security Policy](https://github.com/fajarhide/omni/blob/main/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Text command results with optional stderr and exit-code metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distilled command output may omit details; archived full output can be retrieved by hash when available.]

## Skill Version(s):

0.5.9 (source: server release metadata and openclaw.plugin.json; SKILL.md frontmatter lists 0.5.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
