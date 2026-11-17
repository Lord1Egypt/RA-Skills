## Description:

Generate full SEO articles using Kitful.ai from a keyword or topic, with Kitful researching, writing, and delivering a publication-ready article.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eashish93](https://clawhub.ai/user/eashish93)

### License/Terms of Use:


## Use Case:

External users and content teams use this skill to generate SEO-ready long-form articles from keywords, topics, audience notes, language preferences, and promotion settings. Developers can also use it for sequential batch article generation through the Kitful.ai API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article prompts, context, brand URLs, and workspace identifiers are sent to Kitful.ai for processing.

Mitigation: Use the skill only with content you intend Kitful.ai to process, and avoid sending secrets, private client details, or unpublished business information in prompts.

Risk: The skill requires a Kitful API key for article generation and export commands.

Mitigation: Keep the API key private, store it in the configured credential location or environment, and avoid pasting live keys into shared transcripts or files.

## Reference(s):

- [Kitful.ai](https://kitful.ai)
- [Kitful SEO Article Writer on ClawHub](https://clawhub.ai/eashish93/skills/kitful)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown status messages and shell commands for exporting generated articles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces article generation progress updates, dashboard links, and export commands; generated articles are downloaded as Markdown and HTML zip files.]

## Skill Version(s):

1.0.4 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
