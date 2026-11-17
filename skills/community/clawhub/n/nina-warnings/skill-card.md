## Description:

Provides read-only access to current German public warnings from the official NINA / warnung.bund.de API for city, district, ARS-code, and source-feed checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolf128058](https://clawhub.ai/user/wolf128058)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to check active German civil protection, weather, flood, and source-feed warnings for cities, districts, or ARS codes. It returns concise human-readable summaries or machine-readable JSON from public warning endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on live public data from warnung.bund.de and requires network access.

Mitigation: Confirm network access before use, report API results plainly, and avoid stating more certainty than the returned warning data supports.

Risk: Local place lookup depends on the bundled or locally populated ARS cache, which may miss places or return ambiguous matches.

Mitigation: Use explicit 12-digit ARS codes for important checks, mention the resolved region, and extend the ARS cache when local coverage is insufficient.

Risk: The skill runs bundled shell scripts that require bash, curl, and jq.

Mitigation: Confirm prerequisites before use and run only the read-only bundled scripts against the public warning API.

## Reference(s):

- [Official NINA API base](https://warnung.bund.de/api31)
- [ARS starter cache](references/ars-codes.json)
- [ClawHub skill page](https://clawhub.ai/wolf128058/skills/nina-warnings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Concise text or Markdown summaries with optional raw JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, network access to warnung.bund.de, and German ARS inputs, place names, or supported source-feed names.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
