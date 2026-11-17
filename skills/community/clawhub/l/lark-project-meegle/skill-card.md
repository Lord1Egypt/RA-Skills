## Description:

Connects to Lark Project / Meegle to query and manage work items, todos, comments, workflow transitions, attachments, and related project data through the Meegle CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kentonyu](https://clawhub.ai/user/kentonyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and support agents use this skill to inspect and update Lark Project / Meegle workspaces after confirming authorization and required project metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a mutable npm package with `@latest` for authenticated Meegle operations.

Mitigation: Prefer a pinned and reviewed CLI version before installation or production use.

Risk: The skill can read and change project data using the user's Meegle authorization.

Mitigation: Use least-privilege Meegle access and manually confirm create, update, comment, workflow, and attachment actions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kentonyu/skills/lark-project-meegle)
- [Meegle npm package](https://www.npmjs.com/package/@lark-project/meegle)
- [Command examples](references/api-examples.md)
- [Auth guard](references/auth-guard.md)
- [CLI guide](references/cli-guide.md)
- [URL kinds](references/url-kinds.md)
- [Work item metadata commands](references/workitem.md)
- [MQL syntax reference](references/mql-syntax.md)
- [Field value extras](references/field-value-extras.md)
- [Workflow commands](references/workflow.md)
- [Attachment commands](references/attachment.md)
- [View commands](references/view.md)
- [Performance guidance](references/performance.md)
- [Error handling](references/error-handling.md)
- [Rich text editor Markdown syntax](references/rich-text-editor-markdown-syntax.md)
- [Miscellaneous commands](references/misc.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, JSON]

**Output Format:** [Markdown guidance with CLI commands and structured command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs follow the user's language when possible and may include Meegle CLI JSON, NDJSON, or summarized query results.]

## Skill Version(s):

0.1.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
