## Description:

Raindrop.io (raindrop.io). Use this skill for ANY Raindrop.io request — reading, creating, updating, and deleting data. Whenever a task involves Raindrop.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Raindrop.io can ask the agent to find and read bookmarks, manage collections and tags, or create, update, and delete saved items through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute downloaded code whose contents have not been verified.

Mitigation: Review and explicitly approve CLI installation and updates, including any installation or update of other agent skills, before allowing automatic setup.

Risk: Connecting Raindrop.io gives OOMOL access to the connected account.

Mitigation: Connect only an account the user intends to make available to the skill.

Risk: Bookmark and collection writes or deletions can change or remove user data.

Mitigation: Confirm the exact action and target with the user before writes or destructive actions.

## Reference(s):

- [Raindrop.io](https://raindrop.io)
- [Raindrop.io API documentation](https://developer.raindrop.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and oo CLI commands with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Raindrop.io data; writes and deletions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
