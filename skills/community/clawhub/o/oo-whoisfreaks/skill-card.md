## Description: <br>
WhoisFreaks (whoisfreaks.com) support for searching and reading domain, IP, ASN, availability, and subdomain data through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to run user-directed WhoisFreaks lookups for domains, IP addresses, autonomous systems, domain availability, and subdomains from an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected WhoisFreaks account and may use account credentials or billing through the OOMOL connector. <br>
Mitigation: Use it only with an intended OOMOL-connected WhoisFreaks account, and run setup, login, connection, or billing steps only after a relevant failure and user confirmation. <br>
Risk: WHOIS, IP, ASN, and subdomain lookups are sent to the WhoisFreaks/OOMOL connector. <br>
Mitigation: Submit only lookup targets the user explicitly wants to query, and avoid adding unrelated sensitive data to action payloads. <br>
Risk: Connector action inputs can change over time. <br>
Mitigation: Inspect the live action schema before building payloads and match requests to the authoritative schema. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-whoisfreaks) <br>
- [WhoisFreaks homepage](https://whoisfreaks.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector responses as JSON when commands are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
