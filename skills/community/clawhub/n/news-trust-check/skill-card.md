## Description:

Verify suspicious news, announcements, screenshots, and viral claims using a high-trust source pool of official channels, Chinese and international mainstream media, and fact-checking sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloeveryworlds](https://clawhub.ai/user/helloeveryworlds)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and analysts use this skill to triage suspicious claims, viral messages, screenshots, announcements, and possible scams by checking official, mainstream media, and fact-checking sources before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A verdict could be misleading if it is based on screenshots, forwarded text, or weak secondary sources.

Mitigation: Require cited official or reputable sources before treating important financial, security, legal, or public claims as reliable.

Risk: The optional keyword scorer can miss context-dependent scams or overstate risk from keyword matches.

Mitigation: Use the scorer only as triage scaffolding and complete the source-based verification workflow before recommending action.

Risk: Money-transfer, credential, token, cookie, OTP, or impersonation claims can create immediate user harm.

Mitigation: Apply a stronger proof threshold, flag these claims as high risk first, and advise users not to share sensitive information or send funds without official confirmation.

## Reference(s):

- [High-Trust Source Pool](references/high-trust-sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured Markdown verdict with evidence, feasibility, risk flags, and recommended action; optional JSON keyword risk score from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script requires non-empty text input and provides keyword-based scaffolding rather than final source verification.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
