## Description:

Manage and audit OpenClaw secrets by coordinating gateway restarts, converting plaintext credentials to SecretRef format, and validating configuration accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlab1201](https://clawhub.ai/user/jlab1201)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw deployments for plaintext credentials, migrate credentials into OpenClaw secrets management, and validate that gateway and integration behavior still works after the change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local secrets and configuration edits can expose credentials or leave old plaintext keys in place.

Mitigation: Back up affected config files, restrict secrets file permissions before adding real secrets, avoid pasting credentials into shared terminals, and rotate keys that were previously stored in plaintext.

Risk: Gateway reloads and configuration changes can disrupt OpenClaw authentication or integrations.

Mitigation: Apply gateway operations sequentially, reload secrets deliberately, and validate with OpenClaw audit and gateway health checks before treating migration as complete.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jlab1201/skills/openclaw-secrets-hygiene)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audit reports, migration plans, configuration templates, testing checklists, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
