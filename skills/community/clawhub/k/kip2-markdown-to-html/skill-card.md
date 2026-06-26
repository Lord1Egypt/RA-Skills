## Description: <br>
Convert a Markdown file or raw Markdown string into a polished HTML document with custom Pandoc templates, custom CSS, and built-in HTML themes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mutour](https://clawhub.ai/user/mutour) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to convert Markdown files or raw Markdown strings into standalone HTML pages with selected templates, CSS, tables of contents, section numbering, metadata, and embedded assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted Markdown, templates, CSS, or metadata can affect the generated HTML content and presentation. <br>
Mitigation: Use trusted inputs for templates, CSS, and metadata, and review the generated HTML before publishing or sharing it. <br>
Risk: Broad resource paths or embedded assets can include referenced local files in the generated HTML output. <br>
Mitigation: Keep resource paths narrow and inspect referenced assets before using embedded-output options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mutour/kip2-markdown-to-html) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Sample Markdown input](artifact/assets/examples/sample.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifact is standalone HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pandoc on PATH; supports custom templates, CSS files, metadata, table of contents, section numbering, and embedded assets.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
