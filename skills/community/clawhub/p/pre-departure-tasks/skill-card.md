## Description:

Guides an agent through preparing for travel or other long offline periods by inventorying scheduled automations, creating a durable pre-departure checklist, running selected output-producing tasks early, adding redundant triggers, and recording return checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hechunxian](https://clawhub.ai/user/hechunxian)

### License/Terms of Use:

MIT-0

## Use Case:

Personal productivity and WorkBuddy users use this skill before planned or likely offline periods to preserve scheduled task outputs, prevent duplicate sends after return, and create a checklist for recovery. It is especially relevant when automations depend on a local host being online.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can touch local state, automation prompts, scripts, and outbound email records.

Mitigation: Ask for a dry-run list of files, automations, scripts, and outbound emails before making changes, then require explicit approval for email sends and persistent automation changes.

Risk: Broad travel or offline phrasing could trigger the workflow when the user only intended discussion or planning.

Mitigation: Confirm the intended offline window and requested action before executing tasks or writing checklist state.

Risk: Incorrect assumptions about offline backfill can lead to missed task outputs or duplicate return-time output.

Mitigation: Use the pre-departure checklist as the source of truth, record duplicate-prevention markers, and review the return checklist item by item.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hechunxian/skills/pre-departure-tasks)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklist tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local checklist files, shared state notes, TODO or QUICK_INDEX entries, logs, automation prompts, and user-approved email-send records.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
