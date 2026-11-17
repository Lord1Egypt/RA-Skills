## Description:

SmugMug (smugmug.com). Use this skill for ANY SmugMug request — searching and reading data. Whenever a task involves SmugMug, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search SmugMug content and retrieve user, album, folder, image, and image metadata through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified downloaded code and make broader, persistent agent changes without clear user control.

Mitigation: Review and approve CLI installation separately, use a verified release, and consider disabling automatic skill synchronization before first use.

Risk: Connecting SmugMug authorizes OOMOL to mediate account requests.

Mitigation: Connect only the intended SmugMug account after reviewing the setup and account connection.

## Reference(s):

- [SmugMug API documentation](https://api.smugmug.com/api/v2/doc/index.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [SmugMug](https://www.smugmug.com)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON responses with text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected SmugMug account and the selected read action.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
