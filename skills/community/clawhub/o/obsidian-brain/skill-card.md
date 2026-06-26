## Description: <br>
Obsidian Brain guides an agent to read and write durable Obsidian-backed memory fragments before and after tasks using layered retrieval and concise Markdown records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realpda](https://clawhub.ai/user/realpda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and developers use this skill to maintain cross-session task memory in an Obsidian vault. It helps the agent recall relevant fragments at task start, write concise findings at task end, and distinguish Obsidian-backed fragments from system memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory fragments may capture secrets, personal data, or sensitive project details. <br>
Mitigation: Restrict the memory folder, require confirmation before writes, review saved notes, and avoid storing secrets or personal data. <br>
Risk: Recalled memory may be surfaced or injected without clear user approval and can influence future work. <br>
Mitigation: Show a concise read summary, let the user reject irrelevant fragments, and validate relevance before using recalled memory. <br>
Risk: The artifact instructs publishing a new ClawHub version when the skill is edited. <br>
Mitigation: Do not allow any ClawHub publish action unless the user explicitly requests it and reviews the release. <br>


## Reference(s): <br>
- [System Memory vs Agent Memory Fragments](references/storage-distinction.md) <br>
- [ClawHub skill page](https://clawhub.ai/realpda/obsidian-brain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and Obsidian memory fragment structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce durable Markdown memory fragments in an Obsidian vault when the agent is allowed to write files.] <br>

## Skill Version(s): <br>
1.7.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
