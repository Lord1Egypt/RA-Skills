## Description:

Multi-stage journalism agent for OpenClaw that researches, drafts, and edits publication-quality articles and assembles mixed newsletters combining original articles and curated event or marketplace listings with images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[defineagain](https://clawhub.ai/user/defineagain)

### License/Terms of Use:

MIT-0

## Use Case:

External users, editorial teams, and developers use this skill to research publication topics, draft sourced longform articles, curate event or marketplace listings, and assemble mixed newsletters with images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The newsletter assembly script uses shared temporary paths, which can mix content across runs or users in a shared workspace.

Mitigation: Use the skill only in a trusted workspace, avoid elevated privileges, and clear or isolate newsletter part files before assembly.

Risk: Generated newsletter HTML can include unescaped content and external image URLs.

Mitigation: Inspect and sanitize generated HTML, links, image URLs, captions, and credits before sending newsletters to real recipients.

Risk: Research topics, drafts, and newsletter plans may contain embargoed or private editorial information.

Mitigation: Avoid sensitive inputs unless the workspace and downstream services are approved for that material.

## Reference(s):

- [Source Quality Guide](references/source-quality.md)
- [NK Images Search API](https://nkimages.com/api/public/images?source=clawhub&q={query}&per_page=6)
- [NK Images Generation Quota API](https://nkimages.com/api/public/generate/quota)
- [NK Images Anonymous Generation API](https://nkimages.com/api/public/generate/anonymous)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles with YAML frontmatter, HTML newsletter documents, inline source citations, image captions, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article mode targets 800-1200 words; newsletter mode assembles feature articles, listings, images, captions, credits, and source links.]

## Skill Version(s):

1.0.1 (source: server release evidence, created 2026-04-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
