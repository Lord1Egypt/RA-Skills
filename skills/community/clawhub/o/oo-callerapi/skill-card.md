## Description:

Use CallerAPI to search phone-number reputation and retrieve authenticated account information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up phone-number spam reputation, business details, complaints, and optional carrier data, or retrieve the authenticated CallerAPI account email and credit balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute unverified remote code, and its local changes are not fully disclosed.

Mitigation: Review setup before enabling it, install a vetted CLI release manually, and consider disabling automatic skill synchronization.

Risk: CallerAPI requests are mediated by OOMOL.

Mitigation: Understand the data flow and use the skill only for information you are comfortable routing through OOMOL.

## Reference(s):

- [CallerAPI homepage](https://callerapi.com)
- [CallerAPI API documentation](https://docs.callerapi.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON responses with optional text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only CallerAPI queries; available fields depend on the selected action's live schema.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
