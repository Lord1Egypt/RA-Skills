## Description: <br>
Publish blog posts to Medium via GitHub Pages and URL import without requiring a Medium API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylnhari](https://clawhub.ai/user/ylnhari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a requested topic, outline, or draft into a Medium-ready draft. The workflow creates constrained HTML, publishes it through the user's GitHub Pages staging repo, imports it into Medium, and stops for human review before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft content is published to a public GitHub Pages staging repo before Medium import. <br>
Mitigation: Use only content that is safe to make public, confirm the target GitHub owner and repo, and review the Medium draft before publishing. <br>
Risk: The skill can reuse a remembered blog repository from prior setup. <br>
Mitigation: Confirm or override the GitHub owner and repository when the destination matters, especially for broad blog-writing prompts. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ylnhari/skills/medium-blog-post-creator) <br>
- [HTML standards for Medium importer](references/html-standards.md) <br>
- [Persistent configuration](references/configuration.md) <br>
- [GitHub CLI](https://cli.github.com) <br>
- [Medium URL import](https://medium.com/p/import) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates public GitHub Pages draft artifacts and a Medium draft URL for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
