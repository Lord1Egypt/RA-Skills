## Description:

Use Saperly through an OOMOL-connected account to read and manage workspace data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read Saperly workspace data and manage calls, messages, connections, numbers, keys, and other workspace resources through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup runs downloaded installer code, and the remote installers could not be inspected.

Mitigation: Review setup before installing, use a verified CLI release, and approve CLI and any additional skill installations separately.

Risk: The skill includes actions that can change or delete Saperly data and workspace resources.

Mitigation: Connect only the permissions needed and confirm the exact effect of calls, messages, key changes, and destructive actions before running them.

## Reference(s):

- [Saperly](https://saperly.com)
- [Saperly API documentation](https://saperly.com/docs/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Text and JSON returned through the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read workspace data and perform user-approved state-changing actions.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
