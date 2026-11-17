## Description:

OKKI Go helps agents and sales teams find B2B prospect companies, unlock selected company details and contact emails, draft or send outbound email, and check balances or delivery status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okki-op](https://clawhub.ai/user/okki-op)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, and agent operators use this skill to search global B2B prospects, review company matches, unlock selected company details, and manage outbound email workflows with explicit confirmation for paid or send actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid unlocks and email sends can consume credits or send outreach to real recipients.

Mitigation: Require explicit confirmation of selected companies, credit cost, recipients, and final email content before running paid or send actions.

Risk: The skill stores an API key, profile data, viewed or unlocked state, and attribution metadata locally.

Mitigation: Install only if the publisher is trusted, use the documented secure save path, and protect the OKKI Go config directory.

Risk: Changing OKKIGO_BASE_URL can redirect API traffic away from the default OKKI Go endpoint.

Mitigation: Keep OKKIGO_BASE_URL unset unless deliberately using a trusted test endpoint.

Risk: Update notifications may create a recurring local notification job.

Mitigation: Decline update notifications if recurring checks are not desired, or review the notification setup before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/okki-op/skills/okki-go)
- [OKKI Go](https://go.okki.ai)
- [Authentication](references/authentication.md)
- [Context Firewall](references/context-firewall.md)
- [Output Contracts](references/output-contracts.md)
- [Paid Actions](references/paid-actions.md)
- [API Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with script-rendered tables, compact JSON outputs, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal output is compact and user-facing; raw data, private mappings, and debug metadata are hidden unless explicitly requested.]

## Skill Version(s):

1.3.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
