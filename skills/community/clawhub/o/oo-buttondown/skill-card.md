## Description:

Use this skill to read, create, update, and delete Buttondown data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Newsletter operators and developers use this skill to inspect Buttondown account data and manage subscribers and tags through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute unverified remote installers without separate approval.

Mitigation: Review the installer and approve CLI installation separately; prefer a verified, pinned release.

Risk: The connected Buttondown account can be changed through subscriber and tag write actions, and data can be deleted through destructive actions.

Mitigation: Review the exact action and payload, and retain the skill's required confirmation for changes and explicit approval for deletions.

Risk: The publisher documents automatic bundled-skill installation on first CLI launch, while the remote installer and runtime implementations were not verified.

Mitigation: Review first-launch installation effects and the CLI/runtime before use.

## Reference(s):

- [Buttondown API authentication documentation](https://docs.buttondown.com/api-authentication)
- [Buttondown](https://buttondown.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON]

**Output Format:** [CLI commands with JSON payloads and API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific schemas; write and destructive actions require confirmation as described by the skill.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
