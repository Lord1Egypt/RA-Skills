## Description: <br>
Use Wellness Nourish to give agents local-first nutrition search, barcode lookup, pt-BR meal estimation, intake logging, hydration, goals, and summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to install, configure, troubleshoot, and safely operate the Nutrition MCP server from MCP-compatible clients while preserving local-first privacy boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup and provider workflows may involve OAuth tokens, API keys, service-account JSON, local token files, or other sensitive credentials. <br>
Mitigation: Use least-privilege credentials, avoid printing secrets, and run connection_status, manifest, doctor, privacy_audit, or dry-run checks before live provider calls or writes. <br>
Risk: Nutrition logs, hydration records, meal photos, and related summaries can expose private user data. <br>
Mitigation: Keep local logs under ~/.wellness-nourish/ where expected, require explicit user confirmation before logging meal photos or other writes, and avoid exposing private user data in agent output. <br>
Risk: Nutrition estimates and summaries may be mistaken for professional advice. <br>
Mitigation: Present outputs as informational only and do not treat the tools as medical, legal, financial, or platform-policy advice. <br>


## Reference(s): <br>
- [Nutrition MCP ClawHub page](https://clawhub.ai/davidmosiah/nutrition-mcp) <br>
- [Wellness Nourish repository](https://github.com/davidmosiah/wellness-nourish) <br>
- [Wellness Nourish nutrition documentation](https://wellness.delx.ai/nutrition) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privacy and safety cautions for credentials, local user data, and nutrition-related outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
