## Description:

ablefy (ablefy.io). Use this skill for ANY ablefy request — searching and reading data. Whenever a task involves ablefy, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected ablefy account can retrieve account details, products, and pricing plans. The skill guides an agent to inspect each action's schema and return the resulting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded CLI software without first obtaining approval, and the remote installer's full effects remain unverified.

Mitigation: Review and approve CLI installation separately using a verified release. Check whether it installs additional agent skills; the upstream command reference documents OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: Connecting ablefy entrusts OOMOL with access to the connected account.

Mitigation: Connect only the ablefy account the user intends to make available to OOMOL.

## Reference(s):

- [ablefy](https://ablefy.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference: skill synchronization setting](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON data with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results depend on the connected ablefy account and available data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
