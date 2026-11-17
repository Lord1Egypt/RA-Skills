## Description:

Automates batch uploads of game assets to the mmgame.woa.com operations platform using a logged-in browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xymhxy](https://clawhub.ai/user/xymhxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to upload image and combination game marketing assets to the WeChat game operations platform, including repeated updates across templates and categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a logged-in mmgame browser session to upload and submit selected assets.

Mitigation: Confirm the target game, file list, and upload category before running the workflow.

Risk: The artifact references scripts/upload.js, but that script is not included in the package.

Mitigation: Review any external upload script before using it with a logged-in browser session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xymhxy/skills/mmgamexxyanguo)
- [Publisher profile](https://clawhub.ai/user/xymhxy)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown instructions with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide browser automation through Playwright MCP and report upload results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
