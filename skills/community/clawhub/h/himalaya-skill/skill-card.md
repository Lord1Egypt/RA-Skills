## Description:

Expert guidance for querying, writing, and managing emails using the `himalaya` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bird-frank](https://clawhub.ai/user/bird-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email users use this skill to construct and review Himalaya CLI commands for listing and searching email, composing messages, and managing flags, folders, templates, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated guidance may include send, reply, forward, delete, purge, or expunge email actions.

Mitigation: Review account, folder, message IDs, recipients, and all send or destructive actions before allowing any generated command to run.

Risk: Broad email search and management commands may target the wrong account, folder, message, or recipient if parameters are incorrect.

Mitigation: Validate generated Himalaya query strings, account flags, folder flags, message IDs, and recipients against the intended mailbox before execution.

## Reference(s):

- [Bundled Query DSL Reference](references/query_dsl.md)
- [Himalaya Repository](https://github.com/pimalaya/himalaya)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-response guidance with commands for a user to review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
