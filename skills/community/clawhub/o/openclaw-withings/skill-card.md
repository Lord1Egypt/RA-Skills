## Description:

Official Withings OAuth integration for OpenClaw that connects a personal Withings account, stores and refreshes tokens locally, fetches health measurements and sleep summaries where available, and produces normalized daily JSON for the Wellness hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinchengcool](https://clawhub.ai/user/gavinchengcool)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw agents use this source skill to authorize a personal Withings account, retrieve daily wellness measurements, normalize them for a Wellness hub, and render a short channel-aware summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth tokens and Withings health data are sensitive and may be exposed if written to shared paths or permissive directories.

Mitigation: Use a private token path and private output directory, avoid shared /tmp filenames, and restrict permissions on token and output files.

Risk: OAuth loopback authorization does not validate a state parameter, which weakens protection against authorization response mix-up or injection.

Mitigation: Review OAuth behavior before installation, prefer controlled authorization environments, and verify the pasted or loopback authorization response before saving tokens.

Risk: Health summaries can be incomplete because sleep summary fetching is best-effort and missing measurements render as absent values.

Mitigation: Treat rendered summaries as convenience reports, inspect the normalized JSON when accuracy matters, and avoid using the output as medical advice.

## Reference(s):

- [Withings API quick reference](references/withings_api.md)
- [Output schema for Wellness hub](references/output_schema.md)
- [Withings Developer Documentation](https://developer.withings.com/)
- [ClawHub skill page](https://clawhub.ai/gavinchengcool/skills/openclaw-withings)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text summaries, JSON files, Python scripts, and environment-variable setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized daily JSON includes date, timezone, generated timestamp, sleep, body, vitals, source list, and raw-file provenance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
