## Description:

Miromind helps OpenClaw users run MiroMind deep research sessions through browser automation and save the resulting research as Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karminski](https://clawhub.ai/user/karminski)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to submit research questions to MiroMind, monitor the live chat session, and collect a local Markdown report with the completed findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation with reusable MiroMind account credentials.

Mitigation: Use a dedicated MiroMind account with a unique password and restrict access to OpenClaw configuration and output directories.

Risk: Research prompts and submitted data are sent to MiroMind.

Mitigation: Avoid submitting confidential or regulated data unless approved, and review MiroMind's data practices before use.

Risk: Completed reports may contain sensitive research content saved on the local machine.

Mitigation: Restrict access to output directories and periodically delete reports or session files that are no longer needed.

## Reference(s):

- [MiroMind](https://dr.miromind.ai)
- [OpenClaw](https://openclaw.ai)
- [ClawHub Miromind skill page](https://clawhub.ai/karminski/skills/miromind)
- [ClawHub publisher profile](https://clawhub.ai/user/karminski)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown report, research summary text, local report path, and MiroMind chat URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIROMIND_EMAIL and MIROMIND_PASSWORD; reports are saved locally after the MiroMind session completes.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
