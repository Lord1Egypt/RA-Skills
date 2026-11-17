## Description:

Switches OpenViking's embedding model to a local llama-server or another OpenAI-compatible endpoint, rebuilding the vector index when dimensions change and verifying the restarted service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers operating OpenViking environments use this skill to change the embedding endpoint or dimension, rebuild an incompatible vector collection, and verify the service after restart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Switching models can erase the vector collection, and stopping a process can affect an unrelated service if ownership is not confirmed.

Mitigation: Before authorizing the switch, verify the server and process ownership, validate paths and inputs, keep a recoverable collection backup, and test the reindexing and rollback plan.

## Reference(s):

- [Guardrails](artifact/references/guardrails.md)
- [Configuration Reference](artifact/references/config-reference.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Related Commands](artifact/references/related-commands.md)
- [IAM Policies and Access Controls](artifact/references/iam-policies.md)
- [Data Flow Diagram](artifact/references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Operational guidance]

**Output Format:** [Bash script with configuration changes and text status output]

**Output Parameters:** [Three inputs: model name, endpoint port, and target dimension]

**Other Properties Related to Output:** [Backs up the configuration, verifies the new collection, and restores the backup when checks fail.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
