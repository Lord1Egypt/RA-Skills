## Description:

Deploy a decentralized CI/CD pipeline with 3 agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to configure a three-agent CI/CD pipeline where build, test, and deploy stages exchange artifacts, test results, webhooks, and deployment receipts over Pilot tunnels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs mutable helper skills that can affect build, test, deployment, webhook, and artifact-transfer behavior.

Mitigation: Review the exact helper skill versions and publishers before installation and pin or document approved versions where the deployment process allows it.

Risk: The skill establishes production-capable agent trust relationships and data flows across CI/CD stages.

Mitigation: Use a safe hostname prefix and confirm every handshake peer, data-flow direction, and deployment or webhook target before enabling the pipeline.

Risk: Deployment commands and receipts can affect production environments if run against live targets.

Mitigation: Treat the generated setup as production-affecting CI/CD configuration and review it through the same change-control process used for deployment automation.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, and a running daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
