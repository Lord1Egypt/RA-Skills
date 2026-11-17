## Description:

Guides agents through building a minimal Tencent CloudBase Web and database demo with browser SDK CRUD, MCP-managed schema, a preview-first workflow, and cloud functions only when secrets, scheduled work, or rule limitations require them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binggg](https://clawhub.ai/user/binggg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and partner-host agent builders use this skill to quickly create minimal CloudBase Web demos such as message boards, Todo, Notes, and Kanban apps with direct browser-to-database CRUD. It is intended for BaaS-first prototypes where local preview and schema setup matter more than cloud-function middleware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct automatic template downloads and dependency installation during credential or trust setup.

Mitigation: Use a test tenant, review the template source and lockfile before relying on the generated app, and disable install scripts where possible.

Risk: The skill can direct agents to create CloudBase database schema or permission resources.

Mitigation: Review proposed schema and permission changes before applying them, especially outside disposable demo environments.

Risk: SessionStart hooks or connector changes may alter the agent environment before a demo is built.

Mitigation: Approve hook and connector changes explicitly before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binggg/skills/minimal-web-baas-demo)
- [WorkBuddy CLI hooks documentation](https://www.workbuddy.ai/docs/cli/hooks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create CloudBase schema resources, install template dependencies, configure hooks or connectors, and produce local preview instructions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.25.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
