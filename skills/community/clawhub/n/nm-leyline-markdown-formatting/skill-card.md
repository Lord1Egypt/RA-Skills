## Description: <br>
Enforces markdown line-wrap and structure rules for clean git diffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation authors use this skill to write, review, and revise committed Markdown with consistent 80-character wrapping, heading spacing, list spacing, and link formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad documentation or formatting triggers may lead to large Markdown edits. <br>
Mitigation: Review the skill's suggestions before applying large repo-wide documentation changes. <br>
Risk: Incorrect reflow can make documentation harder to review or alter protected Markdown structures. <br>
Mitigation: Keep code blocks, tables, frontmatter, HTML blocks, link definitions, and image lines exempt from wrapping as described by the artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-markdown-formatting) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Hybrid Line Wrapping Rules](modules/wrapping-rules.md) <br>
- [Google Markdown style guide](https://google.github.io/styleguide/docguide/style.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and edited Markdown prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on prose formatting; code blocks, tables, headings, frontmatter, HTML blocks, link definitions, and image lines are exempt from wrapping.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
