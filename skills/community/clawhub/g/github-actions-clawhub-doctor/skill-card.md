## Description:

Diagnoses GitHub Actions-to-ClawHub publishing failures and suggests evidence-based fixes for workflow, ownership, credential wiring, skill naming, and registry status issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers publishing skills through GitHub Actions use this skill to identify why ClawHub releases fail or appear to fail, then prioritize a minimal fix and a verification step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow logs or configuration shared for diagnosis may expose ClawHub tokens or other secrets.

Mitigation: Share redacted logs and configuration; never paste raw secret values into chat.

Risk: An Actions failure may be mistaken for a failed release when registry publication is pending or already complete.

Mitigation: Check the registry status or public skill page before changing the publication workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bonniegeng-max/skills/github-actions-clawhub-doctor)
- [Project homepage (skill metadata)](https://github.com/bonniegeng-max/openclaw-publisher)
- [Publishing failure map](references/failure_map.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline configuration and verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies the failure layer, cites supporting configuration or logs, and proposes a minimal fix and verification step.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
