## Description:

Use Paradym to inspect project data and manage credential issuance and verification workflows through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to read Paradym project, credential, issuance, and verification data, and to create credential offers or verification requests through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified downloads and change skills in multiple agent applications.

Mitigation: Review the CLI installation before automatic setup; consider setting OO_SKILLS_SYNC_DISABLED=1 to prevent startup synchronization.

Risk: A connected Paradym account can perform write actions that change issuance or verification state.

Mitigation: Use a narrowly scoped Paradym connection and confirm the exact payload and effect before each write.

## Reference(s):

- [Paradym](https://paradym.id)
- [Paradym API reference](https://paradym.id/reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell commands, with procedural guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve Paradym data; write actions create credential offers or verification requests and require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
