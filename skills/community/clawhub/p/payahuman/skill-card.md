## Description: <br>
Pay a Human lets agents prepare Talentir API requests for creator payouts, payout lookup, team information, and payout webhook management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johanneskares](https://clawhub.ai/user/johanneskares) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to prepare Talentir API calls that send payments to creators, track payout records, inspect team information, and administer payout webhooks from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare requests that initiate real payouts when a Talentir API key is available. <br>
Mitigation: Use limited-scope credentials, require explicit approval before every payout, and keep Talentir daily spend limits in place. <br>
Risk: Webhook creation or deletion can expose payout events or disrupt existing payout integrations. <br>
Mitigation: Review the target URL, event type, and environment before webhook changes, and require approval before creating or deleting webhooks. <br>
Risk: Team metadata and payout records may expose sensitive business or recipient information. <br>
Mitigation: Limit API key permissions and share command outputs only with users authorized to see payment and account data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johanneskares/payahuman) <br>
- [Talentir API](https://www.talentir.com/api/v1) <br>
- [Talentir business signup](https://www.talentir.com/start/business) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and TALENTIR_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
