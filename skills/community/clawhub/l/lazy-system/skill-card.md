## Description: <br>
Lazy System is a bilingual agent skill that uses proactive daily check-ins and minimum viable actions to help users maintain habits without relying on self-starting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcii](https://clawhub.ai/user/0xcii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to configure an agent-driven habit execution routine with scheduled check-ins, simple progress memory, and tolerant restart behavior. It is intended for people who know what action they want to take but need an external prompt to start. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may install a daily scheduled check-in or memory-based habit tracking without intending ongoing reminders or persistent progress state. <br>
Mitigation: Confirm the desired schedule and memory content before installing; remove the Hermes cron job and related memory entry when stopping the system. <br>
Risk: Using the reset interaction clears habit counters and progress state. <br>
Mitigation: Use reset only when intentionally restarting the habit system, and confirm that clearing counters is acceptable before invoking it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xcii/lazy-system) <br>
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Hermes cron and memory setup examples for daily check-ins and simple progress tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
