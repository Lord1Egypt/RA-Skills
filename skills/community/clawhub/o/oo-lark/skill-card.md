## Description:

Use the connected Lark account to read, create, update, and delete Lark data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Lark through a connected account can ask the agent to find information and manage Lark data such as documents, chats, tasks, calendars, and spreadsheets. The skill guides the agent to inspect each action's input schema before submitting a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions run a remote installer whose behavior the scan could not verify; the scan was partial and some referenced local paths were missing.

Mitigation: Use an independently verified, versioned installer or an already trusted oo CLI; avoid installation until the installer can be reviewed or replaced with a trusted method.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-lark)
- [Lark API Documentation](https://open.larksuite.com/document/home/index)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Structured connector requests and responses, with user-facing text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies by Lark action; the skill marks state-changing operations for confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
