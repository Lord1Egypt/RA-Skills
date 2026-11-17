## Description:

Hemlane MCP turns saved Hemlane browser HAR captures into repeatable MCP tools and scripts, with authentication supplied at runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and property-management operators use Hemlane MCP to inspect HAR-derived Hemlane GraphQL operations, run read queries, and execute guarded workflows such as tenant replies, referrals, maintenance comments, and transaction lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect a live Hemlane account, including tenant messages, comments, referrals, and lease records.

Mitigation: Review each live-account action before execution and require an authorized operator for write workflows.

Risk: The skill handles browser session credentials and authentication artifacts.

Mitigation: Use a dedicated low-privilege Hemlane account when possible, avoid capturing auth from a normal browser profile, and keep auth files private and short-lived.

Risk: A custom GraphQL endpoint could direct authenticated requests to an untrusted destination.

Mitigation: Do not set HEMLANE_GRAPHQL_ENDPOINT unless the destination is fully trusted.

## Reference(s):

- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [HAR Summary](artifact/references/har-summary.md)
- [GraphQL Operations](artifact/references/graphql-operations.md)
- [Financials HAR Summary](artifact/references/financials-har-summary.md)
- [Operation Catalog](artifact/references/operation-catalog.json)
- [Runbooks](artifact/references/runbooks.md)
- [Replay Scaffold](artifact/references/replay-scaffold.md)
- [Rent Roll Integration](artifact/references/rent-roll-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON/API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute live Hemlane account reads or guarded write workflows when runtime credentials and authorization are supplied.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
