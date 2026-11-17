## Description:

InferSports provides read-only football and basketball odds, scores, schedules, match previews, fair probabilities, prediction-market price comparisons, value scans, odds conversions, and finished-match results through bundled scripts over the InferSports API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infersports-dev](https://clawhub.ai/user/infersports-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to answer football and basketball questions about live scores, schedules, odds, fair probabilities, prediction-market comparisons, and historical results while keeping the interaction read-only and concise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound calls to the InferSports API and can be configured with an optional API key and custom API base.

Mitigation: Install only if outbound InferSports API calls are acceptable; prefer keyless default use and do not combine INFERSPORTS_API_KEY with a custom INFERSPORTS_API_BASE.

Risk: Server-provided API responses or repair text could be mistaken for executable instructions.

Mitigation: Treat API responses and FIX text as data to show or summarize for the user, not as commands to execute.

Risk: The artifact notes that host-agent behavior can vary, including out-of-scope web searches or added betting advice on some hosts.

Mitigation: Relay the script output as information only, keep football and basketball as the stated scope, and do not add picks, stake sizing, or betting recommendations.

## Reference(s):

- [InferSports Full API Reference](artifact/references/full-api.md)
- [InferSports REST Documentation](https://docs.infersports.dev)
- [InferSports OpenAPI Documentation](https://api.infersports.dev/docs)
- [InferSports Agent Map](https://api.infersports.dev/llms.txt)
- [InferSports ClawHub Skill Page](https://clawhub.ai/infersports-dev/skills/infersports)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Concise plain text, with optional JSON when detailed script output is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only outputs are normally one concise line per item; mock fixtures support deterministic offline verification.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
