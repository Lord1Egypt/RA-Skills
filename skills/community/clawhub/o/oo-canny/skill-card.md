## Description:

Canny (canny.io). Use this skill for ANY Canny request — reading, creating, and updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Product, support, and engineering teams use this skill to read and manage Canny boards, posts, comments, and users through their connected account. Confirm the connected account and each proposed write before changing Canny data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may make persistent changes to other agent skill directories.

Mitigation: Review the CLI installation separately, use a verified release, and set OO_SKILLS_SYNC_DISABLED=1 before CLI use to disable startup skill synchronization.

Risk: Canny writes affect the connected account, and the remote installers and hosted connector implementation remain unverified.

Mitigation: Confirm the connected account and each proposed write; review CLI installation before setup and use a verified release.

## Reference(s):

- [Canny](https://canny.io)
- [Canny API documentation](https://developers.canny.io/api-reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON requests and responses, with shell command examples and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve Canny data; write actions change Canny data and require user confirmation.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
