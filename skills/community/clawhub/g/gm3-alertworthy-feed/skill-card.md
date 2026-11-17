## Description:

Read-only access to the GM3 Alertworthy feed, providing real-time token market data for analysis agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigbadman-lab](https://clawhub.ai/user/bigbadman-lab)

### License/Terms of Use:


## Use Case:

External analysts and agent developers use this skill to fetch current GM3 alertworthy-token market snapshots for downstream analysis, filtering, and decision support. The skill is analysis-only and does not perform ranking, strategy logic, or trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GM3 API key exposure or misuse.

Mitigation: Store the API key as a secret and never expose it in client-side code.

Risk: Market data may be mistaken for trading advice or execution authority.

Mitigation: Treat returned token data as analysis input and keep filtering, decision logic, and any trading actions outside this skill.

Risk: Dependency on a third-party market data API and active entitlement.

Mitigation: Install only if you trust GM3 as the data provider and handle 401, 429, and temporary 5xx responses in agent workflows.

## Reference(s):

- [GM3 Alertworthy API endpoint](https://api.gm3.fun/functions/v1/gm3-api/v1/paid/alertworthy)
- [ClawHub skill page](https://clawhub.ai/bigbadman-lab/skills/gm3-alertworthy-feed)

## Skill Output:

**Output Type(s):** [JSON, API data]

**Output Format:** [JSON object containing a data array of alertworthy token snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GM3 Developer API key; exact response fields may change as the GM3 platform evolves.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
