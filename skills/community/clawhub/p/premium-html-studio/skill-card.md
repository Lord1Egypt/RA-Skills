## Description:

Generates polished single-file HTML technical documentation and proposals using international and Chinese technical-spec design systems with reusable CSS and SVG templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fbbyqsyea](https://clawhub.ai/user/fbbyqsyea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical writers use this skill to turn technical plans, architecture notes, research reports, and Chinese or English proposals into polished single-file HTML documents with diagrams, syntax highlighting, and responsive styling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documents can load remote scripts or fonts, which may be unsuitable for sensitive, offline, or authenticated content.

Mitigation: Review generated HTML before sharing; self-host or remove remote assets for sensitive use and pin dependencies with integrity checks when external assets remain.

Risk: The client-side search example uses unsafe HTML insertion.

Mitigation: Replace search-result innerHTML rendering with safe DOM construction before using the pattern in shared or hosted documents.

Risk: Generated technical docs or proposals may include incorrect or misleading guidance.

Mitigation: Have a qualified reviewer check the generated content and scan the final HTML before deployment or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fbbyqsyea/skills/premium-html-studio)
- [International CSS system](artifact/templates/css-system.css)
- [Chinese technical-spec CSS system](artifact/templates/css-system-cn.css)
- [Reusable SVG components](artifact/templates/svg-components.svg)
- [Prism.js CDN reference](https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js)
- [Mermaid CDN reference](https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js)
- [FlexSearch CDN reference](https://cdn.jsdelivr.net/npm/flexsearch@0.7.31/dist/flexsearch.bundle.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and SVG code blocks; final agent output is typically a single-file HTML document.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML may include optional CDN-loaded fonts/scripts and client-side search or diagram components.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
