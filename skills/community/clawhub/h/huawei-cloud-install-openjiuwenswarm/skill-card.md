## Description:

Installs and starts JiuwenSwarm locally inside the current Huawei Cloud development container by downloading the runtime mirror, extracting it, configuring credentials and model settings, and launching the service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate first-time JiuwenSwarm or WorkSwarm local setup, recovery after restart or migration, and standardized deployment workflows inside Huawei Cloud development containers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an external JiuwenSwarm runtime and creates persistent files and global commands in the container.

Mitigation: Use a disposable or dedicated Huawei Cloud development container and review the external runtime source before execution.

Risk: The deployment reads local Huawei Cloud configuration and kernel keyring credentials to populate runtime settings.

Mitigation: Avoid using a high-value API key, confirm generated configuration files use restrictive permissions, and review logs for accidental credential exposure.

Risk: The startup phase detects, stops, and starts services on matched JiuwenSwarm port ranges.

Mitigation: Verify that no unrelated services are using the matched ports before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-install-openjiuwenswarm)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [JiuwenSwarm README](https://raw.gitcode.com/openJiuwen/jiuwenswarm/raw/main/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal progress text, JSON error messages, configuration files, and a final web access URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a fixed five-phase local deployment flow and writes runtime configuration under the current container user.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
