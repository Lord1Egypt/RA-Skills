## Description:

Use Context.dev through your OOMOL-connected account to search, retrieve, create, update, and manage Context.dev data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with Context.dev data through an OOMOL-connected account. It provides the action contracts and command patterns for read, write, and destructive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs a remote CLI installer that has not been verified and has no clear approval step.

Mitigation: Review and approve the CLI setup separately, and verify the installer before allowing fallback installation.

Risk: Context.dev write and destructive actions can change or remove account data.

Mitigation: Confirm the exact payload and effect before writes, and get explicit approval for destructive actions.

Risk: The hosted connector implementation has not been verified.

Mitigation: Review the connector before use and retain the skill's approval requirements for writes and deletions.

## Reference(s):

- [Context.dev](https://context.dev)
- [Context.dev API quickstart](https://docs.context.dev/quickstart)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and payloads are selected for the requested Context.dev action.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
