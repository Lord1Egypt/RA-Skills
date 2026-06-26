## Description: <br>
Memory-Dream helps OpenClaw agents consolidate recent daily memory files into MEMORY.md and report the changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep persistent agent memory current by scanning recent memory journals, updating MEMORY.md, optionally marking older journals, and receiving a consolidation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic or scheduled runs can quietly reshape persistent agent memory. <br>
Mitigation: Run manually first on a backed-up or version-controlled workspace, then inspect diffs to MEMORY.md and memory/*.md before enabling cron. <br>
Risk: The broad trigger word 'dream' can invoke memory consolidation unintentionally. <br>
Mitigation: Prefer explicit trigger phrases such as 'consolidate memory' or 'memory consolidation'. <br>
Risk: Some documentation describes daily logs as read-only while the skill can mark older journal files. <br>
Mitigation: Expect possible marker comments in memory/*.md and review those file diffs after execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wavmson/memory-dream) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with file edits and optional cron configuration command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update MEMORY.md and optionally add consolidation markers to memory/*.md files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
