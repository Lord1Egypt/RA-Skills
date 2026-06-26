## Description: <br>
Mingli is a multi-system daily horoscope skill that combines Western astrology, Ba-Zi/Four Pillars, numerology, I Ching readings, AstronomyAPI data, and Telegram delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukebaze](https://clawhub.ai/user/lukebaze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to set up personalized horoscope profiles, receive daily Telegram horoscope messages, request on-demand readings, and cast I Ching hexagrams. It is intended for personal divination and reflective guidance, not professional advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores birth details, approximate coordinates, timezone, and Telegram chat ID locally for recurring horoscope delivery. <br>
Mitigation: Install only if comfortable with local storage of these details, and use the documented remove command when the profile and daily job should be deleted. <br>
Risk: AstronomyAPI credentials and Telegram delivery settings are used during setup and daily execution. <br>
Mitigation: Use limited AstronomyAPI credentials, verify the Telegram destination and delivery schedule during setup, and keep credentials scoped to this use. <br>


## Reference(s): <br>
- [AstronomyAPI Reference](references/astronomyapi-reference.md) <br>
- [Horoscope Prompt Template](references/horoscope-prompt-template.md) <br>
- [I Ching 64 Hexagrams](references/i-ching-64-hexagrams.json) <br>
- [Zodiac Reference](references/zodiac-reference.md) <br>
- [AstronomyAPI](https://api.astronomyapi.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/lukebaze/mingli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown horoscope messages, JSON calculation outputs, shell commands, and cron configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses birth details, approximate coordinates, timezone, local memory, AstronomyAPI credentials, and Telegram delivery settings for recurring personalized output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
