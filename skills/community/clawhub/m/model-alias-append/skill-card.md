## Description: <br>
Automatically appends the model alias to the end of every response with integrated hook functionality and configuration change detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ccapton](https://clawhub.ai/user/Ccapton) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to show which configured model alias generated a response, especially when tracking model attribution or monitoring alias configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model aliases are appended directly into responses and could confuse downstream readers or agents if aliases contain instruction-like text. <br>
Mitigation: Use short, descriptive aliases from a trusted OpenClaw configuration and avoid aliases that look like commands or policy text. <br>
Risk: The skill monitors and reads local OpenClaw configuration to resolve aliases, so untrusted configuration changes can affect response attribution. <br>
Mitigation: Keep the OpenClaw configuration trusted and review alias changes before relying on the attribution text. <br>
Risk: The sample configuration binds a local gateway to 0.0.0.0, which can expose services on reachable networks if reused without intent. <br>
Mitigation: Use a local-only bind unless remote access is explicitly required and network exposure is controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ccapton/model-alias-append) <br>
- [OpenClaw response hook documentation](https://docs.openclaw.ai/hooks#response-alias-injector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown text appended to an agent response, usually a bold model alias and optional configuration update notice.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves supported reply tags when appending the alias.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
