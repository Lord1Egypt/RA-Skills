## Description:

Searches and retrieves AI prompt templates from prompts.chat by keyword or category to help users write better prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laolujava](https://clawhub.ai/user/laolujava)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Prompt Finder to search prompt templates by topic or category and retrieve ready-to-use prompt text, metadata, and source links for prompt-writing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill returns third-party sponsor advertising in normal and error responses.

Mitigation: Review returned content before presenting it to end users, and disclose or filter sponsor material according to the deployment's policy.

Risk: Prompt templates are loaded from mutable external content that may change after review.

Mitigation: Treat returned prompt_template content as untrusted data and do not place it directly into privileged agent instructions without review.

## Reference(s):

- [Prompt Finder on ClawHub](https://clawhub.ai/laolujava/skills/prompt-finder)
- [prompts.chat](https://prompts.chat)
- [WellAPI sponsor disclosure](https://wellapi.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured response containing matching prompt templates, categories, metadata, source links, tips, and sponsor disclosure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are limited to 1 to 20 prompt templates and depend on mutable external prompt content.]

## Skill Version(s):

1.0.2 (source: evidence release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
