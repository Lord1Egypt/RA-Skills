## Description: <br>
DNS record lookups via Google DNS-over-HTTPS - A, AAAA, MX, NS, TXT, CNAME, and reverse DNS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security analysts use this skill to query DNS records, verify DNS propagation, troubleshoot email delivery records, and perform reverse DNS lookups during domain or infrastructure investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DNS queries may disclose domains, IPs, confidential internal hostnames, private infrastructure indicators, or sensitive investigation targets to the Pipeworx gateway and Google DNS-over-HTTPS. <br>
Mitigation: Avoid querying sensitive or private targets unless that disclosure is acceptable for the intended investigation or operational workflow. <br>
Risk: The optional setup uses npx mcp-remote@latest, which can install or run a moving dependency version. <br>
Mitigation: Review the setup command and prefer pinned dependency versions where repeatability or supply-chain control is required. <br>


## Reference(s): <br>
- [Pipeworx DNS Pack](https://pipeworx.io/packs/dns) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-dns) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Configuration] <br>
**Output Format:** [DNS lookup results and setup guidance, including JSON MCP configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and sends DNS lookup requests to remote DNS services.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
