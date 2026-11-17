## Description:

Deploy a data labeling pipeline with 4 agents for ingestion, auto-labeling, quality review, and dataset export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML operations teams use this skill to configure a four-agent pipeline that ingests raw data, applies ML labels, reviews quality, and exports training-ready datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs unpinned dependent skills.

Mitigation: Use trusted, pinned versions of each dependent skill before installing in production.

Risk: The setup creates persistent agent configuration.

Mitigation: Inspect ~/.pilot/setups/data-labeling-pipeline.json after setup and remove it when the deployment is no longer needed.

Risk: The setup establishes trusted data flows between peers and to external notification destinations.

Mitigation: Verify peer hostnames or identities before handshakes and confirm S3, shared-storage, and webhook destinations.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-data-labeling-pipeline-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl and clawhub binaries, the pilot-protocol skill, dependent Pilot skills, and a running daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
