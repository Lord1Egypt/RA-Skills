## Description: <br>
Converts Markdown notes into readable offline HTML pages with a fixed left-side table of contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanxu98](https://clawhub.ai/user/seanxu98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, students, and technical writers use this skill to convert Markdown notes or documentation into navigable static HTML with heading navigation, syntax highlighting, math rendering, and Mermaid diagram support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML from untrusted Markdown may execute browser-side content when opened. <br>
Mitigation: Only convert and open Markdown from trusted sources, or inspect the generated HTML before viewing it in a browser. <br>
Risk: Running the converter with an output path can overwrite an existing file. <br>
Mitigation: Review the output path before execution and choose a new filename when preserving existing HTML is important. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanxu98/md-to-html) <br>
- [Publisher profile](https://clawhub.ai/user/seanxu98) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Python shell commands that produce an HTML file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated HTML embeds offline JavaScript and CSS assets for table-of-contents navigation, syntax highlighting, KaTeX math rendering, and Mermaid diagrams.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
