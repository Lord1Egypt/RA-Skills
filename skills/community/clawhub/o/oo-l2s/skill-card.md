## Description:

L2S (l2s.is). Use this skill for ANY L2S request — reading, creating, and updating data. Whenever a task involves L2S, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other L2S users use this skill to retrieve details for shortened URLs and to create or update them through their connected L2S account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the oo CLI executes downloaded code, and the live installers were unavailable for inspection.

Mitigation: Review and approve installation separately; prefer a pinned release with verified integrity.

Risk: L2S data passes through OOMOL, and CLI startup may synchronize skills.

Mitigation: Review the applicable data handling and skill synchronization behavior; set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill writes when appropriate.

## Reference(s):

- [L2S homepage](https://www.l2s.is)
- [L2S API documentation](https://docs.l2s.is/api-8021271)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [L2S action results and JSON payloads, with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read URL details or create and update shortened URL records.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
