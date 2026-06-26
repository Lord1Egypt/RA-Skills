## Description: <br>
Real-time retrieval of the latest official OpenClaw documentation, returned as compact LLM-friendly Markdown for config, CLI, channels, gateway, and skills questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sakayoo](https://clawhub.ai/user/sakayoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, and AI assistants use this skill to look up current OpenClaw documentation before answering questions, generating commands, or changing configuration for CLI, gateway, channels, diagnostics, deployment, and skills workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation search keywords are sent to public OpenClaw and Mintlify documentation services. <br>
Mitigation: Do not include secrets, tokens, private configuration, internal URLs, customer data, or proprietary details in search queries. <br>
Risk: Retrieved documentation may not account for a user's local environment or version-specific deployment constraints. <br>
Mitigation: Review source paths and validate commands or configuration changes against the target environment before applying them. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw Docs Search ClawHub Page](https://clawhub.ai/sakayoo/openclaw-docs-search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Compact Markdown search results and page excerpts with source paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns cleaned documentation snippets or a single fetched page body converted from the public OpenClaw docs site.] <br>

## Skill Version(s): <br>
1.0.4 (source: evidence.json, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
