## Description:

Upload AI-generated HTML games, apps, or generative art to PaperBox and return a shareable link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felixdaga](https://clawhub.ai/user/felixdaga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to publish completed self-contained HTML games, apps, or generative art to PaperBox and send the resulting shareable URL back to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A completed HTML project could be uploaded to a public or shareable PaperBox page without sufficiently explicit user confirmation.

Mitigation: Confirm that the user wants the specific project published before upload, and review the HTML for secrets, tokens, private customer data, proprietary code, or other sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felixdaga/skills/paperbox)
- [PaperBox homepage](https://paperbox-beta.vercel.app)
- [PaperBox upload API](https://paperbox-beta.vercel.app/api/games)
- [PaperBox login](https://paperbox-beta.vercel.app/login)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with an API request pattern and a returned shareable URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PaperBox API key and outbound network access to upload the completed HTML project.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
