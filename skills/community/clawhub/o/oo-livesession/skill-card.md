## Description: <br>
LiveSession (livesession.io) supports searching and reading LiveSession session replay data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to list LiveSession session replays with pagination and common filters through the OOMOL `oo` CLI. It is intended for read-only LiveSession requests where the agent should inspect the live connector schema before running an action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session listings may expose customer or visitor activity data from LiveSession. <br>
Mitigation: Install and use the skill only in workspaces where agent access to LiveSession replay metadata is appropriate. <br>
Risk: Expired credentials, missing scopes, or billing limits can prevent connector execution. <br>
Mitigation: Use the documented OOMOL setup and troubleshooting steps only after an action fails for the matching reason. <br>


## Reference(s): <br>
- [LiveSession homepage](https://livesession.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only connector responses are returned as JSON from the `oo` CLI, including data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
