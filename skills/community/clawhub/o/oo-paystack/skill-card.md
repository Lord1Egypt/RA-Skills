## Description:

Paystack (paystack.com). Use this skill for ANY Paystack request — reading, creating, and updating data. Whenever a task involves Paystack, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to read Paystack customers and transactions, initialize and verify transactions, and create or update customers through an OOMOL-connected Paystack account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A payment checkout can be initialized without confirming its details first.

Mitigation: Require confirmation of the checkout details before initialization.

Risk: Setup executes a remote CLI installer that was unavailable for inspection.

Mitigation: Review and verify the CLI installer separately, and review or disable its automatic skill synchronization.

## Reference(s):

- [Paystack API documentation](https://paystack.com/docs/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses include data and execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
