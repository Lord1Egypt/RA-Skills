## Description:

Mitigate prompt injection attacks, especially indirect ones from external web content or files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Developers and agents use Guardian Wall before processing untrusted web, file, or uploaded text to sanitize content, flag common prompt-injection patterns, and wrap suspicious content for safer downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword and regex heuristics can miss sophisticated or obfuscated prompt-injection attacks.

Mitigation: Treat clean results as a screening signal, keep untrusted content delimited, and manually review high-stakes inputs.

Risk: Heuristics can flag benign content that resembles attack examples.

Mitigation: Review warnings manually before blocking content or changing downstream actions.

Risk: The artifact includes adversarial phrases as examples of attacks to detect.

Mitigation: Use those examples only as detection evidence and keep them separated from operational task instructions.

## Reference(s):

- [Comprehensive Encyclopedia of LLM Adversarial Patterns](references/patterns.md)
- [Guardian Wall ClawHub Release](https://clawhub.ai/1999azzar/skills/guardian-wall-azzar)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional plain-text sanitizer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The sanitizer returns cleaned text and warnings; detections are heuristic and require manual review.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
