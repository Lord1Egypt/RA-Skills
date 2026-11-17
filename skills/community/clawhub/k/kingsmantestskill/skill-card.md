## Description:

Generates a daily Chinese-language civil aviation news digest for the previous Beijing-time day, selecting up to 10 public-source items and sending the report to a specified email recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyun1118](https://clawhub.ai/user/wuyun1118)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to receive a concise daily roundup of civil aviation news covering airlines, airports, air traffic control, routes, regulation, safety, and service topics. It is intended for quick situational awareness, not deep research reports or non-aviation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to email each report to a fixed external address.

Mitigation: Install only if wuyun5329@163.com is the intended recipient, or require a version that asks for and confirms the recipient before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuyun1118/skills/kingsmantestskill)
- [ClawHub publisher profile](https://clawhub.ai/user/wuyun1118)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown news digest in Chinese with ranked items, sources, summaries, impact notes, observation points, and shortage notices when fewer than 10 verified items are available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may also attempt to email the generated report to the configured recipient.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
