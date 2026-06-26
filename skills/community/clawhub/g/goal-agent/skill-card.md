## Description: <br>
Scaffold a self-learning goal-oriented agent that iterates toward a measurable goal by measuring, learning, and adapting its strategy at every heartbeat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theashbhat](https://clawhub.ai/user/theashbhat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to scaffold a goal-focused agent workspace with a measurable target, metric command, iteration budget, and constraints so an agent can optimize toward that goal over repeated heartbeats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates an autonomous agent loop whose most important generated heartbeat and evaluator templates were not present in the reviewed package. <br>
Mitigation: Review generated files before activation, supply and review missing templates, and avoid use in production or sensitive workspaces until the full loop behavior is verified. <br>
Risk: The activated loop can take repeated actions toward a user-defined goal based on text constraints rather than a programmatic sandbox. <br>
Mitigation: Run in an isolated VM or low-risk workspace, keep backups, use read-only metric commands, set a low max-iteration count, and avoid goals involving credentials, finances, destructive actions, public accounts, or sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theashbhat/goal-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Generated Markdown files and an executable shell script, with setup commands and operational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied goal, metric command, target value, and optional constraints, direction, iteration limit, and output directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
