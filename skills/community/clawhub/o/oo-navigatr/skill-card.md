## Description:

Use this skill to read, create, update, and delete Navigatr data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to inspect badges and assertions, issue badges, revoke assertions, and verify badge assertions in Navigatr.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may automatically change skills installed for other agents.

Mitigation: Review the CLI setup and prefer a reviewed, versioned installation. Set OO_SKILLS_SYNC_DISABLED=1 for CLI invocations unless automatic skill changes are intended.

Risk: Badge issuance, revocation, and verification can change Navigatr records or their public verification indicator.

Mitigation: Connect only the intended Navigatr account, confirm the action and target, and retain the required approvals before making badge changes.

## Reference(s):

- [Navigatr](https://www.navigatr.org)
- [Navigatr API documentation](https://api.navigatr.app/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, API calls, Guidance]

**Output Format:** [Shell commands and JSON payloads, with connector results returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema; read actions return data and state-changing actions require approval.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
