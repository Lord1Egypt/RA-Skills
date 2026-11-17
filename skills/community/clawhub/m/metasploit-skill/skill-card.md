## Description:

Plan and execute authorized Metasploit assessments for OpenClaw tasks with repeatable workflows, including target triage, exploit module selection, option tuning, .rc generation, controlled execution, and evidence-focused reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengyuxiu](https://clawhub.ai/user/zengyuxiu)

### License/Terms of Use:

MIT-0

## Use Case:

External security testers and developers use this skill to plan and document authorized Metasploit assessments, including scoping, module and payload selection, reviewable .rc generation, controlled execution, evidence capture, and remediation reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .rc files can include unsafe extra Metasploit commands if crafted argument values are accepted.

Mitigation: Review every generated .rc file before running it in msfconsole, and use only module, payload, host, path, and option values that were typed and validated by the operator.

Risk: Metasploit execution can affect systems outside approved authorization or scope.

Mitigation: Confirm target ownership, in-scope hosts, allowed ports, testing window, and prohibited techniques before selecting modules or generating execution scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengyuxiu/skills/metasploit-skill)
- [Module Selection Heuristics](references/module-selection.md)
- [Execution and Reporting Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands and generated Metasploit .rc content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewable Metasploit resource scripts and concise assessment reports; generated .rc files require manual review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
