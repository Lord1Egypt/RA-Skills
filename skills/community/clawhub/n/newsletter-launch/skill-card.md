## Description: <br>
Newsletter Launch runs a setup wizard, scaffolds newsletter project files, and wires automation crons for a new Beehiiv newsletter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[micphigoo](https://clawhub.ai/user/micphigoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and newsletter operators use this skill to launch a new newsletter from scratch or set up a second newsletter on a new topic. It guides setup, generates project configuration and writing materials, and creates recurring automation for research, issue writing, publishing checks, and keyword refreshes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Beehiiv credentials and may place them in generated configuration, cron payloads, command output, logs, or project history if the operator is not careful. <br>
Mitigation: Use the least-privileged Beehiiv key available, keep generated configuration and cron payloads out of public files and logs, and rotate any key that was pasted into chat, files, logs, or git history. <br>
Risk: The skill creates persistent newsletter automation that can continue using credentials and may publish content if auto-publishing is enabled. <br>
Mitigation: Review generated files and cron definitions before enabling them, keep auto-publishing disabled until a test run succeeds, and confirm schedules, timezones, and Beehiiv plan access before relying on the automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/micphigoo/newsletter-launch) <br>
- [Beehiiv Setup Guide](references/beehiiv-setup.md) <br>
- [Config Schema](references/config-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with generated files, JSON configuration, cron definitions, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces newsletter project files and recurring automation that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
