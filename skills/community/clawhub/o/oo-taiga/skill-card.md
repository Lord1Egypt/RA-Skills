## Description:

Taiga (taiga.io). Use this skill for ANY Taiga request — reading, creating, updating, and deleting data. Whenever a task involves Taiga, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working in Taiga use this skill to inspect projects, issues, tasks, and user stories, and to create or update them through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup directs the agent to run a remote installer, and the installer contents could not be inspected.

Mitigation: Approve dependency setup separately and use a fixed, verified release before running an installer.

Risk: The CLI may install or update other agent skills during setup.

Mitigation: Check whether setup changes other skills before allowing it.

Risk: Taiga requests and connected-service credentials are mediated by OOMOL.

Mitigation: Use an appropriately limited Taiga account.

## Reference(s):

- [Taiga](https://taiga.io)
- [Taiga API documentation](https://docs.taiga.io/api.html)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and Taiga action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require user confirmation; destructive updates require explicit approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
