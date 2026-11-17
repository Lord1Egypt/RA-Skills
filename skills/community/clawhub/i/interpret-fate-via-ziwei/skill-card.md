## Description:

通过紫薇斗数解释命运 A skill to interpret fate using Ziwei astrology principles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[herberthe](https://clawhub.ai/user/herberthe)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate Ziwei Dou Shu chart data from birth date, birth time, calendar type, leap-month status, and sex, then receive a human-readable astrology interpretation and related guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a user's birth date, birth time, and sex through a generated third-party chart URL.

Mitigation: Prefer local chart calculation; only open or request a populated ziwei.pub URL after the user accepts sharing those details and having them appear in browser or conversation history.

Risk: The skill gives fate and life-event interpretations that may be mistaken for factual or professional advice.

Mitigation: Present results as astrology-based interpretation and avoid treating the output as medical, legal, financial, or other professional guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/herberthe/skills/interpret-fate-via-ziwei)
- [Ziwei online chart URL](https://ziwei.pub/astrolabe/)
- [iztro discussions](https://github.com/SylarLong/iztro/discussions)
- [Ziwei Dou Shu astrolabe](docs/learn-astrolabe.md)
- [Ziwei Dou Shu palace system](docs/learn-palace.md)
- [Ziwei Dou Shu star system](docs/learn-star.md)
- [Ziwei Dou Shu mutagens](docs/learn-mutagen.md)
- [Ziwei Dou Shu patterns](docs/learn-pattern.md)
- [Ziwei Dou Shu star setup](docs/learn-setup.md)
- [Ziwei Dou Shu complete book](docs/learn-ancient-book.md)
- [Ziwei Dou Shu star question and answer text](docs/learn-ancient-book-qa.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown prose with optional Node.js code blocks and generated chart links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include astrolabe data, horoscope data, birth-hour mapping, and interpretive conclusions based on bundled reference documents.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
