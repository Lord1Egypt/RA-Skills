## Description:

pasm-companion helps agents integrate an offline elderly companion that remembers key facts, prompts medication schedules, detects crisis expressions, and returns escalation context for a human notifier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to add a local PASM-based elderly companion that can retrieve important personal facts, prompt scheduled medication, and hand crisis context to a human-operated notifier. It is medical-adjacent and should not be used as a medical device or as a replacement for professional judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is medical-adjacent and includes medication prompts, crisis detection, and emergency escalation context.

Mitigation: Keep a human decision-maker in the loop for medication, diagnosis, emergencies, and any notifier that contacts family or emergency services.

Risk: The skill depends on the external pasm-agents package.

Mitigation: Install only after reviewing and accepting that dependency and its source or package distribution.

Risk: The companion stores elder-care facts and interaction state locally.

Mitigation: Treat local state as sensitive personal data and protect the storage location according to the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arronjack/skills/pasm-companion)
- [pasm-agents project homepage](https://github.com/arronJack/pasm-agents)
- [pasm-skills tutorial](https://github.com/arronJack/pasm-skills/blob/master/docs/TUTORIAL.md)
- [pasm-agents source install mirror](https://gitee.com/arronzheng/pasm-agents)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local/offline setup guidance and integration examples for an external pasm-agents dependency.]

## Skill Version(s):

0.5.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
