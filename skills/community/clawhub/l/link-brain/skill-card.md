## Description:

Local knowledge base for links. Save URLs with summaries and tags, search later using natural language, build collections, and review your backlog with spaced repetition. Includes a standalone HTML graph view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakes420](https://clawhub.ai/user/jakes420)

### License/Terms of Use:


## Use Case:

Developers and external users use Link Brain to maintain a local bookmark knowledge base: save and import URLs, summarize and tag them, search later, build collections, and review saved links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-save can read local, localhost, private-network, or attacker-supplied URLs.

Mitigation: Avoid using auto-save with file://, localhost, private-network, or untrusted URLs; review URLs before fetching content.

Risk: Imported bookmark data can become executable script in generated GUI or graph HTML views.

Mitigation: Avoid opening generated HTML views after importing untrusted bookmark exports until URL validation and HTML escaping are fixed.

Risk: The skill reads and stores browser bookmarks in ~/.link-brain.

Mitigation: Install and run it only when local bookmark access and on-disk storage are acceptable for the user or environment.

## Reference(s):

- [Link Brain usage examples](references/examples.md)
- [Link Brain v4.0.0 release notes](references/v4.0.0-release-notes.md)
- [ClawHub skill page](https://clawhub.ai/jakes420/skills/link-brain)
- [Publisher profile](https://clawhub.ai/user/jakes420)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, Markdown, Configuration]

**Output Format:** [Markdown guidance with CLI commands; command results may include text, JSON, Markdown, or standalone HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local data in ~/.link-brain by default; auto-save fetches the target URL only when explicitly used.]

## Skill Version(s):

4.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
