## Description:

Mingli is a multi-system daily horoscope skill for Western astrology, Ba-Zi / Four Pillars, numerology, I Ching, and Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukebaze](https://clawhub.ai/user/lukebaze)

### License/Terms of Use:


## Use Case:

External users use this skill to set up and receive daily or on-demand personal horoscope readings that combine Western astrology, Ba-Zi, numerology, and I Ching. The skill can calculate supporting chart data, store a horoscope profile, and send scheduled Telegram delivery when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores birth details, location, timezone, derived horoscope profile data, and a Telegram chat ID locally.

Mitigation: Confirm the user is comfortable with this local profile storage before setup, restrict access to stored files, and remove stored profile data when delivery is no longer needed.

Risk: Scheduled Telegram delivery can send recurring messages to an unintended destination if the chat ID or schedule is wrong.

Mitigation: Verify the Telegram destination and delivery timezone before enabling the cron job, and provide clear pause, resume, time-change, and removal controls.

Risk: Stored location, timezone, and schedule values are used in scheduled command strings without clear validation in the artifact behavior.

Mitigation: Validate latitude, longitude, timezone, date, time, and Telegram destination values before writing state or creating recurring jobs.

Risk: The skill depends on kerykeion and AstronomyAPI credentials for some calculations.

Mitigation: Use a pinned dependency or isolated virtual environment for kerykeion and protect ASTRONOMY_APP_ID and ASTRONOMY_APP_SECRET as credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukebaze/skills/mingli)
- [AstronomyAPI reference](references/astronomyapi-reference.md)
- [Horoscope prompt template](references/horoscope-prompt-template.md)
- [I Ching hexagrams](references/i-ching-64-hexagrams.json)
- [Zodiac reference](references/zodiac-reference.md)
- [AstronomyAPI](https://api.astronomyapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-producing helper scripts and scheduled delivery configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated horoscope prose, chart calculation JSON, cron setup details, and Telegram delivery instructions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
