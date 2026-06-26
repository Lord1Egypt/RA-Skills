## Description: <br>
Official Strava OAuth integration for OpenClaw that connects to Strava, stores and refreshes tokens, fetches workout activity data for a day or date range, and supports training summaries, weekly mileage, activity lists, and Wellness hub normalization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinchengcool](https://clawhub.ai/user/gavinchengcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to authorize Strava, fetch daily or date-range workout activities, normalize them for a Wellness hub, and render concise training summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Strava OAuth tokens locally and uses a Strava client secret. <br>
Mitigation: Keep STRAVA_CLIENT_SECRET and STRAVA_TOKEN_PATH contents private, restrict token file permissions, and revoke the Strava OAuth grant when access is no longer needed. <br>
Risk: Fetched activity exports may contain sensitive workout, location, timing, heart-rate, or wellness-related data. <br>
Mitigation: Avoid sharing raw activity exports and review normalized JSON or rendered summaries before sending them outside the intended workflow. <br>
Risk: Daily activity filtering depends on the configured timezone. <br>
Mitigation: Set STRAVA_TZ to the user's IANA timezone before fetching today, yesterday, or date-specific activity data. <br>


## Reference(s): <br>
- [Strava API quick reference](references/strava_api.md) <br>
- [Output schema](references/output_schema.md) <br>
- [Strava OAuth authorize endpoint](https://www.strava.com/oauth/authorize) <br>
- [Strava athlete activities endpoint](https://www.strava.com/api/v3/athlete/activities) <br>
- [ClawHub skill page](https://clawhub.ai/gavinchengcool/openclaw-strava) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown or text summaries, shell command guidance, and JSON activity files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normalized activity JSON includes workout timing, type, duration, distance, heart rate, calories, source metadata, and raw file references.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
