## Description:

FundzWatch (fundzwatch.ai). Use this skill for ANY FundzWatch request — reading, creating, and updating data. Whenever a task involves FundzWatch, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use an agent to query FundzWatch company, market, broker, lender, and watchlist data through a connected account, and to add company domains to its watchlist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation and setup can affect the user's agent environment, and the remote installers and connector implementation are unverified.

Mitigation: Review and approve CLI installation separately, use a verified release, and check bundled-skill installation and synchronization behavior before setup.

Risk: Adding domains changes the connected FundzWatch watchlist.

Mitigation: Confirm the exact domains and resulting watchlist change with the user before running the write action.

## Reference(s):

- [FundzWatch](https://fundzwatch.ai/)
- [FundzWatch API documentation](https://fundzwatch.ai/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data and preview limits depend on the selected action and connected FundzWatch account.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
