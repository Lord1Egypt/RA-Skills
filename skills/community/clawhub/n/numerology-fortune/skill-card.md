## Description:

Analyzes a user's Pythagorean numerology profile from birth date and full legal name, including core numbers, personal cycles, calculation steps, and reflective interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request numerology readings, single-number explanations, or personal cycle guidance for entertainment and personal reflection. The skill calculates values from provided or previously saved profile data and returns human-readable interpretations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and silently reuses a user's full legal name and birth date in plaintext local memory files.

Mitigation: Review before installation, use only with explicit consent to save profile data, and provide a clear way to inspect, update, or delete stored profile information.

Risk: Numerology output may be mistaken for factual prediction or professional advice.

Mitigation: Keep readings framed as entertainment and personal exploration, and preserve the disclaimer that major life decisions should rely on rational judgment and professional consultation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eamanc-lab/skills/numerology-fortune)
- [Project homepage](https://github.com/eamanc-lab/fortune-telling-skills)
- [Numerology Calculation Rules](references/calculation-rules.md)
- [Number Meanings Reference](references/number-meanings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown report with calculation steps, interpretations, and optional local MEMORY.md profile cache]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires birth date for core calculations and full legal name in English for name-based numbers.]

## Skill Version(s):

1.2.0 (source: server release metadata and target metadata; artifact metadata states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
