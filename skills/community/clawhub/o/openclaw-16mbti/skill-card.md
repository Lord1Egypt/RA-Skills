## Description:

Dynamic communication style and perspective configurator based on the 16 MBTI personality types for analyzing tasks, recommending workflows, or comparing strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archibald80000-ai](https://clawhub.ai/user/archibald80000-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent respond from a selected or recommended MBTI-style perspective for writing, planning, review, comfort, organization, brainstorming, or side-by-side comparison. It is not intended for clinical diagnosis, hiring, selection, or performance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona profiles may steer aggressive or rule-bending advice, especially ESTP/ENTP-style outputs.

Mitigation: Review outputs for legal, policy, and ethics compliance; add explicit guardrails and profile allowlisting before use in regulated or high-stakes workflows.

Risk: MBTI framing can be misused for clinical, diagnostic, hiring, selection, or performance decisions.

Mitigation: Keep the documented refusal behavior for clinical and HR screening prompts and route those requests to qualified human processes.

Risk: The server security verdict is suspicious and recommends review before installation.

Mitigation: Review the skill before installing and revise prompts that could encourage reckless business tactics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archibald80000-ai/skills/openclaw-16mbti)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Examples](artifact/examples.md)
- [Tests and validation](artifact/tests.md)
- [Personality profile index](artifact/03_personality_profiles.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style prose with structured sections, persona recommendations, comparisons, and refusal messages when boundaries are triggered]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MBTI type, task mode, output style, and comparison type inputs; no code execution or sensitive local resource access is indicated.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, changelog released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
