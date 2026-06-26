## Description: <br>
Marketup CRM - detail/list search, advanced filtering, create, modify, assignment flows, history/behavior lookup, lead-to-account conversion, tags, and pool configuration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azu-zhou](https://clawhub.ai/user/azu-zhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External CRM operators and agents use this skill to search, create, modify, assign, tag, and convert MarketUP leads and accounts through authenticated MarketUP CRM API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MarketUP API key and stores it persistently in ~/.openclaw/.env. <br>
Mitigation: Use a least-privilege, revocable API key; remove or rotate the key when access is no longer needed. <br>
Risk: The skill can modify CRM records, including creating, assigning, tagging, converting, and returning leads or accounts. <br>
Mitigation: Ask the agent to show target records and proposed payloads before important write actions, and rely on API responses before treating an operation as complete. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/azu-zhou/marketup-uc) <br>
- [marketup-uc references](references/README.md) <br>
- [Setup MARKETUP_API_KEY](references/setup-marketup-api-key.md) <br>
- [Find Leads Reference](references/find-leads.md) <br>
- [Leads write APIs](references/leads-mutations.md) <br>
- [Lead history APIs](references/leads-history.md) <br>
- [Form fields and lead to account conversion](references/convert-and-forms.md) <br>
- [Lead pool and user helpers](references/pool-and-users.md) <br>
- [Accounts query reference](references/accounts-query.md) <br>
- [Accounts mutation and pool reference](references/accounts-mutations-and-pool.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with curl/jq shell commands and JSON payload guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MARKETUP_API_KEY, curl, and jq; may perform authenticated MarketUP CRM read and write API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
