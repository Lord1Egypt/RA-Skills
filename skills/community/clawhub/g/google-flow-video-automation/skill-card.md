## Description:

Automatically generate AI videos on Google Flow (labs.google/fx/tools/flow) via Chrome CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate Google Flow video generation from prompts in a logged-in Chrome session, including video settings and MP4 download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation exposes a logged-in Chrome profile through Chrome DevTools Protocol.

Mitigation: Use a dedicated Chrome automation profile or separate OS account, bind CDP to 127.0.0.1, close the debug browser after use, and avoid opening unrelated sensitive sites in that profile.

Risk: The automation can automatically confirm Google Flow credit-spending prompts.

Mitigation: Run the scripts only when the operator is comfortable with automatic confirmation and understands the credit cost of the requested generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/google-flow-video-automation)
- [Google Flow](https://labs.google/fx/tools/flow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration; automation scripts can download MP4 files when run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Google Chrome with local Chrome DevTools Protocol access.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
