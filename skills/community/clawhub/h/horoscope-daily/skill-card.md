## Description: <br>
Generates personalized Western zodiac horoscope readings for all twelve signs across daily, weekly, and monthly periods, with optional birthday-based personalization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eamanc-lab](https://clawhub.ai/user/eamanc-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to generate entertainment-focused horoscope readings from a zodiac sign or birthday. It can produce single-sign readings in conversation or batch readings for all twelve signs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save a user's birthday and sun sign locally for personalization. <br>
Mitigation: Use it only when local profile storage is acceptable, and update or remove saved profile details when the user requests changes. <br>
Risk: Automated daily delivery can send horoscope content to a configured channel. <br>
Mitigation: Enable scheduled delivery only after confirming the schedule, destination, and any webhook or delivery skill configuration. <br>
Risk: Horoscope readings may be mistaken for professional medical, legal, financial, or psychological advice. <br>
Mitigation: Treat outputs as entertainment and reflection, and rely on qualified professionals for important decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eamanc-lab/horoscope-daily) <br>
- [Project Homepage](https://github.com/eamanc-lab/fortune-telling-skills) <br>
- [Zodiac Sign Index](references/zodiac-index.md) <br>
- [Aries Reference](references/signs/aries.md) <br>
- [Taurus Reference](references/signs/taurus.md) <br>
- [Gemini Reference](references/signs/gemini.md) <br>
- [Cancer Reference](references/signs/cancer.md) <br>
- [Leo Reference](references/signs/leo.md) <br>
- [Virgo Reference](references/signs/virgo.md) <br>
- [Libra Reference](references/signs/libra.md) <br>
- [Scorpio Reference](references/signs/scorpio.md) <br>
- [Sagittarius Reference](references/signs/sagittarius.md) <br>
- [Capricorn Reference](references/signs/capricorn.md) <br>
- [Aquarius Reference](references/signs/aquarius.md) <br>
- [Pisces Reference](references/signs/pisces.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown horoscope readings, with optional Markdown files for batch daily, weekly, or monthly output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local MEMORY.md profile data when the user provides a birthday or sun sign.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
