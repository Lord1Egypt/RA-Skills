## Description:

Access cloud storage (S3, GCS, Azure Blob) through a Pilot bridge agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transfer, list, and request cloud-stored files through a Pilot bridge agent when cloud access is mediated by a running Pilot daemon and bridge host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote callers could use the bridge host's cloud permissions without clear access controls.

Mitigation: Use authenticated requesters, per-action and per-bucket authorization, least-privilege short-lived credentials, logging, and explicit approval for sensitive downloads or presigned URLs.

Risk: The public bridge example could expose real cloud accounts if run as written.

Mitigation: Do not run the public bridge example on real cloud accounts; use private networking and production-specific access controls before deployment.

Risk: Shared temporary file paths can mix data between requests or leak downloaded content.

Mitigation: Use safe per-request temporary files and clean them after upload or download handling completes.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-s3-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, a running Pilot daemon, a bridge agent, and cloud-provider CLI credentials.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
