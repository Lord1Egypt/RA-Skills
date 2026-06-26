## Description: <br>
Generate high-quality technical HTML presentations (Reveal.js) and Markdown technical deep-dive articles from projects or papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RevolGMPHL](https://clawhub.ai/user/RevolGMPHL) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and technical communicators use this skill to convert technical projects or papers into Reveal.js HTML slide decks, Markdown deep-dive articles, and architecture diagrams grounded in source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated presentations may load scripts and styles from public CDNs when opened. <br>
Mitigation: Use offline or vendored Reveal.js, MathJax or KaTeX, highlight.js, and Mermaid assets in sensitive environments. <br>
Risk: Generated files may summarize private project content or contain inaccurate technical claims. <br>
Mitigation: Specify the desired output language and review generated HTML, Markdown, diagrams, and speaker notes before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RevolGMPHL/presentation-html-generator-skill) <br>
- [Publisher profile](https://clawhub.ai/user/RevolGMPHL) <br>
- [Article template](references/article-template.md) <br>
- [Matplotlib architecture diagram guide](references/matplotlib-guide.md) <br>
- [Prompt template](references/prompt-template.md) <br>
- [Reveal.js fixes](references/revealjs-fixes.md) <br>
- [Slide template](assets/slide-template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown, HTML, and code snippets for presentations, articles, diagrams, and speaker notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML presentations may reference public CDN assets unless the user vendors or replaces them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
