## Description:

Mutual Consent defines live consent boundaries for agents by keeping scope bounded, responding to friction, announcing state changes, and preserving safe exit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otherpowers](https://clawhub.ai/user/otherpowers)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to shape how an agent asks for consent, holds scope, responds to hesitation or silence, announces state changes, and exits without retaining or exploiting user data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally makes an agent more likely to pause, narrow scope, avoid persistence, and discuss exit or data portability.

Mitigation: Install it only when those consent and boundary-checking behaviors are desired for the target agent.

Risk: The artifact states that it does not replace legal consent, privacy law, or contractual terms.

Mitigation: Review applicable legal and policy requirements separately before using this framework in regulated consent flows.

## Reference(s):

- [Mutual Consent on ClawHub](https://clawhub.ai/otherpowers/skills/mutual-consent)
- [CARE Principles for Indigenous Data Governance](https://www.gida-global.org/careprinciples)
- [Carroll et al. 2020, CARE Principles for Indigenous Data Governance](https://doi.org/10.5334/dsj-2020-043)
- [Mia Mingus](https://en.wikipedia.org/wiki/Mia_Mingus)
- [Patty Berne](https://en.wikipedia.org/wiki/Patricia_Berne)
- [Alice Wong](https://en.wikipedia.org/wiki/Alice_Wong_(activist))
- [Ida B. Wells](https://en.wikipedia.org/wiki/Ida_B._Wells)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Configuration]

**Output Format:** [Markdown guidance with a compact YAML consent_eval form and structured consent output definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only governance skill; no executable code, install hooks, credential access, persistence mechanism, or hidden data flow.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
