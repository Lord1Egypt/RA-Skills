## Description:

Read, start, and update OpenHands Cloud conversations through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can list or read OpenHands Cloud conversations, start repository tasks, and send follow-up messages through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup includes downloaded CLI installers that may execute without separate approval or integrity checks.

Mitigation: Review and approve CLI setup separately, and prefer a pinned, verified release.

Risk: The integration operates through an OOMOL-connected account, and publisher guidance includes installing additional agent skills.

Mitigation: Review the additional-skill installation guidance and connected-account access; confirm the exact payload before OpenHands changes.

## Reference(s):

- [OpenHands Cloud API documentation](https://docs.openhands.dev/openhands/usage/cloud/cloud-api)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [OpenHands](https://www.all-hands.dev)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads and responses, with shell command examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads should follow the live connector schema; state-changing actions require confirmation of the exact payload.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
