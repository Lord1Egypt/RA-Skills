## Description:

Marketup CRM - detail/list search, advanced filtering, create, modify, assignment flows, history/behavior lookup, lead-to-account conversion, tags, and pool configuration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azu-zhou](https://clawhub.ai/user/azu-zhou)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, marketing, and CRM operators use this skill through an agent to query Marketup leads and accounts, inspect histories and behavior records, and perform approved CRM updates such as creating, modifying, assigning, converting, tagging, receiving, or returning records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a persistent MarketUP API key that is stored in plaintext at ~/.openclaw/.env.

Mitigation: Use a least-privilege MarketUP API key, restrict the environment file permissions, and rotate the key if it is exposed.

Risk: The skill can perform live CRM write actions, including create, modify, assign, convert, tag, receive, return, and pool actions.

Mitigation: Require operator approval for each write or pool action and review returned API responses before treating an operation as complete.

Risk: The security verdict is suspicious because the skill combines credential handling with live CRM writes without enough guardrails.

Mitigation: Review before installing and avoid production CRM data unless operators explicitly approve the intended actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azu-zhou/skills/marketup-uc)
- [Reference index](references/README.md)
- [Setup MARKETUP_API_KEY](references/setup-marketup-api-key.md)
- [Find leads reference](references/find-leads.md)
- [Leads mutation APIs](references/leads-mutations.md)
- [Lead history APIs](references/leads-history.md)
- [Form fields and lead conversion](references/convert-and-forms.md)
- [Lead pool and user helpers](references/pool-and-users.md)
- [Accounts query reference](references/accounts-query.md)
- [Accounts mutation and pool reference](references/accounts-mutations-and-pool.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with curl and jq command snippets when API execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and MARKETUP_API_KEY for live Marketup CRM API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
