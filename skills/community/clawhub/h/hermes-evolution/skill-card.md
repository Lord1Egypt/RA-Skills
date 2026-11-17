## Description:

Hermes Evolution enhances OpenClaw with fast PM routing, proactive self-checks, automatic skill generation, user profiling, layered memory, and continuous learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add an OpenClaw productivity-assistant layer for task routing, task management, proactive checks, memory, user profiling, workflow learning, and multi-agent coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle task, user, credential, and agent-memory data in workspaces that may contain sensitive information.

Mitigation: Review the skill before installation and gate the profiler, self-improving rules, frozen memory, scheduler, and auto-skill generator behind explicit approval in sensitive workspaces.

Risk: Feishu notification behavior can expose credentials or task content if configured without transport and recipient review.

Mitigation: Do not configure Feishu credentials unless the notifier is changed to use HTTPS and sends only to a recipient you explicitly control.

Risk: Automatic skill generation, scheduling, memory, and self-improving rules can change assistant behavior over time.

Mitigation: Require review, scanning, and approval before generated skills, scheduled actions, memory changes, or learned rules are enabled.

## Reference(s):

- [Hermes Evolution ClawHub page](https://clawhub.ai/wuritu/skills/hermes-evolution)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Hermes Evolution v1.0 documentation](artifact/docs/HERMES-EVOLUTION-v1.0.md)
- [Deployment checklist](artifact/docs/HERMES-DEPLOY-CHECKLIST.md)
- [Quick reference](artifact/docs/HERMES-QUICK-REF.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JavaScript and shell command examples; JSON task, rule, schedule, and generated-skill files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include routing decisions, task states, recommendations, summaries, logs, generated skill definitions, and configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
