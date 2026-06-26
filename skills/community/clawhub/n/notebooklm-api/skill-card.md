## Description: <br>
Provides agent workflows for creating Google NotebookLM notebooks, adding sources, chatting with content, generating artifacts, and downloading outputs through notebooklm-py. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmanchu](https://clawhub.ai/user/lmanchu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate Google NotebookLM research, content analysis, and artifact generation from URLs, documents, and media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user prompts and local or sensitive documents to Google NotebookLM under broad activation rules. <br>
Mitigation: Prefer explicit /notebooklm activation and require confirmation before uploading local or sensitive documents. <br>
Risk: NotebookLM authentication material can expose access to a user's Google NotebookLM account if logged or shared. <br>
Mitigation: Keep NOTEBOOKLM_AUTH_JSON out of logs and chat transcripts, and use a dedicated NOTEBOOKLM_HOME or account for automation. <br>
Risk: Parallel agents can overwrite shared NotebookLM context and operate on the wrong notebook. <br>
Mitigation: Use explicit notebook IDs or separate NOTEBOOKLM_HOME directories for parallel workflows. <br>


## Reference(s): <br>
- [NotebookLM API Skill Page](https://clawhub.ai/lmanchu/notebooklm-api) <br>
- [lmanchu Publisher Profile](https://clawhub.ai/user/lmanchu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide agents to create notebooks, upload sources, ask questions, generate NotebookLM artifacts, and download outputs in formats such as Markdown, JSON, CSV, HTML, PDF, PNG, MP3, and MP4.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata and artifact comment) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
