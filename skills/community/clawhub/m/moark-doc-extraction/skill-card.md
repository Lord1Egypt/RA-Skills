## Description: <br>
Extract and recognize text from documents, including PDF and DOCX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fchange](https://clawhub.ai/user/fchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract OCR and text from PDF and DOCX documents through a bundled command-line script. It submits selected local files or URLs to Gitee AI and returns the extracted content as concise Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents and embedded images are sent to Gitee AI for processing. <br>
Mitigation: Process only documents that are approved for that provider and avoid confidential, regulated, proprietary, or third-party content unless the use case has explicit approval. <br>
Risk: The script accepts document URLs as input, which can involve untrusted or internal URLs. <br>
Mitigation: Prefer local file paths and avoid internal or untrusted URLs unless the source and destination are approved. <br>
Risk: The skill requires a GITEEAI_API_KEY for external API access. <br>
Mitigation: Use a dedicated API key with appropriate access, keep it local, and rotate or revoke it when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fchange/moark-doc-extraction) <br>
- [Publisher Profile](https://clawhub.ai/user/fchange) <br>
- [Gitee AI Document Parse Endpoint](https://ai.gitee.com/v1/async/documents/parse) <br>
- [Gitee AI Task Status Endpoint](https://ai.gitee.com/v1/task/{task_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with extracted document content and optional shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITEEAI_API_KEY and sends selected documents, including embedded images when present, to Gitee AI for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
