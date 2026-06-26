## Description: <br>
This skill supports Google Analytics requests involving reading, creating, and updating data through the OOMOL Google Analytics connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Google Analytics account and property setup, run GA4 reports, and manage selected property or custom definition settings through the OOMOL connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes actions that can change Google Analytics property settings and custom definitions. <br>
Mitigation: Confirm the exact action, target, payload, and expected effect with the user before running write or destructive actions. <br>
Risk: Connector actions depend on the connected Google Analytics account and live action schemas. <br>
Mitigation: Inspect the connector schema before each action and use first-time setup steps only when an authentication or connection error occurs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-google-analytics) <br>
- [Google Analytics](https://analytics.google.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
