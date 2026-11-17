## Description:

Automates Juejin publishing and supports Zhihu browser-assisted publishing from Markdown posts, including login cookie capture, draft creation, cover generation, column management, publishing, and audit status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thneoly](https://clawhub.ai/user/thneoly)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, developers, and publishing operators use this skill to prepare, validate, publish, and schedule Markdown articles for Juejin and to populate Zhihu article drafts through a browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live account cookies and browser profile data can expose publishing accounts if shared or committed.

Mitigation: Treat .juejin.env and .cdp-profile as credentials; keep them outside source control, shared folders, and public artifacts.

Risk: Publishing and scheduled publishing can post public content without a final approval gate.

Mitigation: Review posts with the preview flow before publishing, and avoid zhihu --auto or scheduled publishing unless unattended public posting is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thneoly/skills/juejin-publisher-pro)
- [Juejin category ID reference](references/category_ids.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples and Python publishing scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local credential, browser profile, metadata, cover image, draft, published post, and scheduling artifacts when executed.]

## Skill Version(s):

1.0.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
