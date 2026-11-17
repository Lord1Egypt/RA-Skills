## Description:

Generates personalized daily, weekly, or monthly Western zodiac horoscope readings for all twelve signs, including five life dimensions, a lucky guide, and a practical tip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to request entertainment-oriented Western zodiac readings by sign or birthday for a selected date or period. Agents can use it to produce single-sign or all-sign horoscope Markdown without relying on external APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist a user's full birthday and reuse profile data from a sibling skill.

Mitigation: Ask for consent before writing memory, prefer storing only a sun sign or month/day, and avoid committing MEMORY.md files.

Risk: Scheduled delivery can send generated readings or profile-derived content to external chat services.

Mitigation: Enable scheduled delivery only after the user confirms the destination and is comfortable with that service receiving the readings.

Risk: Horoscope output may be mistaken for professional advice.

Mitigation: Keep the entertainment and reflection framing visible, and direct users to qualified professionals for important medical, legal, financial, or life decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eamanc-lab/skills/horoscope-daily)
- [Publisher Profile](https://clawhub.ai/user/eamanc-lab)
- [Homepage](https://github.com/eamanc-lab/fortune-telling-skills)
- [Zodiac Sign Index](references/zodiac-index.md)
- [Aries](references/signs/aries.md)
- [Taurus](references/signs/taurus.md)
- [Gemini](references/signs/gemini.md)
- [Cancer](references/signs/cancer.md)
- [Leo](references/signs/leo.md)
- [Virgo](references/signs/virgo.md)
- [Libra](references/signs/libra.md)
- [Scorpio](references/signs/scorpio.md)
- [Sagittarius](references/signs/sagittarius.md)
- [Capricorn](references/signs/capricorn.md)
- [Aquarius](references/signs/aquarius.md)
- [Pisces](references/signs/pisces.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Guidance]

**Output Format:** [Markdown horoscope readings with structured headings, ratings, lucky-guide lists, and tips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save batch daily, weekly, or monthly horoscope files when asked for all twelve signs.]

## Skill Version(s):

2.3.0 (source: frontmatter metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
