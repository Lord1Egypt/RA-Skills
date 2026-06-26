## Description: <br>
Maintain clean, efficient memory files with GOOD/BAD/NEUTRAL categorization and semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zencrust-ai](https://clawhub.ai/user/zencrust-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to keep local agent memory concise, tagged, searchable, and organized across long-term essentials and daily memory logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory notes may retain secrets, sensitive personal data, or broad user prompts longer than intended. <br>
Mitigation: Avoid storing secrets or sensitive personal data, periodically review MEMORY.md and daily logs, and archive or remove entries that should not persist. <br>
Risk: The skill modifies local workspace memory files through shell scripts. <br>
Mitigation: Review proposed changes before relying on them and keep the MEMORY_DIR and WORKSPACE environment variables pointed at the intended workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zencrust-ai/minimal-memory) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/zencrust-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, searches, reviews, and archives local MEMORY.md and memory/YYYY-MM-DD.md files when invoked through its shell scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
