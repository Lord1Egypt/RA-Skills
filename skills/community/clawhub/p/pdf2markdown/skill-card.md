## Description: <br>
Converts PDF and image documents to clean Markdown through the PDF2Markdown CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QThans](https://clawhub.ai/user/QThans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert PDFs and common image formats into Markdown or JSON, including larger documents handled through asynchronous parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or URLs may be sent to the PDF2Markdown service. <br>
Mitigation: Use the skill only for user-requested documents that are appropriate to share with the service, and review organizational data-handling requirements before parsing sensitive files. <br>
Risk: API keys or credentials may be exposed through shell history, logs, or chat if pasted directly. <br>
Mitigation: Use interactive login or a secret manager, avoid logging PDF2MARKDOWN_API_KEY, and do not paste real API keys into conversations. <br>
Risk: Setup commands can modify multiple agent environments, and unpinned npx execution may install unexpected package versions. <br>
Mitigation: Prefer manual installation or single-agent setup for routine use, and pin or review the CLI package before installation in managed environments. <br>
Risk: Parsed document content can be sensitive or untrusted and may be too large for direct agent context handling. <br>
Mitigation: Write outputs to .pdf2markdown/, keep that directory gitignored, and inspect large outputs incrementally with targeted reads. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/QThans/pdf2markdown) <br>
- [PDF2Markdown API Docs](https://pdf2markdown.io/docs) <br>
- [pdf2markdown-cli package](https://www.npmjs.com/package/pdf2markdown-cli) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and optional Markdown or JSON conversion outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are typically written under .pdf2markdown/; synchronous parsing is documented for files under about 30MB and asynchronous parsing for files up to 100MB.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
