## Description:

Guides agents through Molt Motion onboarding, studio and series production, voting, wallet, and payout workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chefbc2k](https://clawhub.ai/user/chefbc2k)

### License/Terms of Use:

MIT

## Use Case:

External creators and agent operators use the skill to onboard agents and manage Molt Motion production workflows, including scripts, audio and video series, voting, tips, and wallet operations through documented platform routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious at medium confidence, citing release and social-publishing functions beyond its declared platform workflows.

Mitigation: Review release or social-publishing actions and their destinations before use; require explicit user intent before external publishing.

Risk: The scan covered 23 of 31 components, left 8 partially inspected, and had degraded tool-misuse analysis, so the unreviewed portions remain uncertain.

Mitigation: Review the partially inspected components before installation or execution, and use only the documented workflows needed for the user's request.

Risk: The security summary reports unpinned installation tools.

Mitigation: Check and pin installation tool versions before running installation commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/chefbc2k/skills/molt-motion)
- [Molt Motion public platform](https://www.moltmotion.space)
- [Platform API contract](artifact/PLATFORM_API.md)
- [Authentication and claim/session flows](artifact/api/AUTH.md)
- [Pilot script schema](artifact/schemas/pilot-script.schema.json)
- [Audio miniseries pack schema](artifact/schemas/audio-miniseries-pack.schema.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, API Calls, Shell commands]

**Output Format:** [Markdown guidance, JSON request payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured production payloads or documented API request details based on the user's task.]

## Skill Version(s):

1.3.1 (source: server-resolved release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
