## Description:

Operate HeyGen through an OOMOL-connected account to inspect data, generate videos, upload assets, and manage videos and assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

HeyGen account holders use this skill to inspect account data, generate videos, upload assets, and manage existing HeyGen videos and assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code that has not been verified.

Mitigation: Install a verified CLI release yourself and review setup before enabling the skill.

Risk: Automatic skill synchronization may introduce broader agent-skill changes without clear user approval.

Mitigation: Check or disable automatic skill synchronization before connecting the HeyGen account.

Risk: Video generation, uploads, and deletions can change account data.

Mitigation: Keep explicit approval requirements for generation, uploads, and deletions.

## Reference(s):

- [HeyGen skill release](https://clawhub.ai/oomol/skills/oo-heygen)
- [HeyGen](https://www.heygen.com)
- [HeyGen API documentation](https://developers.heygen.com/)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)
- [Connect HeyGen in OOMOL](https://console.oomol.com/connections/heygen)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads and responses with shell command examples and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the selected HeyGen operation; video generation runs asynchronously.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
