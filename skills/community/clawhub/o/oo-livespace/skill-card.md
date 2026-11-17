## Description:

Connects to Livespace through an OOMOL-connected account to read, create, update, and delete CRM records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators can use this skill to look up and manage Livespace companies, deals, people, and tasks through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback runs installer scripts fetched from the internet whose contents and effects were not verified.

Mitigation: Review the setup fallback before installing. Use an independently reviewed, version-pinned CLI and require approval before running an installer.

Risk: Write and destructive actions can change or remove Livespace records.

Mitigation: Keep the skill's confirmation steps: confirm the exact payload and effect before writes, and confirm the target and obtain explicit approval before deletions.

## Reference(s):

- [Livespace homepage](https://www.livespace.io/)
- [Livespace API documentation](https://support.livespace.io/en/articles/3572069-api-documentation-and-information)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-livespace)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON connector responses with text summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
