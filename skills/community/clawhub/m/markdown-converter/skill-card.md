## Description: <br>
Convert PDF, Office, web/data, media, archive, YouTube, and EPub inputs to Markdown using markitdown for LLM processing or text analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to convert source documents and data files into Markdown for LLM processing, text analysis, or downstream editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive documents may be sent to Azure Document Intelligence when the cloud extraction option is used. <br>
Mitigation: Use local conversion for sensitive files when possible and enable Azure Document Intelligence only for documents approved for that provider. <br>
Risk: Third-party plugins can change conversion behavior or add supply-chain exposure. <br>
Mitigation: Enable --use-plugins only for reviewed plugins and pin or review the markitdown package source when supply-chain control matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/markdown-converter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Markdown to stdout or a file when the proposed markitdown commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
