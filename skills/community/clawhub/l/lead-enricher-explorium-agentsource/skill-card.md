## Description:

Lead Enricher - Explorium AgentSource helps agents find and enrich B2B companies and contacts through the AgentSource API, preview results, and export confirmed records to CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yossigolan](https://clawhub.ai/user/yossigolan)

### License/Terms of Use:


## Use Case:

External users, sales teams, revenue teams, and developers use this skill to turn natural-language B2B targeting requests into AgentSource searches, preview counts and samples, enrich companies or prospects, and export confirmed results to CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an Explorium API key and B2B contact or prospect data.

Mitigation: Review before installing, use only on a private machine or account, and avoid entering the API key in recorded or shared terminals.

Risk: API keys exposed in terminal scrollback or shared environments may remain usable.

Mitigation: Rotate the key if exposure is suspected and prefer environment or config handling on private systems.

Risk: Result data is written to predictable /tmp JSON files, which may be inappropriate for regulated or sensitive contact lists.

Mitigation: Avoid processing regulated or sensitive contact lists until result files are stored in a private directory with 0600 permissions.

Risk: Optional call_reasoning can send the user's natural-language query to the remote API as request metadata.

Mitigation: Use call_reasoning only after user consent; omit it when query text should not be sent.

## Reference(s):

- [Filter Reference](artifact/references/filters.md)
- [Enrichment Reference](artifact/references/enrichments.md)
- [Events Reference](artifact/references/events.md)
- [Explorium API Key Setup](https://developers.explorium.ai/reference/setup/getting_your_api_key)
- [Explorium AgentSource API Endpoint](https://api.explorium.ai/v1/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON files, CSV files, Configuration]

**Output Format:** [Markdown guidance with inline shell commands; CLI operations write JSON result files and CSV exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EXPLORIUM_API_KEY; full fetches and exports require explicit user confirmation after sample preview.]

## Skill Version(s):

1.0.0 (source: server release metadata and plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
