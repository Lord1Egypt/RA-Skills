## Description:

Analyzes text for manipulation patterns including urgency, false authority, social proof, FUD, grandiosity, dominance assertions, us-vs-them framing, and emotional manipulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudio-prime](https://clawhub.ai/user/claudio-prime)

### License/Terms of Use:


## Use Case:

Agents, developers, and security-minded reviewers use this skill to evaluate suspicious messages, social posts, or other text for common influence tactics before deciding how much skepticism to apply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The detector is heuristic and may produce false positives, so a flagged passage is not proof of manipulation.

Mitigation: Use the report as a prompt for additional scrutiny and corroborate findings with contextual human review.

Risk: Keyword-based matching can miss sophisticated manipulation that avoids obvious phrases.

Mitigation: Treat a low score as limited evidence and continue applying independent judgment for high-impact decisions.

Risk: The skill analyzes user-supplied local text, which may include sensitive content.

Mitigation: Run it only on text appropriate for the local environment; the security summary reports no network access or persistence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claudio-prime/skills/manipulation-detector)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Human-readable CLI report with score, severity label, triggered flags, matched phrases, and cautionary notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided text from stdin or a local file; security evidence reports no network access or persistence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
