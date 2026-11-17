## Description:

GoList helps an agent manage GoList grocery lists through a CLI for creating, joining, switching, sharing, reading, and updating shopping lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel17903](https://clawhub.ai/user/daniel17903)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to operate GoList shopping lists from an agent session, including list creation, item updates, sharing, and joining shared lists. It is intended for low-friction grocery list workflows backed by the GoList API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically creates and displays share links after new lists, which may expose list access if shared unintentionally.

Mitigation: Review generated share links before sending them onward and use the skill only when automatic sharing is acceptable.

Risk: Shopping list contents and list or device identifiers may be private and are sent to GoList or stored in local CLI state.

Mitigation: Avoid entering sensitive list contents and protect or limit access to the local state file before use.

## Reference(s):

- [ClawHub GoList skill page](https://clawhub.ai/daniel17903/skills/golist)
- [GoList app](https://go-list.app/)
- [GoList API endpoint](https://go-list.app/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local CLI state and send requests to the fixed GoList API endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
