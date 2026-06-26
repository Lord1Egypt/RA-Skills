## Description: <br>
Converts Markdown files and static-site Markdown content to HTML using workflows and examples for marked.js, Pandoc, gomarkdown, Jekyll, Hugo, and standard Markdown flavors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert Markdown into HTML for documentation, previews, generated files, and static-site workflows. It is suited for single-file conversions, batch conversion guidance, and Markdown features such as code blocks, tables, collapsed sections, and math expressions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted Markdown can produce unsafe HTML when rendered or published. <br>
Mitigation: Sanitize untrusted Markdown output before displaying it in a browser or publishing generated HTML. <br>
Risk: Optional package installs, converter commands, or theme setup commands may introduce dependency or execution risk. <br>
Mitigation: Review commands before running them and pin or trust third-party packages and themes before installation. <br>
Risk: Preview servers can expose local content if bound to a public or LAN-facing interface. <br>
Mitigation: Avoid binding preview servers to 0.0.0.0 unless LAN access is intentional. <br>


## Reference(s): <br>
- [Basic Markdown to HTML](references/basic-markdown-to-html.md) <br>
- [Code Blocks to HTML](references/code-blocks-to-html.md) <br>
- [Collapsed Sections to HTML](references/collapsed-sections-to-html.md) <br>
- [Mathematical Expressions to HTML](references/writing-mathematical-expressions-to-html.md) <br>
- [Tables to HTML](references/tables-to-html.md) <br>
- [marked.js](references/marked.md) <br>
- [Pandoc](references/pandoc.md) <br>
- [gomarkdown](references/gomarkdown.md) <br>
- [Jekyll](references/jekyll.md) <br>
- [Hugo](references/hugo.md) <br>
- [ClawHub release page](https://clawhub.ai/jhauga/markdown-to-html-converter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and HTML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces conversion guidance and example commands; does not execute conversion tools by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
