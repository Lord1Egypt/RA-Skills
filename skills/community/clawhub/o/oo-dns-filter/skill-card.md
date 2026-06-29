## Description: <br>
Operate DNSFilter through an OOMOL-connected account using the oo CLI for DNSFilter lookup and listing actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect DNSFilter tenant data such as users, public IP, categories, applications, IP address records, networks, and policies through an OOMOL-connected DNSFilter account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates through a connected DNSFilter account, so unintended tenant operations could expose or affect DNSFilter data. <br>
Mitigation: Use it only for explicit DNSFilter tenant requests and review any proposed policy or configuration changes before allowing execution. <br>
Risk: The scanner notes that the trigger wording is broader than ideal. <br>
Mitigation: Invoke the skill only when the user request is clearly about DNSFilter, and fetch each action's live schema before running connector commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-dns-filter) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [DNSFilter Homepage](https://www.dnsfilter.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches the live connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
