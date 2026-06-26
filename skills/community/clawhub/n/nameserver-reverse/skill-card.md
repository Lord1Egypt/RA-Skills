## Description: <br>
Provides DomainKits MCP configuration and examples for newly registered domain search and nameserver reverse lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ABTdomain](https://clawhub.ai/user/ABTdomain) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Domain investors, brand managers, and researchers use this skill to configure MCP clients for DomainKits domain intelligence tools and query newly registered domains or domains hosted on a specified nameserver. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain lookup terms are sent to the remote DomainKits MCP service. <br>
Mitigation: Use the skill only where sending lookup terms to DomainKits is acceptable for the user's data-handling requirements. <br>
Risk: Setup examples rely on external MCP installation commands and remote service endpoints. <br>
Mitigation: Review the remote service and extension source before deploying in environments with strict supply-chain controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ABTdomain/nameserver-reverse) <br>
- [DomainKits](https://domainkits.com) <br>
- [DomainKits newly registered domains search](https://domainkits.com/search/new) <br>
- [DomainKits nameserver reverse lookup](https://domainkits.com/tools/ns-reverse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP client configuration snippets, curl examples, tool parameters, rate limits, and privacy notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
