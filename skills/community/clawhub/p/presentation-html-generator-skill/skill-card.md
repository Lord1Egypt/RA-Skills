## Description:

Generates Reveal.js HTML presentations, Markdown technical deep-dive articles, and matplotlib architecture diagrams from technical projects or papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[revolgmphl](https://clawhub.ai/user/revolgmphl)

### License/Terms of Use:


## Use Case:

Developers, engineers, and technical writers use this skill to turn project or paper evidence into Chinese-first Reveal.js slide decks, Markdown deep-dive articles, and architecture diagrams for technical review or education.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated slide decks may fetch third-party JavaScript and CSS from CDNs when opened.

Mitigation: For confidential or high-assurance presentations, pin exact dependency versions, add integrity checks, or vendor browser libraries locally.

Risk: The skill inspects project or paper files supplied for summarization, which may include confidential material.

Mitigation: Limit inputs to approved materials and review generated presentations or articles before sharing.

Risk: The skill produces Chinese content by default, which may not match every audience or review workflow.

Mitigation: Specify the required output language in the user request and review the generated text for audience fit.

## Reference(s):

- [Article Template](references/article-template.md)
- [Matplotlib Architecture Diagram Guide](references/matplotlib-guide.md)
- [Prompt Template](references/prompt-template.md)
- [Reveal.js Fixes](references/revealjs-fixes.md)
- [Slide Template](assets/slide-template.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance and single-file HTML code, optionally with bash or Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese output by default; generated HTML may reference CDN-hosted Reveal.js, Mermaid, MathJax, and highlight.js.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
