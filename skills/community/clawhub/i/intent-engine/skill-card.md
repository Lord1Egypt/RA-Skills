## Description:

Intent Engine classifies user requests into code, knowledge, task, and chat categories using keyword and regex matching, confidence scoring, editable intent rules, and a web management dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to classify user intent, tune routing rules, and return route recommendations for assistant workflows through a local REST API and dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard and management APIs can modify intent routing rules and should not be exposed broadly.

Mitigation: Run it only on localhost or behind authentication, and restrict access to the management APIs before using it on a shared or network-reachable machine.

Risk: Debug server behavior can expose sensitive implementation details or unsafe controls.

Mitigation: Disable Flask debug mode before deployment or shared use.

Risk: User-managed regex patterns and dashboard rendering can introduce reliability or rendering risks.

Mitigation: Limit or validate regex patterns and sanitize dashboard rendering for any untrusted input.

Risk: The dependency requirement is broad and may resolve to unreviewed package versions.

Mitigation: Pin reviewed dependencies before installation in production or shared environments.

## Reference(s):

- [ClawHub Intent Engine release](https://clawhub.ai/bettermen/skills/intent-engine)
- [ClawHub publisher profile: bettermen](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Configuration]

**Output Format:** [JSON API responses and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Classification responses can include category, sub-category, confidence score, matched rules, route skill, route description, and alternatives.]

## Skill Version(s):

2.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
