## Description: <br>
Copy and snapshot all important agent context (MEMORY.md, memory/*.md, AGENTS.md, SOUL.md, etc.) into a dedicated archive directory or repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrimsonDevil333333](https://clawhub.ai/user/CrimsonDevil333333) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Memory Keeper to back up agent memory, context, and configuration files before maintenance, migrations, or recovery work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can archive sensitive agent memory, context, and extra workspace files to a local path or Git remote. <br>
Mitigation: Install only when memory backup is intended, prefer a local target or private repository, and review files before committing or pushing. <br>
Risk: Broad extra-file patterns or remote URLs could expose unintended data or credentials. <br>
Mitigation: Avoid broad --allow-extra patterns, never place tokens in remote URLs or commands, and redact memory log entries if a remote URL contained credentials. <br>


## Reference(s): <br>
- [Usage Reference](references/usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/CrimsonDevil333333/memory-keeper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can copy selected workspace files, append memory log entries, and optionally run git commit or push commands when invoked.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
