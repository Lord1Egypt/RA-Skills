## Description:

Use the oo CLI to read and manage esa posts, comments, teams, and categories through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to work with esa content through their OOMOL-connected account, including reading and changing posts and comments and browsing team information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The esa workflow requires approval for changes, while the required CLI may also install other agent skills through broader startup behavior; actual installer contents and hosted execution were not verified.

Mitigation: Use a verified oo CLI release and review its installation behavior. Set OO_SKILLS_SYNC_DISABLED=1 for subsequent invocations if you want to prevent startup skill synchronization.

## Reference(s):

- [esa API documentation](https://docs.esa.io/posts/102)
- [esa](https://esa.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API calls, Markdown, text]

**Output Format:** [JSON action requests and results; esa post and comment content may be Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions marked write or destructive can change esa data; the skill requires confirmation before running them.]

## Skill Version(s):

1.0.6 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
