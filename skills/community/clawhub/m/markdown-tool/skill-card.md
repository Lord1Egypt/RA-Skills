## Description: <br>
Convert Markdown text to HTML and other formats for documentation generation, content formatting, and text transformation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to convert Markdown files or piped Markdown text into HTML, generate tables of contents, and prepare formatted documentation output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML generated from untrusted Markdown should not be treated as sanitized. <br>
Mitigation: Review generated HTML before publishing or embedding it, and sanitize it with an approved HTML sanitizer when handling untrusted input. <br>
Risk: The documented feature claims may exceed the actual parser behavior. <br>
Mitigation: Test required Markdown constructs with representative files before relying on this skill for production documentation conversion. <br>
Risk: The documented command may require a wrapper in the runtime environment. <br>
Mitigation: Confirm the available entry point before use, such as invoking the bundled Python script directly when no command wrapper is installed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/markdown-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated HTML or text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write converted output to a requested local file or print it to standard output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
