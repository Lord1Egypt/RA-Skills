## Description: <br>
Reads meeting minutes from local text files or URLs and lists local meeting-note directories so an agent can answer questions about decisions, action items, discussions, and file counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaocaijic](https://clawhub.ai/user/xiaocaijic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill to retrieve meeting-note content from a provided local path or URL, or to count and list meeting-note files in a local directory before answering meeting-related questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Windows folder-listing helper can turn a supplied folder path into unintended PowerShell commands. <br>
Mitigation: Review before installing on Windows, use only trusted meeting-note paths, and prefer a fixed version that uses Python-only file enumeration. <br>
Risk: Reading broad local directories or untrusted URLs can expose sensitive meeting content or internal resources. <br>
Mitigation: Provide only the specific meeting-note file, folder, or URL needed for the task and avoid broad sensitive directories or internal network URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaocaijic/meeting-minutes-retriever) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Guidance] <br>
**Output Format:** [Plain text or JSON from helper scripts, followed by concise Markdown answers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directory listings count supported .md and .txt meeting-note files; file reads return raw meeting text or human-readable ERROR messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
