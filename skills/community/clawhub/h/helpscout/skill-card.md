## Description:

Fetch and reply to Helpscout conversations

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabiensebban](https://clawhub.ai/user/fabiensebban)

### License/Terms of Use:


## Use Case:

Customer support operators and developers use this skill to fetch Help Scout inbox conversations, filter conversation lists, and create internal notes or replies through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured inbox list should not be treated as a complete security boundary for customer conversation access.

Mitigation: Use a Help Scout app with the narrowest possible permissions and add explicit allowlist checks before using the skill with real customer data.

Risk: The documented send-reply behavior and implemented controls do not line up clearly.

Mitigation: Review the code and documentation before enabling customer-visible replies; limit use to reviewed internal-note workflows until reconciled.

Risk: The security evidence recommends dependency updates before real customer-data use.

Mitigation: Update dependencies, rerun security scans, and review the skill before installation in a production support workflow.

## Reference(s):

- [HelpScout API Documentation Reference](references/helpscout-api.md)
- [Help Scout Developer Documentation](https://developer.helpscout.com/)
- [ClawHub Skill Page](https://clawhub.ai/fabiensebban/skills/helpscout)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON objects containing Help Scout conversation data or note/reply status, with text fields from conversations and replies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API_KEY, APP_SECRET, and INBOX_IDS; output depends on Help Scout API permissions, filters, pagination, and network availability.]

## Skill Version(s):

1.0.2 (source: server release metadata; package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
