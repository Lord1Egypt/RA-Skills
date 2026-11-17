## Description:

Patches OpenClaw and the @openclaw/msteams plugin to diagnose, repair, and verify Microsoft Teams China/21Vianet endpoint configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhs666](https://clawhub.ai/user/yhs666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to support Microsoft Teams China deployments in OpenClaw by diagnosing endpoint issues, applying patch scripts, setting required cloud configuration, and producing repair reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill rewrites installed OpenClaw and @openclaw/msteams program files.

Mitigation: Run read-only diagnosis first, back up the affected installations, test against the exact package versions in use, and keep a restore plan before applying patches.

Risk: Persistent CLOUD and SERVICE_URL changes can affect host behavior beyond the immediate repair session.

Mitigation: Record current environment or registry settings before changes and remove or restore those settings if the patch is misapplied.

Risk: Automatic repair and Gateway restart behavior can interrupt a running OpenClaw host.

Mitigation: Avoid scheduled auto-fix until the workflow has been tested on the target host, and run restarts during an approved maintenance window where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhs666/skills/msteamschinaadapter)
- [OpenClaw](https://openclaw.ai)
- [Endpoint reference](references/endpoints.md)
- [Error code reference](references/error-codes.md)
- [Workflow reference](references/workflow.md)
- [Output standards](references/output-standards.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured repair reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic findings, patch status, verification checks, and recovery guidance.]

## Skill Version(s):

10.0.2 (source: server release metadata; artifact metadata reports 10.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
