## Description: <br>
Complete self-improvement system for AI agents with four-layer memory, continuous learning, experimentation, and autonomous file maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3m2b](https://clawhub.ai/user/j3m2b) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add long-lived memory, self-evaluation, learning logs, experiment tracking, and autonomous maintenance routines to AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to maintain long-lived memory and store learned user preferences, which can retain sensitive or stale information. <br>
Mitigation: Define retention, redaction, and deletion rules before deployment; review USER.md, MEMORY.md, and memory logs regularly. <br>
Risk: The skill directs autonomous file maintenance and recurring self-maintenance jobs, which can modify workspace files without timely human review. <br>
Mitigation: Constrain writable paths, require approval for scheduled jobs and generated skills, and review changes before they are used by future agent sessions. <br>
Risk: Learned patterns and self-created skills can reinforce incorrect behavior if failures are logged or summarized inaccurately. <br>
Mitigation: Periodically audit .learnings files and generated skills, and scan any new or updated skill before deployment. <br>


## Reference(s): <br>
- [Nova Self-Improver ClawHub page](https://clawhub.ai/j3m2b/nova-self-improver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with file templates, procedural steps, JSON cron examples, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace memory-file structures, learning-loop procedures, maintenance schedules, and skill-creation guidance for an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
