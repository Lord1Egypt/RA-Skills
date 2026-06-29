## Description: <br>
Enforces markdown line-wrap and structure rules for clean git diffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation authors, and agents use this skill when writing or editing committed Markdown to apply consistent wrapping, heading spacing, list spacing, and link formatting for reviewable diffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the skill to be considered during general Markdown or documentation edits. <br>
Mitigation: Review activation terms before installation and confirm proposed edits before applying them in important repositories. <br>
Risk: Markdown reflow can change content that should remain exact, such as code blocks, tables, frontmatter, HTML blocks, link definitions, and image references. <br>
Mitigation: Preserve the documented exempt content types and review diffs for formatting-only changes before commit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-markdown-formatting) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Google Markdown style guide](https://google.github.io/styleguide/docguide/style.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown prose and edit guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies hybrid 80-character wrapping and structural Markdown formatting rules while preserving exempt content such as code blocks, tables, frontmatter, and link definitions.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
