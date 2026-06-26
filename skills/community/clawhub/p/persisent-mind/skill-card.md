## Description: <br>
Provides persistent, searchable, context-aware memory storage for AI agents to retain user preferences, corrections, and project context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vedantsingh60](https://clawhub.ai/user/vedantsingh60) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to give AI agents durable local memory for user preferences, project facts, recurring procedures, and corrections that can be searched or injected into prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories may include secrets or sensitive information that can later be injected into prompts or exported. <br>
Mitigation: Do not store passwords, API keys, tokens, private personal data, confidential business details, or secret locations; review context returned by get_context() before sending it to a model. <br>
Risk: Imported or exported memory JSON may carry sensitive or misleading context. <br>
Mitigation: Treat memory JSON as sensitive and untrusted until reviewed, especially before importing it into a durable local memory store. <br>


## Reference(s): <br>
- [Persistent Mind on ClawHub](https://clawhub.ai/vedantsingh60/persisent-mind) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [LICENSE.md](artifact/LICENSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code] <br>
**Output Format:** [Markdown-formatted memory context, Python API results, and JSON memory exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memory data locally under .persistentmind/ and can export or import memory sets as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, manifest.yaml, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
