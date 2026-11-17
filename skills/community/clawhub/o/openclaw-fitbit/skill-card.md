## Description:

Official Fitbit OAuth integration for OpenClaw (Tier 1). Use to connect/authorize Fitbit, store+refresh tokens locally, fetch daily activity + sleep summaries, normalize into a stable daily JSON shape for the Wellness hub, and render a short digest for any chat channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinchengcool](https://clawhub.ai/user/gavinchengcool)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to authorize Fitbit access, retrieve daily activity and sleep data, normalize it for a Wellness hub, and render a short digest for chat channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence security summary says the skill asks for extra Fitbit permissions.

Mitigation: Use the narrowest Fitbit scopes possible, preferably activity and sleep only.

Risk: The release evidence security summary says the skill writes sensitive health data to local files with weak handling.

Mitigation: Set a private output directory instead of /tmp and treat raw and normalized JSON files as sensitive health records.

Risk: Stored Fitbit OAuth tokens can continue granting account access after authorization.

Mitigation: Revoke or rotate Fitbit tokens if broader scopes were previously authorized or if token files may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gavinchengcool/skills/openclaw-fitbit)
- [Publisher profile](https://clawhub.ai/user/gavinchengcool)
- [Fitbit API quick reference](references/fitbit_api.md)
- [Output schema](references/output_schema.md)
- [Fitbit OAuth authorize endpoint](https://www.fitbit.com/oauth2/authorize)
- [Fitbit OAuth token endpoint](https://api.fitbit.com/oauth2/token)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches daily Fitbit activity and sleep data, writes raw and normalized JSON files, and can render channel-aware summaries.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
