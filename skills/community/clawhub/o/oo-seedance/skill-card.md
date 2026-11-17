## Description:

Manage Seedance video-generation tasks through an OOMOL-connected account, including submission, retrieval, listing, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can submit Seedance video-generation tasks, inspect their status and results, list visible tasks, or cancel and delete tasks through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions may execute downloaded installer code and the CLI may install or synchronize additional agent skills; complete installer and hosted connector behavior was unavailable for inspection.

Mitigation: Review and approve CLI installation separately, including any additional skills it may install or synchronize.

Risk: Seedance requests use the connected account through OOMOL, so account access and submitted data are relevant to the user's trust decision.

Mitigation: Review the data and account access granted to OOMOL and connect only the intended Seedance account.

## Reference(s):

- [Seedance on ClawHub](https://clawhub.ai/oomol/skills/oo-seedance)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Seedance product page](https://www.volcengine.com/product/ark)
- [Seedance API documentation](https://www.volcengine.com/docs/82379/1520757)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Video files or links]

**Output Format:** [JSON action responses, task status and result details, and generated video links or files; shell commands are used to invoke actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation is asynchronous; result availability depends on task status and the connected Seedance account.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
