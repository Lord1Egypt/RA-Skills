## Description:

Detect provider models, deduplicate them, remove unusable ones, register missing models into OpenClaw, and safely keep provider-native model ids/names during model catalog sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqh2333](https://clawhub.ai/user/zqh2333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain OpenClaw model catalogs by discovering provider models, deduplicating model ids, validating usability, registering eligible models, and scheduling controlled registry refreshes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent validation and recurring sync jobs can repeatedly act on the model registry after installation.

Mitigation: Approve cron jobs explicitly, enable them only after one clean sync and validation run, and review the latest model-registry reports after scheduled runs.

Risk: Provider API keys are used against configured provider base URLs during model discovery and probing.

Mitigation: Use only trusted provider base URLs and scoped, revocable API keys in a controlled OpenClaw environment.

Risk: Registry sync can overwrite live OpenClaw configuration and restart the gateway.

Mitigation: Back up configuration first, review generated diffs and reports, validate before keeping changes, and require explicit approval for gateway restarts.

## Reference(s):

- [Model Sync Policy](artifact/references/model-sync-policy.md)
- [Model Sync Policy JSON](artifact/references/model-sync-policy.json)
- [API Failover Upgrade Notes](artifact/references/api-failover-upgrade.md)
- [ClawHub Skill Page](https://clawhub.ai/zqh2333/skills/model-registry-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw configuration, write model-registry reports, and schedule recurring validation or sync jobs after a clean run.]

## Skill Version(s):

1.3.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
