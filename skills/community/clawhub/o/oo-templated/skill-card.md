## Description: <br>
Templated (templated.io). Use this skill for ANY Templated request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Templated account, template, and render workflows through an OOMOL-connected account. It supports read actions as well as guarded render creation and render deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a connected account and requires sensitive credentials to be available through OOMOL. <br>
Mitigation: Use the OOMOL-connected account flow so raw tokens are not handled by the agent, and run setup steps only after an authentication or connection failure. <br>
Risk: Templated render creation changes account state and render deletion removes data. <br>
Mitigation: Confirm the exact payload and expected effect before write actions, and require explicit approval before destructive delete actions. <br>
Risk: Generated connector commands may fail or act on the wrong schema if action inputs are assumed. <br>
Mitigation: Fetch the live connector schema before constructing each action payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-templated) <br>
- [Templated homepage](https://templated.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the oo CLI and return connector responses as JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
