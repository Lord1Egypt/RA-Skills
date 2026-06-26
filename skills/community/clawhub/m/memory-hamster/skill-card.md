## Description: <br>
Memory Hamster helps agents maintain long-lived local memory with temperature-based archiving, learning records, semantic search, and skill extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tomor1984](https://clawhub.ai/user/Tomor1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Memory Hamster to add persistent local memory workflows for daily logs, lessons, errors, decisions, archive maintenance, and reusable skill extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived local memory can retain sensitive prompts, credentials, private notes, or full error dumps. <br>
Mitigation: Do not store secrets or raw private prompts, and review and prune retained memory files regularly. <br>
Risk: Scheduled jobs can make background changes to workspace memory files. <br>
Mitigation: Review the configured workspace path, use dry-runs where available, keep backups, and document how to remove cron entries. <br>
Risk: Promoted memories can change future-agent instructions in files such as SOUL.md, AGENTS.md, TOOLS.md, or generated skills. <br>
Mitigation: Require manual review before promoting memories into instruction files or new skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tomor1984/memory-hamster) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes and reports, shell command snippets, and generated skill scaffold files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or move local workspace memory files when scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter, package.json, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
