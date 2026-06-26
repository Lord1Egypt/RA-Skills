## Description: <br>
Talentir HumanPay helps agents create and inspect Talentir payouts and webhooks through documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johanneskares](https://clawhub.ai/user/johanneskares) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare Talentir API calls for creator payouts, payout lookup, team information, and webhook management from an OpenClaw shell environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables money-moving Talentir payout operations and webhook changes from an agent shell environment. <br>
Mitigation: Use a dedicated low-limit Talentir API key, confirm every payout and webhook change manually, and avoid auto-approval permissions unless they are explicitly required. <br>
Risk: Unexpected behavior could create unauthorized payouts or send webhook data to an unintended endpoint. <br>
Mitigation: Verify webhook URLs before use, monitor Talentir activity, and revoke or rotate the API key if behavior is unexpected. <br>


## Reference(s): <br>
- [Talentir API](https://www.talentir.com/api/v1) <br>
- [Talentir Business Account Setup](https://www.talentir.com/start/business) <br>
- [ClawHub Skill Page](https://clawhub.ai/johanneskares/humanpay) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with curl and jq shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TALENTIR_API_KEY plus curl and jq.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
