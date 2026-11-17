## Description:

Publish content to Nosi and get a shareable URL. Use when the user wants to publish text, markdown, or files to nosi.pub for sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billhao](https://clawhub.ai/user/billhao)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they want an agent to publish text, markdown, or file contents to Nosi and return a permanent shareable URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Content sent to Nosi may become public and permanent.

Mitigation: Confirm the user intends public sharing before publishing, and do not publish secrets, credentials, private personal information, regulated data, or proprietary material unless it is explicitly intended for public release.

Risk: The workflow may require a user-provided Nosi API key.

Mitigation: Use the key only for the publish request, avoid echoing it in outputs, and ask the user to re-register if the service rejects the key.

## Reference(s):

- [Nosi public publishing service](https://nosi.pub)
- [ClawHub skill page](https://clawhub.ai/billhao/skills/nosi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text with shareable URLs and publication status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a human-facing content URL and, when available, a raw text URL.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
