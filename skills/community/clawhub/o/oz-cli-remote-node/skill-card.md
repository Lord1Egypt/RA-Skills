## Description:

Execute commands or tasks on the Oz Build Node through the Oz CLI, with mode-based control and direct bash command support on a remote node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route Oz prompts and explicit shell commands to a configured remote node where oz-cli is installed. It supports remote task execution, profile selection, shared-session flags, and local tracking records for Oz runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute arbitrary shell commands on a named remote node.

Mitigation: Install only when remote command execution is intended, grant node access narrowly, and review commands before sending them to the remote node.

Risk: Oz prompts, run IDs, and Oz URLs may be persisted in local tracking files.

Mitigation: Avoid including secrets in prompts, restrict workspace access, and review generated tracking files before sharing or committing them.

Risk: The --share flag can expose an Oz session to teammates.

Mitigation: Use --share only when collaboration is intended and the session contents are appropriate for the receiving audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eladrave/skills/oz-cli-remote-node)
- [ClawHub publisher profile](https://clawhub.ai/user/eladrave)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and run-tracking file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local oz_run.<id>.md tracking files containing run metadata, prompts, and Oz URLs.]

## Skill Version(s):

1.1.3 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
