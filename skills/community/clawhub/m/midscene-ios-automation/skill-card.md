## Description:

Vision-driven iOS device automation using Midscene CLI and WebDriverAgent from screenshots, without requiring DOM access or accessibility labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanru](https://clawhub.ai/user/quanru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to automate and verify iOS app workflows on connected iPhone or iPad devices through natural-language commands, screenshots, and Midscene CLI actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a connected iPhone or iPad and may perform unintended actions if prompts or screen interpretation are wrong.

Mitigation: Use a test device or test account where possible, run one command at a time, review screenshots between actions, and verify final state with assertions.

Risk: Screenshots and reports may contain sensitive information and can be processed by external model providers.

Mitigation: Avoid sensitive screens unless necessary, review screenshots and reports before sharing them, and keep only the required model API key available to the process.

Risk: The skill invokes npm packages through Midscene CLI, and mutable package resolution can change behavior over time.

Mitigation: Prefer pinned, reviewed Midscene package versions and review generated reports and scanner results before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quanru/skills/midscene-ios-automation)
- [Midscene.js](https://midscenejs.com)
- [Midscene Model Configuration](https://midscenejs.com/model-common-config)
- [Midscene iOS Getting Started](https://midscenejs.com/ios-getting-started.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce paths to screenshots, reports, or converted report files created by Midscene CLI runs.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
