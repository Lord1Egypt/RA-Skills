## Description:

Operate WeCom Bot through an OOMOL-connected account to read and manage chats, messages, documents, schedules, meetings, todos, sheets, and pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use the skill to manage WeCom communications and collaboration data through an agent connected to their WeCom account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may silently install or update other agent skills without disclosing those changes.

Mitigation: Review the CLI setup, use a verified release, and consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking it, as described in the CLI environment-variable reference.

Risk: The connector can read or change WeCom business data, and OOMOL mediates access to that data.

Mitigation: Connect only the intended WeCom account and confirm the exact target and effect before any write or deletion.

## Reference(s):

- [WeCom Bot](https://work.weixin.qq.com)
- [WeCom API documentation](https://developer.work.weixin.qq.com/document/path/91770)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown]

**Output Format:** [Connector results as structured JSON, text, or Markdown; CLI instructions may use Markdown code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the selected WeCom action; write actions change account data and require confirmation before execution.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
