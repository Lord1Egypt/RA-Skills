## Description: <br>
AI memory middleware that gives an AI agent persistent, cross-session long-term memory with automatic capture of key facts, decisions, user preferences, project context, semantic-style search, and vector retrieval support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szwangw](https://clawhub.ai/user/szwangw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw agents persistent local memory across sessions. It stores selected facts, decisions, preferences, project notes, and session summaries, then recalls relevant context for future prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists conversation details that may include sensitive information in local memory files. <br>
Mitigation: Avoid saving secrets, credentials, regulated data, or private personal details; review saved memories regularly and delete unwanted entries with the provided forget command. <br>
Risk: Recalled memories may be injected into future prompts outside their original context. <br>
Mitigation: Use project tags carefully, keep memories selective, and inspect context-injection output before relying on it for sensitive or compartmentalized work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szwangw/memory-for-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text output with inline shell commands and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite-backed memory records, search results, context-injection text, setup guidance, session summaries, and memory statistics.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
