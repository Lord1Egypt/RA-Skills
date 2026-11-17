## Description:

Vision-driven desktop automation skill that helps an agent control native desktop applications on macOS, Windows, and Linux through Midscene screenshot-based commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanru](https://clawhub.ai/user/quanru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to automate and verify desktop-native applications that cannot be driven through browser DOM or accessibility APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the real desktop, including mouse and keyboard input.

Mitigation: Install only when full desktop automation is needed and run it in a dedicated VM or restricted OS account when possible.

Risk: Screenshots and generated automation reports may capture sensitive visible screen data.

Mitigation: Close or hide sensitive windows before use and treat screenshots, reports, and replay artifacts as sensitive data.

Risk: The documented commands use automatic npx package execution for Midscene.

Mitigation: Prefer an exact pinned and reviewed Midscene package version instead of a floating package invocation.

Risk: Desktop automation can interact with the wrong window or display if screen state is not verified.

Mitigation: Run a health check, confirm the target app is foregrounded, use one Midscene command at a time, and verify state with screenshots or assertions before continuing.

## Reference(s):

- [Midscene.js](https://midscenejs.com)
- [Midscene Model Configuration](https://midscenejs.com/model-common-config)
- [ClawHub Skill Page](https://clawhub.ai/quanru/skills/midscene-computer-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference screenshots and Midscene HTML, Markdown, or JSON reports generated during automation.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
