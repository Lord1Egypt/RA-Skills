## Description:

JustCall (justcall.io). Use this skill for ANY JustCall request — reading, creating, updating, and deleting data. Whenever a task involves JustCall, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

JustCall account users can retrieve contact and user records, create or update contacts, delete contacts, and manage suppression status through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run an online CLI installer before the installed version and bundled skills are verified.

Mitigation: Review and install a verified CLI version before enabling automatic setup, including any bundled skills it installs.

Risk: Contact changes, deletions, and suppression-list changes can alter or remove JustCall data.

Mitigation: Keep approval requirements for contact changes, deletions, and suppression-list changes; confirm the exact target and effect before execution.

## Reference(s):

- [JustCall homepage](https://justcall.io)
- [JustCall API documentation](https://developer.justcall.io/reference/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands, JSON connector requests and responses, and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations return JustCall records; state-changing actions require user approval as described in the skill.]

## Skill Version(s):

1.0.3 (source: server release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
