## Description:

A Chinese self-reflection skill that starts from an emotional trigger and layers analysis through subconscious needs, thinking patterns, and core beliefs to produce an iceberg-style analysis with reconstruction suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-long-2022](https://clawhub.ai/user/jack-long-2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders can use this skill to structure non-clinical self-reflection around emotional triggers, recurring fears, thinking patterns, and core beliefs. It is intended for reflective insight and practical reframing suggestions, not crisis or clinical mental-health support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for or infer sensitive emotional history, fears, trauma-related origins, and core beliefs.

Mitigation: Use it only when the user intentionally wants this kind of reflection, and avoid sharing information the user does not want retained.

Risk: The skill can start deep psychological-style analysis without explicit consent.

Mitigation: Require explicit user opt-in before deeper layers of analysis, especially before discussing origins, trauma, or core beliefs.

Risk: The artifact describes storing a user preference in memory when a user resists deep analysis.

Mitigation: Change memory behavior to require explicit opt-in or keep these preferences session-only.

Risk: Users may over-rely on reflective output for crisis or clinical mental-health needs.

Mitigation: Present the output as non-clinical reflection and direct users to appropriate professional or crisis support for severe situations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jack-long-2022/skills/iceberg-excavation)
- [Publisher Profile](https://clawhub.ai/user/jack-long-2022)
- [Skill Overview](artifact/SKILL.md)
- [Configuration Template](artifact/config/iceberg-config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration]

**Output Format:** [Markdown, JSON, or plain text structured as layered self-reflection analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include emotion intensity scores, configurable analysis depth, and system reconstruction suggestions when enabled.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact version information)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
