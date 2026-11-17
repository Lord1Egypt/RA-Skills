## Description:

Generate a talkable single-file HTML resume webpage with a built-in keyword-matched resume assistant, WeChat sharing assets, and a deployable shareable link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterzhangzihui](https://clawhub.ai/user/peterzhangzihui)

### License/Terms of Use:

MIT

## Use Case:

External users, job seekers, and personal-branding authors use this skill to turn structured resume content into a shareable HTML resume with a keyword-matched visitor chat interface and WeChat sharing assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted resume data can inject JavaScript into the generated public resume page.

Mitigation: Use only trusted resume JSON/content, validate and escape input fields before publication, and avoid processing third-party resume JSON until script escaping is fixed.

Risk: Generated public resume pages can expose personal data such as phone numbers, email addresses, compensation, or other sensitive profile details.

Mitigation: Review generated pages before sharing, remove sensitive fields, and use access controls or authenticated hosting for private resumes.

Risk: Front-end expiration checks are not strong access control.

Mitigation: Use backend authentication or protected static hosting when access must be enforced.

## Reference(s):

- [Quickstart](references/quickstart.md)
- [WeChat Sharing Reference](references/wechat-sharing.md)
- [ClawHub skill page](https://clawhub.ai/peterzhangzihui/skills/online-resume-creator-chat-enabled-shareable-via-wechat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with commands and generated HTML, PNG, and JSON-backed configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated resume pages are static single-file HTML with inline CSS and JavaScript; optional image outputs include a cover image and QR-code share card.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
