## Description:

Use Jev and WorkerKit to classify Gmail and Outlook emails for AI-powered inbox analysis, prioritization, and triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workerkit](https://clawhub.ai/user/workerkit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install, authorize, deploy, and reuse a WorkerKit email-classification worker for Gmail or Outlook inbox triage. It supports bounded classification runs, reporting category totals, coverage limits, warnings, and reusable worker links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires user-approved WorkerKit worker-management scopes and a connected Gmail or Outlook account for read-only classification.

Mitigation: Review the kit preview, publisher, requested scopes, budget limits, and email account identity before deployment; keep OAuth secrets and keys in approved secret storage.

Risk: Classification results are bounded by the selected window, run limits, available source coverage, and preview-level email evidence.

Mitigation: Report the actual window, judged and omitted counts, warnings, category totals, unclear cases, and any unknown completeness instead of presenting a sample as full-inbox coverage.

Risk: Worker installation, deployment, and runs can depend on available runtime capacity, wallet funding, and approved spending limits.

Mitigation: Check account usage and readiness gates before running, set max cost limits for deployment, and report settled cost data rather than in-flight estimates.

## Reference(s):

- [Email Jev Classifier kit](https://workerkit.ai/kit/email-jev-classifier)
- [OpenClaw setup](https://docs.openclaw.ai/start/getting-started)
- [WorkerKit OpenClaw setup guide](https://workerkit.ai/openclaw/setup.md)
- [WorkerKit fleet skill](https://workerkit.ai/openclaw/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/workerkit/skills/jev-email)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports worker and run links, classification counts, category totals, cost details, warnings, omissions, and coverage limits when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
