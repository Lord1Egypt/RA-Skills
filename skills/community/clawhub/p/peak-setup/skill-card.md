## Description:

Move a repository's GitHub Actions jobs to Peak runners. Use when the user asks to set up Peak, speed up CI, switch runners to Peak, or run `peak init`. Runs the Peak CLI in agent mode, relays the sign-in link, and returns the pull request link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aperswal](https://clawhub.ai/user/aperswal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate GitHub Actions jobs to Peak runners, guide sign-in and blocking-resolution steps, and return the pull request created by the Peak CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs mutable remote npm packages for Peak setup.

Mitigation: Review the skill before installing and prefer pinned or otherwise verified CLI versions before execution.

Risk: Selected GitHub Actions workflow files can be uploaded to Peak during hard-job handling.

Mitigation: Run it only in repositories where sharing selected workflow files with Peak is acceptable.

Risk: Repository secrets or broad environment credentials could be exposed if the execution environment is not controlled.

Mitigation: Avoid exposing broad environment secrets and never print, log, store, or echo tokens.

## Reference(s):

- [Peak Quickstart Documentation](https://docs.peak.inc/quickstart)
- [Peak Homepage](https://peak.inc)
- [ClawHub Skill Page](https://clawhub.ai/aperswal/skills/peak-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and JSON event-handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relays Peak authorization details and pull request links; the user remains responsible for merging the pull request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
