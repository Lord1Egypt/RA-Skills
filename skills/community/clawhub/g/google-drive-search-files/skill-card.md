## Description:

Atomic node skill to search for files in Google Drive using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to locate files in Google Drive by running a Google Drive search through the local gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command template leaves user-provided search text unsafe to insert into a shell command.

Mitigation: Execute gog with an argument-array style call and pass the search query as one literal argument.

Risk: The skill depends on the local gog CLI configuration and its Google Drive access.

Mitigation: Install only where the gog CLI setup is trusted and its account permissions are appropriate for the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-drive-search-files)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON]

**Output Format:** [Markdown guidance with an inline shell command; the command returns a JSON array of matching Google Drive file objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local gog CLI setup with access to Google Drive.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
