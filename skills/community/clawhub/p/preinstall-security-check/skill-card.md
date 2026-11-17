## Description:

Pre-installation security assessment for ClawHub skills. Run before any skill install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marianachow0321](https://clawhub.ai/user/marianachow0321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to assess another ClawHub skill before installation, review trust signals and risk findings, and decide whether to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can gate skill-install workflows and may install untrusted skills during its own review with weak containment details.

Mitigation: Review carefully before installation, prefer inspecting inert artifacts before install, and run any review in a disposable sandbox boundary.

Risk: The security workflow asks for broad control over skill-install decisions.

Mitigation: Require explicit user confirmation before executing install commands and validate skill identifiers before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marianachow0321/skills/preinstall-security-check)
- [Project homepage](https://github.com/marianachow0321/openclaw-preinstall-security-check)
- [Risk Scoring Reference](references/risk-scoring.md)
- [Sandbox Testing Procedure](references/sandbox-procedure.md)
- [Report Templates](references/report-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown security report with verdict, findings, and installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured JSON findings from sandbox review when deeper analysis is needed]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
