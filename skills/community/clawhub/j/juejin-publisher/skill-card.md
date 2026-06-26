## Description: <br>
Juejin Publisher publishes Markdown articles to the Juejin platform through Cookie-authenticated Juejin APIs, with support for categories, tags, summaries, and cover images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devilWwj](https://clawhub.ai/user/devilWwj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to publish Markdown articles to Juejin from an agent-assisted workflow or command line. It helps prepare article metadata, create drafts, and optionally publish after the user reviews the target category, tags, summary, and publication mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Juejin browser Cookie that can authorize actions on the user's Juejin account. <br>
Mitigation: Keep juejin.env private, avoid committing or sharing the Cookie, and rotate the Cookie if it is exposed. <br>
Risk: A normal run can publish content publicly to the configured Juejin account. <br>
Mitigation: Use --draft-only when review is needed before public publication, and verify the title, summary, category, tags, and cover image before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devilWwj/juejin-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/devilWwj) <br>
- [Juejin](https://juejin.cn) <br>
- [Juejin category IDs reference](artifact/references/category_ids.md) <br>
- [Juejin tag IDs reference](artifact/references/tag_ids.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Juejin publication links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a Juejin draft link or published article link depending on --draft-only and user configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter and _meta.json report 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
