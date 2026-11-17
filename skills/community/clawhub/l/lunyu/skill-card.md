## Description:

Captures user-approved quotes, reflections, jokes, and personal insights into a local personal quote archive with categories, search, daily recall, and Markdown export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyxin-del](https://clawhub.ai/user/joeyxin-del)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agent users use this skill to preserve memorable personal sayings, organize them by chapter, tag, and type, search the archive, receive daily or random recalls, and export a compiled Markdown quote collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved quotes may contain sensitive personal thoughts or third-party information and are stored in plaintext under ~/.hermes/lunyu/.

Mitigation: Avoid saving passwords, private third-party statements, financial or health details, and intimate content unless plaintext local storage is acceptable.

Risk: Daily, random, or exported quote features may resurface private entries outside the original context.

Mitigation: Review entries before exporting the compiled Markdown file or enabling scheduled daily push behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyxin-del/skills/lunyu)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown responses, command-style guidance, JSON-backed quote entries, and exported Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes local plaintext storage under ~/.hermes/lunyu/ and optional daily or random resurfacing of saved entries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
