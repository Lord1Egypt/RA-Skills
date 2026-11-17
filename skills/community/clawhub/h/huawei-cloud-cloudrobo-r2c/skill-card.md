## Description:

Starts the robot-side R2C client to exchange observations and actions with CloudRobo over Zenoh using an mTLS credential bundle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to configure and start a robot-side CloudRobo R2C client, test observation and action flows, record observations, and extend hardware adapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom adapter may move hardware during testing, and dry-run does not guarantee that startup or shutdown will avoid movement.

Mitigation: Use a dummy adapter until the motion-safety issue is corrected, and require explicit authorization before real hardware execution.

Risk: Dry-run still transmits observations, including camera data, to the configured cloud destination.

Mitigation: Review the cloud destination and camera mappings before starting the client.

Risk: Credential bundles contain private keys, and external SDK packages were not validated by this review.

Mitigation: Protect the credential bundle and verify external packages before use.

Risk: Tests using shared temporary paths may interfere with other data, and a test process may not stop on its own.

Mitigation: Use a private temporary directory and an external timeout for tests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-r2c)
- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [Authentication & Access Control](artifact/references/iam-policies.md)
- [Custom Adapter Guide](artifact/references/custom-adapter-guide.md)
- [Verification Method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with shell commands, YAML examples, and adapter code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
