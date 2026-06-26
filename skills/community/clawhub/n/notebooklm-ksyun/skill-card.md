## Description: <br>
Complete Google NotebookLM integration for adding sources, asking questions, generating Studio content, downloading artifacts, and managing notebooks programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinzien1107-ctrl](https://clawhub.ai/user/kevinzien1107-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate NotebookLM research workflows, including source import, cited Q&A, notebook management, and generation of podcasts, videos, slide decks, quizzes, flashcards, infographics, mind maps, data tables, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls NotebookLM through an unofficial client that uses undocumented Google APIs and may break without notice. <br>
Mitigation: Confirm the client is intentionally allowed for the workflow, validate authentication with diagnostic commands, and fall back to manual review if API behavior changes. <br>
Risk: The skill requires sensitive Google session access and can import, export, share, delete, or download user content. <br>
Mitigation: Use a dedicated low-privilege Google account or isolated browser profile, avoid primary-account cookies, review source and Drive content before import, and require explicit confirmation before sharing, exporting, deleting, or uploading sensitive material. <br>
Risk: NotebookLM content generation can be long-running, rate-limited, or fail after partially completed work. <br>
Mitigation: Use non-blocking generation for long tasks, monitor artifact status, retry after rate limits, and ask the user whether to retry, skip, or investigate failures. <br>
Risk: Shared active-notebook state can be unsafe in parallel agent workflows. <br>
Mitigation: Pass notebook IDs directly with commands or isolate each agent with its own NotebookLM profile or home directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevinzien1107-ctrl/notebooklm-ksyun) <br>
- [Publisher Profile](https://clawhub.ai/user/kevinzien1107-ctrl) <br>
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) <br>
- [notebooklm-py Troubleshooting](https://github.com/teng-lin/notebooklm-py/blob/main/docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create, download, export, or share NotebookLM artifacts such as MP3, MP4, PDF, PPTX, JSON, Markdown, HTML, PNG, and CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
