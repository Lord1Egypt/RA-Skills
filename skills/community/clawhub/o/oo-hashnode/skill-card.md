## Description:

Read and manage Hashnode publications and posts through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams can use this skill to read, create, publish, update, or delete Hashnode posts and drafts in a connected publication. Write and destructive actions require confirmation of the exact effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup automatically executes downloaded oo CLI installation code that has not been verified.

Mitigation: Review and verify the CLI installer before enabling fallback setup, and check the CLI's automatic skill synchronization settings.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Hashnode API documentation](https://github.com/Hashnode/gql-skill)
- [Hashnode](https://hashnode.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Markdown]

**Output Format:** [oo CLI commands and Hashnode connector results in JSON; post content may include Markdown and HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
