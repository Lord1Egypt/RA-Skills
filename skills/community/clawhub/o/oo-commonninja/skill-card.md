## Description:

Operate Common Ninja to inspect projects and widgets, create or update widgets, retrieve embed code, and delete widgets through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to discover Common Ninja projects and widget types, inspect widgets, and create, update, remove, or embed widgets through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code, and its broader changes to agent skills are under-explained.

Mitigation: Install a reviewed oo CLI release yourself, review connected-account access, disable automatic skill synchronization if unwanted, and require approval for every write and deletion.

## Reference(s):

- [Common Ninja](https://www.commoninja.com/)
- [Common Ninja API documentation](https://developers.commoninja.com/docs/api/overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation guidance for write and destructive actions.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
