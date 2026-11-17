## Description:

Operate Ongage through a connected OOMOL account to inspect lists and contacts, create or update contacts, and change contact status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents managing an Ongage account use this skill to inspect lists and contacts, and to create, update, or change contact status through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial CLI setup may execute unverified installer code and synchronize broader agent changes.

Mitigation: Install the CLI from a verified source and review its automatic skill synchronization before first use.

Risk: Ongage data passes through the connected OOMOL account, and account scope can affect data changes.

Mitigation: Connect only the intended account and retain the documented approval checks for contact updates and destructive status changes.

## Reference(s):

- [Ongage](https://www.ongage.com/)
- [Ongage API FAQ](https://ongage.atlassian.net/wiki/spaces/HELP/pages/70418454/API+FAQ)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON action responses and concise text summaries, with oo CLI commands for requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the selected Ongage action. Contact updates and status changes follow the skill's approval guidance.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
