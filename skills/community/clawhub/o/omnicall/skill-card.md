## Description: <br>
Omnicall gives agents access to 248 LLMs, media generation, and live crypto, DeFi, market, web, and research data through a keyless, pay-per-call OpenAI-compatible endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinhughes2121](https://clawhub.ai/user/colinhughes2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure Omnicall as an OpenAI-compatible gateway or OpenClaw default for model routing, hosted generation tools, and live data endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route model prompts and related agent context through Omnicall's third-party hosted service. <br>
Mitigation: Install only after reviewing the service and avoid setting it as a global default in sensitive workspaces. <br>
Risk: The OpenClaw setup can make Omnicall the default paid gateway for agent model traffic. <br>
Mitigation: Review the router package, wallet or payment setup, billing behavior, and the steps needed to revert the routing change before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/colinhughes2121/skills/omnicall) <br>
- [Omnicall API endpoint](https://omnicall.gocreativeai.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown instructions with inline commands and endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure OpenClaw to route model traffic through Omnicall and may call hosted endpoints that return text, media URLs, or live data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
