## Description: <br>
Capture and automate macOS UI with the Peekaboo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect, capture, and automate macOS interfaces through Peekaboo CLI commands for screenshots, UI targeting, input, app management, and window workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to operate macOS UI, including screen capture, clipboard access, app control, and input actions. <br>
Mitigation: Install and use it only when that level of local UI automation is intended; review proposed commands before execution. <br>
Risk: Screenshots, clipboard contents, or automated interactions may expose secrets or affect sensitive applications. <br>
Mitigation: Avoid capturing secret-bearing screens or clipboard data, and do not automate credentials or sensitive apps unless the workflow is explicitly trusted. <br>
Risk: The skill requires macOS Screen Recording and Accessibility permissions, which increase local automation capability. <br>
Mitigation: Grant permissions only on systems where Peekaboo automation is needed and remove them when no longer required. <br>


## Reference(s): <br>
- [Peekaboo homepage](https://peekaboo.boo) <br>
- [ClawHub Peekaboo skill page](https://clawhub.ai/steipete/peekaboo) <br>
- [ClawHub steipete publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces macOS Peekaboo CLI command guidance; commands may emit JSON when the CLI is run with --json or -j.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
