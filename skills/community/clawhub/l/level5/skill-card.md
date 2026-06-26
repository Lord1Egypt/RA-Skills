## Description: <br>
Budget management for AI agents through a USDC billing gateway on Solana for per-token LLM compute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-gilbert](https://clawhub.ai/user/chris-gilbert) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Level5 to register and configure a USDC-funded billing proxy for LLM calls across OpenAI, Anthropic, and OpenRouter, with balance tracking and dashboard access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures a paid LLM billing proxy that requires USDC deposits. <br>
Mitigation: Use it only when Level5 billing is intended, and verify the service and payment details before depositing funds. <br>
Risk: The dashboard URL and API token provide access to the billing account. <br>
Mitigation: Protect the dashboard URL and API token like passwords, and avoid sharing them in prompts, logs, or public files. <br>
Risk: LLM prompts and responses may be routed through the Level5 proxy. <br>
Mitigation: Avoid sending sensitive prompts through the proxy unless the user is comfortable with the service's privacy and retention practices. <br>


## Reference(s): <br>
- [Level5 homepage](https://level5.cloud) <br>
- [Level5 service descriptor](https://level5.cloud/.well-known/agent-service.json) <br>
- [Canonical Level5 skill file](https://level5.cloud/SKILL.md) <br>
- [ClawHub Level5 listing](https://clawhub.ai/chris-gilbert/level5) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before registration or network calls; dashboard URLs contain account tokens and should be handled as secrets.] <br>

## Skill Version(s): <br>
1.6.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
