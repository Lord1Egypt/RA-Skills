## Description:

Use static route analysis plus runtime cron delivery audit to validate OpenClaw cron notification wiring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw cron notification routing, compare static route checks with runtime delivery results, and identify mismatches or silent delivery failures without sending test messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled audit script writes potentially sensitive cron routing results to predictable files in /tmp.

Mitigation: Review the helper script before use, run it only on a trusted single-user host, or modify it to use mktemp with restrictive permissions and cleanup.

Risk: The audit reads local OpenClaw cron configuration and runtime delivery files that may contain sensitive routing details.

Mitigation: Inspect the referenced local files before execution and avoid running as root unless required to read the OpenClaw files.

## Reference(s):

- [OpenClaw Route Check Repository](https://github.com/pfrederiksen/openclaw-route-check)
- [GitHub Publish Notes](references/github-publish-notes.md)
- [Publish Checklist](references/publish-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/pfrederiksen/skills/openclaw-route-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, route findings, delivery audit summaries, and proposed configuration changes.]

## Skill Version(s):

0.1.1 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
