## Description: <br>
Analyze Google Ads search-term CSV exports locally and draft negative-keyword plans with dry-run safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and agent operators use this skill to install, configure, and safely operate Google Ads Intent MCP for local search-term CSV analysis and negative-keyword planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Ads OAuth tokens, API keys, service-account files, local token files, or private CSV exports could be exposed if copied into chat or logs. <br>
Mitigation: Keep credentials and exports local, do not paste secrets into chat, and use connection status, doctor, manifest, privacy audit, and dry-run checks before sharing outputs. <br>
Risk: Future live-account tooling could change ad-account state if used without clear user consent. <br>
Mitigation: Default to exported CSV analysis and require explicit confirmation before any live provider call or account mutation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidmosiah/google-ads-intent-mcp) <br>
- [Google Ads Intent MCP repository](https://github.com/davidmosiah/google-ads-intent-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on dry-run workflows, privacy checks, and explicit handling of Google Ads credentials and exported CSV data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
