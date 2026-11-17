## Description:

Optimize technical articles for the Juejin community: improve rankings, readability, and developer engagement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevRel teams, and technical authors use this skill to diagnose and optimize Juejin-targeted technical drafts, titles, SEO tags, article structure, and publishing strategy while retaining final publishing control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated promotional language or publishing advice could be unsuitable for a final Juejin post.

Mitigation: Keep final publishing under user control and review titles, tags, cross-promotion snippets, and engagement prompts before use.

Risk: JSON output could be unsafe or malformed if passed directly into downstream automation.

Mitigation: Re-serialize or strictly validate script output against the provided output schema before automated use.

Risk: Juejin-oriented, Chinese-market recommendations may not fit other publishing platforms or audiences.

Mitigation: Use the skill for Juejin-focused optimization and review recommendations against the target audience and venue.

## Reference(s):

- [Category Benchmarks](artifact/references/category_benchmarks.json)
- [Input Schema](artifact/schemas/input.schema.json)
- [Output Schema](artifact/schemas/output.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/juejin-article-optimizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and optimized article drafts, with optional JSON from the CLI script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic scores, title variants, SEO recommendations, publishing strategy, warnings, and improved code block guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
