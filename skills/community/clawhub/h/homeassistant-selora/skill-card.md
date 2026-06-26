## Description: <br>
Control Home Assistant lights, switches, climate, scenes, and automations from an agent; create and risk-check automations from natural language, validate YAML before deploying, and connect over MCP with OAuth 2.0 through Selora Connect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lafoush](https://clawhub.ai/user/lafoush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and smart-home operators use this skill to connect an agent to Home Assistant through Selora Connect, inspect device state, control entities, and create or review automations with explicit approval steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OAuth callback fallback may expose authorization data if full callback URLs, codes, tokens, or similar login parameters are pasted into chat. <br>
Mitigation: Prefer same-machine OAuth completion where the browser redirect reaches OpenClaw, and do not paste callback URLs, codes, tokens, or similar login parameters unless the publisher provides a safer out-of-band flow or clear redaction guidance. <br>
Risk: The skill can control smart-home devices and create, enable, or delete Home Assistant automations through authorized MCP tools. <br>
Mitigation: Require explicit user confirmation before mutating actions, surface the returned risk assessment, use a second confirmation for high or missing risk, and create automations disabled by default. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lafoush/homeassistant-selora) <br>
- [Selora AI installation documentation](https://selorahomes.com/docs/selora-ai/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Home Assistant entity summaries, automation YAML, risk assessments, OAuth setup guidance, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
