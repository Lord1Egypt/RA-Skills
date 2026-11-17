## Description:

Execution discipline for agents with instinct, verification, trust calibration, approval gates, trust boundaries, trust recovery, discrepancy reasoning, and resilient error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palxislabs](https://clawhub.ai/user/palxislabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use IBT to add execution discipline, verification habits, approval gates, trust calibration, recovery behavior, and preference handling to assistant workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persisted USER.md preference file can carry assumptions into later sessions and affect future agent behavior.

Mitigation: Review USER.md periodically, keep it human-readable, and delete inferred or stale preferences that were not explicitly approved.

Risk: Stored preferences could weaken approval or verification behavior if the agent over-applies learned preferences.

Mitigation: Keep approval gates and verification rules stronger than convenience preferences, especially for destructive, public, external, or high-impact actions.

Risk: Preference storage can expose sensitive information if it is used for secrets, credentials, financial data, or private communications.

Mitigation: Store only generic communication, task, project, and session preferences; do not store API keys, passwords, tokens, raw credentials, sensitive financial data, private messages, or personal communications.

## Reference(s):

- [IBT Skill Page](https://clawhub.ai/palxislabs/skills/ibt)
- [README](README.md)
- [Policy](POLICY.md)
- [Template](TEMPLATE.md)
- [Examples](EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance, policy text, templates, and example response patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to maintain a human-readable USER.md preference file in the agent workspace.]

## Skill Version(s):

2.9.2 (source: server release metadata; artifact SKILL.md frontmatter reports 2.9.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
