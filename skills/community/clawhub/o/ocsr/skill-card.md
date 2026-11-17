## Description:

PatSight-MolVision performs optical chemical structure recognition on one or more molecular structure images, calls the PatSight Patent Extractor API, and returns SMILES/SDF data with RDKit-derived properties and a dashboard report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snailwhb](https://clawhub.ai/user/snailwhb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to recognize molecular structures from uploaded images, extract SMILES/SDF records, and produce RDKit property summaries for downstream chemistry or patent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials, tokens, and uploaded molecular images may be sent to configurable network destinations.

Mitigation: Use only trusted PatSight endpoints, prefer environment variables and short-lived credentials, and avoid command-line secrets.

Risk: Confidential or unpublished molecular structures may be uploaded to an external service and stored in local result files.

Mitigation: Upload sensitive structures only with organizational approval, and manage generated JSON and PNG outputs according to data handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snailwhb/skills/ocsr)
- [PatSight homepage](https://patent.xinsight-ai.com/home)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; generated outputs are JSON result files and PNG dashboard images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PatSight credentials or token, accepts common molecular image formats, and may preserve raw API records when RDKit parsing is unavailable.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata and changelog list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
