## Description:

Controls the Morfeo UGC Engine from OpenClaw or Telegram to generate and manage Argentine-brand UGC videos from script creation through draft publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Content operators and developers use this skill from OpenClaw or Telegram to create, inspect, advance, regenerate, select shots for, and prepare draft social posts for Morfeo UGC Engine runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes an admin access token for the local Morfeo API.

Mitigation: Rotate the token, remove it from the skill content, and supply credentials through a protected environment variable or secret store.

Risk: Chat-driven actions can create runs, advance stages, regenerate script fields, select shots, and create Postiz drafts.

Mitigation: Restrict the skill to trusted operators and require explicit confirmation before create, advance, regenerate, shot-selection, and draft publication actions.

Risk: PM2 maintenance commands can restart or start the local engine service.

Mitigation: Separate service maintenance privileges from routine content workflow use and limit PM2 access to authorized maintainers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/morfeo-ugc-engine)
- [Publisher profile](https://clawhub.ai/user/pauldelavallaz)
- [Morfeo Engine repository](https://github.com/PauldeLavallaz/morfeo-engine)
- [Morfeo Engine dashboard](https://morfeo-engine-ui.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, curl, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing instructions and API call examples for a local Morfeo Engine service; does not directly produce video files by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
