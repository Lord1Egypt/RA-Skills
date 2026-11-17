## Description:

Connects an OOMOL account to NetSuite to read, create, and update records through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to read, create, and update NetSuite records through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified software, and the effects of automatic skill synchronization are not disclosed.

Mitigation: Review and install a verified CLI release; review synchronization behavior and disable it if unwanted.

Risk: NetSuite operations can change records accessible to the connected account.

Mitigation: Limit the account to needed records and review and confirm each exact write payload before execution.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [NetSuite API documentation](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/book_1559132836.html)
- [NetSuite](https://www.netsuite.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with oo CLI commands and JSON action payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches each action schema before use; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
