## Description:

Operate Magic Hour to create, manage, and retrieve image, video, and audio projects through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to read Magic Hour account and project details, submit media creation or editing tasks, upload assets, and manage saved projects through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may execute unverified remote software without separate user approval.

Mitigation: Review and approve CLI installation separately, use a verified release, and check whether it installs additional agent skills.

Risk: The connected account can be used for media generation, uploads, and deletion, which can change or remove user data.

Mitigation: Retain the required user confirmations for generation, uploads, and deletion.

## Reference(s):

- [Magic Hour](https://magichour.ai)
- [Magic Hour API documentation](https://docs.magichour.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-magichour)

## Skill Output:

**Output Type(s):** [Text, API Calls, Image, Video, Audio]

**Output Format:** [JSON connector requests and responses with downloadable media results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media generation tasks are asynchronous; results may include download links.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
