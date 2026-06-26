## Description: <br>
Parses supported document files or URLs with `miaoda-studio-cli doc-parse` and converts extracted content to Markdown or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnycdb](https://clawhub.ai/user/johnnycdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract readable content from local or downloadable documents, including PDF, Word, PowerPoint, Excel, CSV, text, Markdown, and HTML files. It is useful when document content should be converted to Markdown for reading or to JSON for structured processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsed files and URLs may contain confidential, internal, access-controlled, or otherwise sensitive content. <br>
Mitigation: Use the skill only on documents and URLs the user is authorized to process, and install it only if the user trusts `miaoda-studio-cli` and the Miaoda/IDP document parser. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/johnnycdb/miaoda-doc-parse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and optional JSON output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides use of `--file` for local paths or URLs and `--output text/json` for response format selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
