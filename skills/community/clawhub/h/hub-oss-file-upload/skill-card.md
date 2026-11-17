## Description:

Uploads a requested workspace file and provides a temporary external download link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianglei0321](https://clawhub.ai/user/jianglei0321)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent can request a download link for a file already in the workspace, including one the agent has just created. The skill uploads that file and returns a link they can open or share.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An uploaded file can be accessed through its temporary external link by people outside the workspace.

Mitigation: Upload only files the user intends to share; avoid files containing secrets or private data unless external sharing is intended.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jianglei0321/skills/hub-oss-file-upload)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Short Simplified Chinese text with a download URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Link typically remains valid for about 7 days; files must not exceed 20 MB.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
