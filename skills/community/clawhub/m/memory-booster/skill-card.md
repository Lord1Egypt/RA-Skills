## Description: <br>
AI dialogue memory enhancement system that helps agents warm up from prior context, save conversation snapshots, semantically search local memory, and generate customized domain memory skills with Python, ChromaDB, and sentence-transformers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeliang2000](https://clawhub.ai/user/mikeliang2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WorkBuddy users use this skill to preserve useful context across AI conversations, recall prior decisions or notes, and build semantic indexes over configured local memory directories. It also guides agents through creating domain-specific memory skill templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and index local memory files and historical conversation results, which may expose private or sensitive context. <br>
Mitigation: Configure exact memory directories before use, avoid storing secrets or confidential client data in indexed memory, and review recalled excerpts before relying on or sharing them. <br>
Risk: Automatic warmup and first-reply recall can surface historical context unexpectedly in shared or sensitive sessions. <br>
Mitigation: Use the warmup behavior only in sessions where prior context is appropriate, and disable or avoid automatic recall where privacy boundaries are unclear. <br>
Risk: The artifact declares analytics tracking without enough user control in the available evidence. <br>
Mitigation: Disable or remove analytics configuration unless telemetry is explicitly wanted and acceptable for the deployment environment. <br>
Risk: Archive and compression workflows can append to memory files or move older diary files during maintenance. <br>
Mitigation: Run archive workflows in dry-run mode first, keep backups, and inspect target memory paths before executing write or archive commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikeliang2000/memory-booster) <br>
- [Publisher profile](https://clawhub.ai/user/mikeliang2000) <br>
- [Publisher homepage](https://hermesai.ltd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command snippets, configuration guidance, memory search summaries, and generated skill templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include recalled local memory excerpts, conversation-derived summaries, generated SKILL.md content, and installation or maintenance commands.] <br>

## Skill Version(s): <br>
6.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
