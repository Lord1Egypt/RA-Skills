## Description: <br>
IPQualityScore (ipqualityscore.com) helps an agent inspect and run IPQualityScore connector actions for IP reputation checks, URL or domain scans, email validation, and phone validation through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to run IPQualityScore lookups from an OOMOL-connected account without handling raw service credentials. It supports reputation, abuse-risk, deliverability, and threat-signal checks for IP addresses, URLs or domains, email addresses, and phone numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected IPQualityScore account. <br>
Mitigation: Install only when the publisher is trusted and use the documented OOMOL connection flow so raw service tokens are not handled by the agent. <br>
Risk: Connector actions can send IP addresses, URLs, domains, email addresses, or phone numbers to IPQualityScore for analysis. <br>
Mitigation: Confirm that submitted data is appropriate for the user's account, policy, and jurisdiction before running lookups. <br>


## Reference(s): <br>
- [ClawHub IPQualityScore Skill Page](https://clawhub.ai/oomol/oo-ipqualityscore) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [IPQualityScore Homepage](https://www.ipqualityscore.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OOMOL server-side credential injection and returns connector data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
