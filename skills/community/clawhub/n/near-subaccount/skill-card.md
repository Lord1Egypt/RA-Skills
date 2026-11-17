## Description:

Create, list, delete, and manage NEAR subaccounts with bulk distribution operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to create, list, delete, and fund NEAR subaccounts from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs blockchain account creation, deletion, and token transfer operations.

Mitigation: Use it first in a test or low-value NEAR environment and review each command before execution.

Risk: Security evidence reports unsafe shell command construction and weak safeguards around destructive operations.

Mitigation: Validate account IDs and amounts, prefer argument-based process execution, and add explicit confirmations or dry-run previews for delete and bulk distribution workflows.

## Reference(s):

- [NEAR CLI](https://docs.near.org/tools/near-cli)
- [NEAR Subaccounts](https://docs.near.org/concepts/account/subaccounts)
- [ClawHub Skill Page](https://clawhub.ai/shaiss/skills/near-subaccount)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference NEAR account IDs, NEAR token amounts, and JSON files containing subaccount lists.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
