## Description:

Use the Parallel connector for Parallel requests, including web search, content extraction, task creation, and task result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to search the web, extract content from public URLs, and create or retrieve Parallel task runs through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can make broader local changes than the skill explains, and may install additional agent skills.

Mitigation: Review setup first, use a separately reviewed CLI version, and disable automatic skill synchronization unless you want additional skills installed.

Risk: Task data is sent through OOMOL to Parallel, and the downloaded installers and live connector implementation were unavailable for verification.

Mitigation: Confirm that sending the data through OOMOL is acceptable and review the CLI distribution and connector before use.

Risk: Task creation changes Parallel state.

Mitigation: Get user approval for the exact task payload before running a state-changing action.

## Reference(s):

- [Parallel API documentation](https://docs.parallel.ai/)
- [Parallel](https://parallel.ai)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-parallel)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use their live connector schema; results may include text or structured data.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
