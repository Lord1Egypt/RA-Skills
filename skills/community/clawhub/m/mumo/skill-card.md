## Description: <br>
Mumo guides OpenClaw agents through structured multi-model deliberations via mumo's MCP server for architecture decisions, design reviews, red-team reviews, uncertainty expansion, and other high-regret choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericatmumo](https://clawhub.ai/user/ericatmumo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Mumo to ask an OpenClaw agent to run a multi-model panel before high-regret product, architecture, security, migration, and launch decisions, then synthesize claim-map evidence into actionable guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a mumo platform API key in the MCP server configuration. <br>
Mitigation: Store the key only in the local OpenClaw MCP configuration, review the registration command before running it, and rotate keys that are exposed or no longer needed. <br>
Risk: Mumo panel output is advisory and can be incomplete or wrong even when models agree. <br>
Mitigation: Use the claim map to inspect assumptions and disagreement, then verify recommendations with tests, source evidence, or user confirmation before changing the workspace. <br>
Risk: Security guidance flags powerful authenticated actions in the reviewed release context. <br>
Mitigation: Review commands before confirming writes, especially bans, role changes, package transfers, production migrations, and outbound email. <br>


## Reference(s): <br>
- [Mumo MCP documentation](https://mumo.chat/docs/mcp) <br>
- [Mumo REST API documentation](https://mumo.chat/docs/api) <br>
- [Mumo OpenClaw install guide](https://mumo.chat/install/openclaw) <br>
- [Mumo product site](https://mumo.chat) <br>
- [ClawHub listing](https://clawhub.ai/ericatmumo/mumo) <br>
- [Claim Maps](references/claim-maps.md) <br>
- [Model Selection](references/model-selection.md) <br>
- [Operating Notes](references/operating-notes.md) <br>
- [Recap and Synthesis](references/recap.md) <br>
- [Snippets](references/snippets.md) <br>
- [Synthesis](references/synthesis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a mumo platform API key and registered MCP server; deliberation output is advisory and should be verified before workspace changes.] <br>

## Skill Version(s): <br>
0.4.0 (source: changelog, released 2026-06-19; server release metadata agrees) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
