## Description:

Official Strava OAuth integration for OpenClaw that helps agents connect to Strava, store and refresh tokens, fetch workout activities, normalize activity data, and render short training summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinchengcool](https://clawhub.ai/user/gavinchengcool)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to authorize Strava access, fetch recent activity data, and produce normalized workout summaries for OpenClaw and Wellness hub workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Strava OAuth tokens locally, including refresh tokens.

Mitigation: Keep STRAVA_CLIENT_SECRET and the token file private, set STRAVA_TOKEN_PATH to a private directory, and revoke the Strava authorization if the token file may have been exposed.

Risk: Fetched workout data can include sensitive activity, health, and location-adjacent information.

Mitigation: Avoid shared output paths for real activity data, restrict access to generated JSON files, and review summaries before sharing them outside the intended workflow.

## Reference(s):

- [Strava API (quick reference)](references/strava_api.md)
- [Output schema (for Wellness hub)](references/output_schema.md)
- [ClawHub skill page](https://clawhub.ai/gavinchengcool/skills/openclaw-strava)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or plain text summaries, normalized JSON files, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches Strava activity data for today, yesterday, or a supplied date range and can normalize output for Wellness hub ingestion.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
