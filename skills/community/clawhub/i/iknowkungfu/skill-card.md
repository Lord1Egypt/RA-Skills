## Description:

Skill discovery engine that analyzes an agent workflow and recommends missing ClawHub skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whooshinglander](https://clawhub.ai/user/whooshinglander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to profile local agent workflows, identify uncovered tool or domain areas, and receive prioritized ClawHub skill recommendations with trust scores and install commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to read broad private local agent history, recent logs, configuration, schedules, and installed skill directories.

Mitigation: Run it only in a workspace whose local history and skill files you are comfortable exposing to the agent, and review those inputs before use.

Risk: Workflow profiling can surface sensitive paths or credential-like strings from local files.

Mitigation: Keep the release's redaction safeguards active: summarize patterns only, never print credentials, and redact home-directory or username-bearing paths.

Risk: The bundled catalogue and heuristic trust scoring can lag current ClawHub state or produce imperfect recommendations.

Mitigation: Review each recommendation and its ClawHub page before installing; use the recommendations as guidance rather than automatic approvals.

## Reference(s):

- [Workflow Analysis Procedure](references/workflow-analysis.md)
- [Recommendation Engine Procedure](references/recommendation-engine.md)
- [Trust Scoring Methodology](references/scoring.md)
- [Security Quick Check](references/security-check.md)
- [Skills Index Documentation](references/skills-index.md)
- [Issue Tracker](https://github.com/whooshinglander/iknowkungfu)
- [Publisher Profile](https://clawhub.ai/user/whooshinglander)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with workflow profile summaries, ranked recommendations, trust scores, and install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should summarize patterns and categories only, redact sensitive paths or credentials, and avoid printing full file contents.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
