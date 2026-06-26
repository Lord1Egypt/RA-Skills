## Description: <br>
Hermes Memory checks local agent memory files, reports memory health, and prompts users to keep long-term memory concise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdvrommel](https://clawhub.ai/user/jdvrommel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manually or periodically check OpenClaw-style MEMORY.md and USER.md files, review usage thresholds, and decide when to organize or compact local memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script scans local memory files and the ~/self-improving directory, which may expose more local content than the named MEMORY.md and USER.md files. <br>
Mitigation: Review the script paths before installing and confirm that scanning ~/self-improving and the OpenClaw workspace memory files is acceptable. <br>
Risk: Optional cron setup creates recurring local execution and may append output to health.log. <br>
Mitigation: Run the script manually first, then add or narrow the cron entry only if recurring checks are desired. <br>
Risk: The script creates local persistence in hermes-memory-state.json. <br>
Mitigation: Confirm the state file location and contents are acceptable before enabling routine use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jdvrommel/hermes-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands, plus local text output and JSON state written by the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script can write hermes-memory-state.json and can be scheduled to append health checks to health.log.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
