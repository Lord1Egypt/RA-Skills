## Description: <br>
Sentry lets an agent read and update Sentry issues, alerts, releases, replays, projects, integrations, and related organization data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Sentry projects, issues, events, releases, alerts, integrations, replays, and Sentry Apps, and to update issue attributes after confirming the requested change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Sentry data through OOMOL-connected credentials. <br>
Mitigation: Install it only when the agent should access the relevant Sentry organizations and projects. <br>
Risk: The update_issue action can change Sentry issue state, assignment, or bookmark fields. <br>
Mitigation: Confirm the target issue, requested attributes, and exact payload before running state-changing actions. <br>
Risk: First-time setup may involve installing the oo CLI. <br>
Mitigation: Verify or install the CLI through a trusted method before running connector commands. <br>


## Reference(s): <br>
- [ClawHub Sentry skill](https://clawhub.ai/oomol/oo-sentry) <br>
- [Sentry homepage](https://sentry.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
