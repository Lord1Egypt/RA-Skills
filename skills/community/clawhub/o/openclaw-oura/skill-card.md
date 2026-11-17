## Description:

Oura Ring data source for OpenClaw (Tier 1). Use to connect an Oura account using an Oura Personal Access Token, fetch Oura v2 usercollection data (sleep, readiness, activity), normalize it into a stable daily JSON shape for the Wellness hub, and render a short summary message for any chat channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinchengcool](https://clawhub.ai/user/gavinchengcool)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch daily Oura sleep, readiness, and activity data with a Personal Access Token, normalize it for a Wellness hub, and produce a concise text or Markdown digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Oura health data may be written to predictable temporary files or retained longer than intended.

Mitigation: Use private, user-owned output directories, restrict file access, and delete raw exports when no longer needed.

Risk: The Oura Personal Access Token can expose user health data if it is logged, shared, or stored insecurely.

Mitigation: Protect OURA_ACCESS_TOKEN like a password, provide it through a local environment or secret manager, and avoid committing or printing it.

Risk: Using the default timezone can fetch or summarize the wrong local day.

Mitigation: Set OURA_TZ or --tz explicitly for the user's actual timezone before fetching data.

## Reference(s):

- [Oura API quick reference](references/oura_api.md)
- [Wellness hub output schema](references/output_schema.md)
- [Oura API v2](https://api.ouraring.com/v2)
- [ClawHub skill page](https://clawhub.ai/gavinchengcool/skills/openclaw-oura)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Normalized JSON files plus text or Markdown summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OURA_ACCESS_TOKEN and optional OURA_TZ or --tz; fetches sleep, readiness, and daily activity for a requested day.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
