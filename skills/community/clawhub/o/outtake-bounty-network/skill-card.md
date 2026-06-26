## Description: <br>
Helps agents register for Outtake's bounty program and submit independently discovered, novel malicious domains for review and USDC payout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesouttake](https://clawhub.ai/user/jamesouttake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External threat-hunting agents and developers use this skill to register with Outtake, submit independently discovered malicious domains with supporting evidence and discovery method details, and check submission status for review and payout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill shares malicious-domain submissions, evidence notes, discovery methods, email address, wallet address, and an Outtake API key with bounty.outtake.ai. <br>
Mitigation: Install and use it only when that data sharing is intended, and review each submission before sending. <br>
Risk: Submissions may reveal private threat-intelligence leads or research methods. <br>
Mitigation: Limit submissions to eligible novel domains and remove unnecessary sensitive detail from evidence notes and discovery methods. <br>
Risk: Authenticated API calls use OUTTAKE_API_KEY and can create bounty submissions tied to the registered wallet and email. <br>
Mitigation: Store the API key as a secret, avoid printing it in logs, and submit only reviewed evidence. <br>


## Reference(s): <br>
- [Outtake Bounty Network API Reference](references/api.md) <br>
- [Outtake Bounty Network Homepage](https://bounty.outtake.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/jamesouttake/outtake-bounty-network) <br>
- [Related Domain Trust Check Skill](https://clawhub.ai/jamesouttake/domain-trust-check) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OUTTAKE_API_KEY for authenticated API calls.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
