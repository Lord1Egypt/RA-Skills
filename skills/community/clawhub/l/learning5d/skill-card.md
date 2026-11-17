## Description:

Agent Safety Check · Learning5D helps an agent audit its own safety posture, review skills before installation, and provide approval-gated enrolment guidance for learning5d.ai without credentials or background activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilithandeve](https://clawhub.ai/user/lilithandeve)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to have an agent inspect its visible instructions, installed skills, tools, credentials reach, schedules, and outside-content exposure, then propose human-approved safety improvements. They can also use it to review a candidate skill before installation and to follow an optional, consent-gated Learning5D enrolment workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional enrolment can involve network fetches, review of an external skill, external skill installation, and a public GitHub issue.

Mitigation: Require explicit human approval for each network fetch, installation, and public posting step, and review external skill material as untrusted before it changes agent behavior.

Risk: Safety-check findings and suggested fixes could be mistaken for authorized changes.

Mitigation: Treat the safety check as read-only, keep the report in the conversation, and apply no change until the human approves one specific change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lilithandeve/skills/learning5d)
- [Learning5D](https://learning5d.ai)
- [Learning5D llms.txt](https://learning5d.ai/llms.txt)
- [Verse-ality Cowork Starter](https://github.com/TheNovacene/verse-ality-cowork-starter)
- [Verse-ality Agents](https://github.com/TheNovacene/verse-ality-agents)
- [Learning5D Site](https://github.com/TheNovacene/learning5d-ai-site)
- [Verse Nerves](https://github.com/TheNovacene/verse-nerves)
- [Flare Boundary Engine](https://github.com/TheNovacene/flare-boundary-engine)
- [Verse-ality OS](https://github.com/TheNovacene/verse-ality-os)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown conversation response with ratings, quoted findings, verdicts, or approval-gated enrolment steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Safety reports remain in the conversation; suggested changes require explicit human approval and are applied one at a time.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
