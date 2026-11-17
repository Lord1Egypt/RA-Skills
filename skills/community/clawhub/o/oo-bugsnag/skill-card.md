## Description:

Bugsnag (bugsnag.com). Use this skill for ANY Bugsnag request — searching and reading data. Whenever a task involves Bugsnag, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to search and read Bugsnag organizations, projects, errors, events, and releases through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup path can execute downloaded code without a clear user approval step.

Mitigation: Review and approve CLI setup separately before installation, prefer a verified pinned release, and check whether setup installs or synchronizes additional agent skills.

Risk: The connected service handles Bugsnag access and diagnostic data.

Mitigation: Confirm that OOMOL is approved to handle the account's Bugsnag access and diagnostic data.

## Reference(s):

- [Bugsnag](https://www.bugsnag.com)
- [Bugsnag API documentation](https://bugsnagapiv2.docs.apiary.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Bugsnag skill release](https://clawhub.ai/oomol/skills/oo-bugsnag)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured Bugsnag data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Bugsnag account's access.]

## Skill Version(s):

1.0.5 (source: skill frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
