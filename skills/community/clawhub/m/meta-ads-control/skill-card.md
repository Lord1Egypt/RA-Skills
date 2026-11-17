## Description:

Use this skill when the user wants to inspect, report on, create, update, pause, resume, budget, target, upload assets for, or troubleshoot Meta, Facebook, or Instagram ads via the Marketing API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT

## Use Case:

Developers, marketers, and operations teams use this skill to inspect Meta ad accounts, run performance reports, create or update campaign structures, manage delivery status, adjust budgets, resolve targeting IDs, upload assets, and troubleshoot Meta Marketing API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meta bearer tokens could be exposed to untrusted hosts if custom graph bases, full request URLs, or unexpected pagination URLs are used.

Mitigation: Use tightly scoped Meta tokens, keep requests on trusted Meta HTTPS hosts, avoid custom META_GRAPH_BASE values and full URLs unless host allowlisting is fixed, and rotate any token used with untrusted URLs.

Risk: Live ad changes can spend money, alter delivery, affect tracking, or archive objects.

Mitigation: Read the target objects first, run dry-run commands, require explicit approval before confirmed writes, default new delivery objects to PAUSED, and verify state after mutation.

Risk: Special ad categories such as housing, employment, credit, social issues, elections, or politics can have additional policy and targeting restrictions.

Mitigation: Confirm whether a special category applies and review account category settings and policy requirements before creating or modifying targeting or delivery.

## Reference(s):

- [API Guide](references/API-GUIDE.md)
- [Field Sets and Reporting Defaults](references/FIELDS.md)
- [Workflow Playbook](references/WORKFLOWS.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [OpenClaw Notes](references/OPENCLAW.md)
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/meta-ads-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request payloads, and structured API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dry-run and confirmed API operations; bundled commands can emit JSON and write report output files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
