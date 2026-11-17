## Description:

Turn scattered local sources into a source-constrained evidence notebook for incident, release, and maintainer decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiepu110](https://clawhub.ai/user/jiepu110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and incident reviewers use this skill to turn approved local sources into a concise evidence notebook that separates facts, conflicts, assumptions, and decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved local source sets may still contain secrets, credential-bearing logs, or irrelevant personal data.

Mitigation: Screen source materials before use, exclude secrets and unnecessary personal data, and review notebook outputs before sharing.

Risk: Unsupported claims or ambiguous evidence could be mistaken for established facts.

Mitigation: Keep answers source-constrained, mark inferences and missing information explicitly, and preserve citations or anchors for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiepu110/skills/oc-evidence-notebook)
- [OpenClaw Gateway Guardian GitHub repository](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evidence notebook with source lists, evidence cards, conflict lists, source-constrained answers, and a decision packet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should keep claims tied to supplied sources and label inferences or missing information.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
