## Description:

Analyzes Apple Health exports from an export.zip or exported folder to summarize activity, steps, sleep, and source counts with local shell tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:


## Use Case:

Developers, analysts, and users working with their own Apple Health exports use this skill to inspect record types, generate activity and sleep summaries, and extract bounded JSON records for local analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apple Health exports and derived outputs can contain sensitive PHI/PII.

Mitigation: Process exports locally, avoid uploading or sharing raw values without explicit consent and review, and delete exports or derivative JSON when no longer needed.

Risk: Untrusted or shared export ZIP files can expose sensitive data or place extracted temporary data outside the user's control.

Mitigation: Use exports from the user's own device, avoid untrusted ZIP files, keep files on private local storage, and avoid shared folders unless privacy controls are in place.

Risk: Large JSON exports can create broad derived datasets that are easy to overshare.

Mitigation: Prefer --limit for JSON extraction and use --out for a private output path created with 600 permissions.

Risk: Running the helper with unnecessary privileges increases the impact of shell execution or file handling mistakes.

Mitigation: Do not run the helper with elevated privileges.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Plain text summaries, JSON arrays, and restricted local files when --out is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local xmlstarlet, jq, and unzip; --limit bounds JSON output and --out creates 600-permission files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
