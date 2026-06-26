## Description: <br>
Vedic astrology (Jyotish) REST API skill for Panchanga, Kundali, KP system, aspects, dashas, muhurta, compatibility, transits, remedies, webhooks, and related sidereal calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[degen0root](https://clawhub.ai/user/degen0root) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have agents call PanchangaAPI for Vedic astrology data, including daily Panchanga, birth charts, timing windows, compatibility, transit analysis, festival calendars, remedies, and webhook subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send sensitive birth, time, and location data to a third-party astrology API. <br>
Mitigation: Use a dedicated API key and only send precise personal data when the user has explicitly agreed that it is needed for the requested calculation. <br>
Risk: The skill describes registration, webhook setup, and paid Telegram, crypto, and x402 flows. <br>
Mitigation: Require explicit user approval before account registration, webhook creation, or any paid flow, and enforce strict wallet spending limits for agents. <br>


## Reference(s): <br>
- [PanchangaAPI homepage](https://api.moon-bot.cc) <br>
- [ClawHub skill listing](https://clawhub.ai/degen0root/panchanga-api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires or can register a PANCHANGA_API_KEY; calculation requests use datetime, latitude, and longitude.] <br>

## Skill Version(s): <br>
4.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
