## Description:

Lucky Day helps users choose upcoming auspicious dates for events such as weddings, business openings, moving, groundbreaking, engagements, and worship using Chinese almanac-style criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

External users can use this skill to request ranked auspicious dates for a planned activity, optionally including their Chinese zodiac sign to avoid conflicting days. The skill returns reference-only recommendations with date, almanac attributes, zodiac conflict notes, and brief reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Almanac-style recommendations may be mistaken for authoritative planning, legal, business, or personal advice.

Mitigation: Present the dates as reference-only suggestions and encourage users to consider practical constraints and professional advice where relevant.

Risk: The skill is Chinese-language and expects Chinese event and zodiac terms.

Mitigation: Use supported Chinese inputs or translate user requests before invoking the bundled script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mingo-318/skills/lucky-day)
- [Skill Definition](artifact/SKILL.md)
- [Bundled Lucky-Day Script](artifact/lucky.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style ranked recommendations with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; recommendations are reference-only and depend on the bundled local Python script.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
