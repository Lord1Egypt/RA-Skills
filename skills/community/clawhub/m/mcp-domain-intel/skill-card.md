## Description: <br>
Provides domain intelligence through WHOIS lookups and domain availability checks via the L402 API for brand research, cybersecurity investigations, and domain acquisition planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haveblue997](https://clawhub.ai/user/haveblue997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, brand-protection teams, and domain acquisition researchers use this skill to query WHOIS/DNS intelligence and check domain registration availability from an MCP client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain names submitted to the lookup or availability tools may be sent to the configured external API provider. <br>
Mitigation: Use the skill only with providers whose privacy and retention practices are acceptable for the queried domains. <br>
Risk: Sensitive internal domains, acquisition targets, or investigation subjects could disclose confidential intent if queried through an untrusted provider. <br>
Mitigation: Avoid sensitive queries unless the provider is trusted and approved for the investigation context. <br>
Risk: The release license evidence conflicts with artifact-level license text. <br>
Mitigation: Confirm whether MIT-0 or MIT governs the release before public publication or downstream redistribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haveblue997/mcp-domain-intel) <br>
- [Blue-Trianon-Ventures GitHub profile](https://github.com/Blue-Trianon-Ventures) <br>
- [Configured Nautdev API base URL](https://api.nautdev.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [MCP tool responses containing JSON-formatted text, plus JSON configuration snippets for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tools accept a domain string and return lookup, availability, or error details from the configured API provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
