## Description: <br>
Interact with the Oasyce decentralized AI data marketplace. Register data assets, trade via bonding curves, invoke AI capabilities, and settle payments between agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shangri-la-0428](https://clawhub.ai/user/shangri-la-0428) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Oasyce to register marketplace data assets, trade shares through bonding curves, invoke AI capabilities, and inspect settlement, reputation, and network state through the Oasyce CLI and Python SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace commands may spend tokens, sell shares, register public assets or endpoints, resolve disputes, or onboard a node. <br>
Mitigation: Use a testnet or low-value account first and require explicit approval before any value-moving or public registration command runs. <br>
Risk: Capability invocation or endpoint registration may send private data to an external AI capability provider. <br>
Mitigation: Verify the active provider, endpoint, wallet, and account before use, and avoid sending secrets or sensitive data unless the provider is approved. <br>
Risk: The skill depends on Oasyce pip packages and an active wallet or account outside the skill artifact. <br>
Mitigation: Verify the installed packages with `oas doctor --json` and confirm the intended wallet or account before executing marketplace operations. <br>


## Reference(s): <br>
- [ClawHub Oasyce release page](https://clawhub.ai/shangri-la-0428/oasyce) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands support JSON output via --json.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
