## Description: <br>
Capture, summarize, and organize knowledge from URLs, YouTube videos, documents, and files. Proactively recall stored knowledge when relevant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plc](https://clawhub.ai/user/plc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to build and maintain an agent-managed personal knowledge base, capture source material, generate summaries, organize categories, and recall stored knowledge when it is relevant to later work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and later recall local knowledge, which may expose sensitive documents or secrets if they are added to the knowledge base. <br>
Mitigation: Use a dedicated non-sensitive knowledge-base folder and avoid adding secrets or private documents. <br>
Risk: Import, sorting, and reorganization workflows can create or move local files and update persistent memory. <br>
Mitigation: Review proposed imports and reorganizations before approving changes. <br>
Risk: Git integration can commit knowledge-base contents and may sync them elsewhere if a remote is configured and pushed. <br>
Mitigation: Only configure or push a git remote when the user intentionally wants the knowledge base synced. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/plc/knowledge-brain) <br>
- [Publisher profile](https://clawhub.ai/user/plc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and concise agent guidance, with shell commands used for local file, transcript, and git operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local knowledge-base directory, category index, changelog entries, and optional git commits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
