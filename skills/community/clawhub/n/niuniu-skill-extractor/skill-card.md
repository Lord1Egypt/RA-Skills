## Description: <br>
Extracts reusable skill documents from completed complex tasks, stores them locally, and helps agents search or suggest them for similar future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[livangy](https://clawhub.ai/user/livangy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill after multi-step tasks to identify repeatable workflows, generate standardized skill Markdown, and search locally saved skills when similar tasks recur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills may preserve private task details, credentials, or misleading workflow guidance if saved without review. <br>
Mitigation: Review every generated skill before saving, remove secrets or private data, and scan saved skill files before reuse. <br>
Risk: The skill creates local files and a local SQLite search index under the user's OpenClaw workspace. <br>
Mitigation: Install only when local searchable workflow memory is desired and manage the workspace with normal file-permission and retention controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/livangy/niuniu-skill-extractor) <br>
- [Publisher Profile](https://clawhub.ai/user/livangy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated skill files and search indexes are stored in the user's local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
