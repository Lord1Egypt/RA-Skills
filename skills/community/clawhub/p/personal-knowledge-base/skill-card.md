## Description: <br>
Personal Knowledge Base helps users create document knowledge bases, import supported files, vectorize content, retrieve relevant chunks, answer questions, and manage stored files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nancyzhong2024](https://clawhub.ai/user/nancyzhong2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to organize personal documents into named knowledge bases, search indexed content, and answer questions with retrieved source excerpts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported document text, retrieved excerpts, and user questions may be sent to ZhipuAI for embeddings or answers. <br>
Mitigation: Use the skill only with documents and questions whose data flow to ZhipuAI is acceptable; avoid confidential, regulated, or proprietary files unless approved. <br>
Risk: Update and delete operations can permanently remove stored source files or indexed chunks from a knowledge base. <br>
Mitigation: Double-check knowledge-base and file names before update or delete actions and keep backups for important source documents. <br>
Risk: API keys can be exposed if stored directly in the configuration file. <br>
Mitigation: Prefer the ZHIPUAI_API_KEY environment variable instead of writing the key into config.txt. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nancyzhong2024/personal-knowledge-base) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with optional Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return knowledge-base names, file lists, retrieved text chunks, generated answers, source file references, and operation status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
