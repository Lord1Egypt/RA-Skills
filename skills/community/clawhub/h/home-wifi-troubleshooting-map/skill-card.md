## Description:

Create a safe visible-diagnostic map for home Wi-Fi problems using device symptoms, router lights, placement notes, outage checks, speed tests, and support-ready evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this prompt-only skill to organize home Wi-Fi symptoms, visible equipment status, outage checks, safe basic checks, and support-ready evidence before contacting an ISP, landlord, building network owner, or device support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share Wi-Fi passwords, ISP account passwords, payment details, one-time codes, or router administrator credentials while describing the issue.

Mitigation: The skill explicitly tells the agent not to request those secrets and to rely on visible symptoms, light labels, outage notices, and account-safe support details.

Risk: Routine troubleshooting could become unsafe when equipment shows smoke, burning smell, sparks, exposed wiring, water near powered devices, damaged power supplies, or repeated breaker trips.

Mitigation: The skill directs the agent to stop routine troubleshooting and route the user to emergency services, the utility provider, landlord, building management, ISP, or a qualified professional as appropriate.

Risk: The diagnostic map may overstate conclusions from limited visible observations.

Mitigation: The skill requires the agent to separate observations from conclusions, mark unknown details instead of guessing, and prefer official provider channels for device-specific or account-specific steps.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/harrylabsj/skills/home-wifi-troubleshooting-map)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic sheet with tables, ranked likely issue areas, next actions, and a support call script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only; no code execution, network access, or credential collection.]

## Skill Version(s):

1.0.1 (source: server release, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
