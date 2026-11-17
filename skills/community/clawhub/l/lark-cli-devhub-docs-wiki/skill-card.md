## Description:

Use when organizing Feishu/Lark Wiki spaces or Docs through lark-cli or feishu-cli for a development knowledge hub, including project pages, design notes, runbooks, bug retrospectives, and long-form artifacts linked from Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to organize Lark or Feishu Docs and Wiki spaces for development knowledge hubs. It helps structure project pages, design notes, runbooks, retrospectives, decisions, and linked long-form artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose document creation or Wiki placement commands that affect authenticated Lark or Feishu workspaces.

Mitigation: Review generated document content, target space IDs, and creation commands before running them.

Risk: Long-form pages may include raw logs or sensitive operational details if users provide them.

Mitigation: Keep raw logs short and safe, and review page content before publishing it to Docs or Wiki spaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afengzi/skills/lark-cli-devhub-docs-wiki)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated lark-cli or compatible feishu-cli workflow.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
