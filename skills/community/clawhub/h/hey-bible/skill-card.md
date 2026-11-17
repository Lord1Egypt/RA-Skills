## Description:

Look up, search, and cross-reference Bible verses and Scripture via the Hey Bible API, including authorized access to saved favorites, notes, verse images, and chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hey-bible](https://clawhub.ai/user/hey-bible)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve Scripture passages, compare translations, and access authorized Hey Bible saved data through the Hey Bible API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm CLI execution can run changed package code with access to HEY_BIBLE_API_KEY and private Hey Bible account data.

Mitigation: Install and review a pinned version of @hey-bible/cli before use, and avoid ad hoc npx execution for sensitive account access.

Risk: The skill can read saved favorites, notes, image metadata or signed URLs, chats, and tags from the user's Hey Bible account.

Mitigation: Expose only the required Hey Bible API key, confirm user intent before saved-data commands, and avoid sharing private outputs outside the authorized session.

Risk: Verse searches may be saved to the user's Hey Bible account.

Mitigation: Tell users when a lookup can affect account history and confirm before running searches where that side effect matters.

## Reference(s):

- [Hey Bible API reference](references/api-reference.md)
- [Hey Bible API documentation](https://docs.heybible.app)
- [Hey Bible homepage](https://heybible.app)
- [@hey-bible/cli npm package](https://www.npmjs.com/package/@hey-bible/cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON returned by the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verse content may include HTML verse markers that should be stripped before presenting text to users.]

## Skill Version(s):

1.0.0 (source: evidence release, frontmatter, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
