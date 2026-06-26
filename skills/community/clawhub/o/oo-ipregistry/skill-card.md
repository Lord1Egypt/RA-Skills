## Description: <br>
Ipregistry helps an agent use the OOMOL Ipregistry connector to look up IP address, ASN, user-agent, geolocation, network, company, currency, time zone, and security data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query Ipregistry through the oo CLI for IP intelligence, ASN data, and user-agent parsing without handling raw service credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connected service credentials through OOMOL. <br>
Mitigation: Use it only after confirming the intended Ipregistry connection and review any permission or command prompts before approving installation or execution. <br>
Risk: Lookup results may include security and network intelligence that can be misapplied if treated as complete ground truth. <br>
Mitigation: Review returned Ipregistry data in context and corroborate high-impact security or compliance decisions with appropriate sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oomol/oo-ipregistry) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Ipregistry homepage](https://ipregistry.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return IP intelligence, ASN records, parsed user-agent data, command execution IDs, and setup guidance for OOMOL-managed credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
