## Description: <br>
Combine high-quality Markdown to HTML rendering with robust HTML to Markdown extraction in one skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[520xiaomumu](https://clawhub.ai/user/520xiaomumu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content engineers use this skill to convert Markdown into presentable standalone HTML and to extract clean Markdown from HTML files, raw HTML, URLs, or batches of documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch URLs and read or write selected local paths during conversion. <br>
Mitigation: Use explicit input and output paths, fetch only intended URLs, and avoid broad private directories in batch mode. <br>
Risk: Generated HTML from untrusted Markdown or HTML may contain content that is unsafe to publish or open without review. <br>
Mitigation: Review generated HTML before publishing or sharing it, especially when the source content is untrusted. <br>
Risk: The Node conversion path depends on npm packages. <br>
Mitigation: Install dependencies from the included lockfile and review dependency updates before use. <br>


## Reference(s): <br>
- [Conversion profiles reference](references/profiles.md) <br>
- [ClawHub skill page](https://clawhub.ai/520xiaomumu/html-markdown-hybrid) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; conversion scripts produce Markdown, HTML, JSON reports, and frontmatter metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on selected conversion direction, profile, theme, input path or URL, and output path.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
