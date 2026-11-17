## Description:

Lists open Nano-paid tasks, shows their acceptance checks, and prepares GitHub issue claims for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhyabi2](https://clawhub.ai/user/dhyabi2)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators browse paid tasks, review acceptance checks, and prepare a GitHub issue claim with a Nano payout address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated GitHub CLI command can include unsafe shell characters from task IDs supplied by the task board.

Mitigation: Prefer the browser link or create the issue manually; inspect task IDs before running any printed shell command.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dhyabi2/skills/nano-paid-tasks)
- [Paid work task board](https://github.com/dhyabi2/paid-work-queue)
- [Task listings](https://raw.githubusercontent.com/dhyabi2/paid-work-queue/main/jobs.json)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists task details and acceptance checks; claim output includes a proposed issue, browser link, and optional GitHub CLI command. It does not submit a claim.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
