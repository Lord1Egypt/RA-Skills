## Description:

Operate Statamic sites through an OOMOL-connected account, including listing, creating, updating, and deleting site licenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site administrators use this skill to inspect and manage Statamic site licenses through their connected Statamic account. They can list sites or create, update, and delete licenses using the documented connector actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs a remote CLI installer without prior review.

Mitigation: Review and verify the CLI installation separately before allowing it to run.

Risk: The CLI's broader skill-synchronization behavior and hosted connector implementation have not been verified.

Mitigation: Review the CLI's synchronization behavior and retain approval for site creation, updates, and deletion.

## Reference(s):

- [Statamic Sites API documentation](https://statamic.dev/advanced-topics/sites-api)
- [Statamic](https://statamic.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected Statamic account; site creation, updates, and deletion require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
