## Description:

Natural language task and list management for MyLister through its public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mgoettel13](https://clawhub.ai/user/mgoettel13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to manage MyLister.dev task lists through natural language commands, including creating, viewing, updating, sharing, exporting, emailing, and deleting list data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change MyLister task data, including deleting items, notes, comments, attachments, and lists.

Mitigation: Require explicit confirmation before destructive actions and review affected list or item identifiers before execution.

Risk: The skill can share lists, change collaborator permissions, email data, and export list or item content.

Mitigation: Confirm recipients, permission levels, export formats, and whether archived content is included before sending or sharing data.

Risk: The skill supports runtime API keys and configurable API base URLs.

Mitigation: Set API keys through environment variables, avoid entering keys in prompts, and use only trusted MyLister API hosts.

Risk: The skill can upload local files and request file URLs.

Mitigation: Confirm each upload path and file URL request, and avoid uploading files that contain sensitive or unrelated local data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mgoettel13/skills/mylister-skill)
- [Server-resolved source repository](https://github.com/mgoettel13/myLister-Skill)
- [MyLister API documentation](https://api.mylister.dev/docs)
- [MyLister app](https://app.mylister.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands]

**Output Format:** [Natural-language command responses with optional JSON or HTML export results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MyLister API credentials and may mutate, share, email, export, or upload user task data.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence; artifact package.json and skill.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
