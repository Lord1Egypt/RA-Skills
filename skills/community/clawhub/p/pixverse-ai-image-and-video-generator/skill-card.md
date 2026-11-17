## Description:

PixVerse CLI - generate AI videos and images from the command line with PixVerse video and image models, third-party model options, and PixVerse effect templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pixverse-official](https://clawhub.ai/user/pixverse-official)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, AI agents, and creative automation teams use this skill to generate and edit PixVerse images and videos from the command line, manage assets and workspaces, and run repeatable media-production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install or run an external PixVerse npm CLI that may change over time.

Mitigation: Use a pinned and verified PixVerse CLI version from a trusted package source before running generated commands.

Risk: PixVerse authentication uses account tokens and generated media may be uploaded to cloud services.

Mitigation: Avoid uploading sensitive local media, keep tokens protected, and re-check authentication state before automated workflows.

Risk: Commands can consume paid credits or affect team workspace assets.

Mitigation: Check account credits and the active workspace before generation, deletion, or batch operations, and confirm asset IDs before destructive commands.

## Reference(s):

- [PixVerse homepage](https://pixverse.ai)
- [PixVerse web app](https://app.pixverse.ai)
- [Mondo Poster Artist Styles Reference](references/mondo-poster/artist-styles.md)
- [Mondo Poster Composition Patterns Reference](references/mondo-poster/composition-patterns.md)
- [Mondo Poster Genre Templates Reference](references/mondo-poster/genre-templates.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commands commonly use PixVerse CLI JSON mode for machine-readable stdout.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
