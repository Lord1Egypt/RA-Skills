## Description:

Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent operate the wacli CLI only for explicit WhatsApp actions, including contacting a third party or syncing and searching WhatsApp history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can authenticate, sync, search, and locally store private WhatsApp history.

Mitigation: Use the narrowest chat and date scope possible, consider an isolated --store path, and avoid continuous sync unless it is needed.

Risk: The skill installs an unpinned third-party wacli CLI.

Mitigation: Verify the upstream wacli package and installation source before installing or upgrading.

Risk: A message could be sent to the wrong recipient or with unintended content if the request is ambiguous.

Mitigation: Require an explicit recipient and message text, confirm both before sending, and ask a clarifying question when details are ambiguous.

## Reference(s):

- [wacli homepage](https://wacli.sh)
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-wacli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance to use wacli --json for machine-readable command output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
