## Description:

Manage Huawei Cloud OptVerse algorithm projects and evolution tasks through KooCLI, including uploads, task monitoring, result retrieval, and optional OBS and IAM setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Huawei Cloud LLM4AD code evolution workflows: upload Python or C++ algorithms and evaluators, create and monitor evolution tasks, and retrieve results and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional OBS delegation may grant broader or longer-lived permissions than needed.

Mitigation: Have an administrator limit actions to the selected bucket and prefix, verify the trusted principal, set an expiry and removal plan, and skip delegation when it is unnecessary.

Risk: Source code is sent to OptVerse even when OBS output is disabled, and uploads may include private files.

Mitigation: Upload only reviewed files from a staging directory and confirm the source is appropriate to send to the service.

Risk: Credentials or private information could be exposed through agent memory or support payloads.

Mitigation: Keep credentials out of agent memory and redact support payloads before sharing them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-optv-evolve-management)
- [KooCLI API mapping](artifact/references/api-mapping.md)
- [Prerequisites and configuration](artifact/references/prerequisites.md)
- [IAM agency setup](artifact/references/iam-agency.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Python workflow and conventions](artifact/references/language-python.md)
- [C++ workflow and conventions](artifact/references/language-cpp.md)
- [Evolution task workflow](artifact/references/evolve-task-workflow.md)
- [Results, logs, and status](artifact/references/result-logs-status.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands and Python or C++ code templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example algorithm, evaluator, and baseline templates for supported workflows.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
