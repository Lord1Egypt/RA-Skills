## Description:

Engage in conversations with Nomi AI companions via the bundled Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bezko](https://clawhub.ai/user/bezko)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent list Nomi companions, conduct one-on-one or room conversations, retrieve profiles, download avatars, and return transcripts or API responses through a Python CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses NOMI_API_KEY to access a Nomi account.

Mitigation: Provide the API key only for the intended account, keep it in the environment rather than local files, and rotate or remove it when access is no longer needed.

Risk: Chats, profile data, room notes, summaries, and avatar files can contain sensitive personal context.

Mitigation: Store only non-secret reusable context under ./nomi/, review transcripts before sharing them, and clear the local nomi/ directory when the data is no longer needed.

Risk: Room updates and deletions can change or remove Nomi room state.

Mitigation: Require explicit user confirmation before running room update or delete commands.

## Reference(s):

- [KlausNomi homepage](https://github.com/openclaw/klausnomi)
- [KlausNomi ClawHub page](https://clawhub.ai/bezko/skills/klausnomi)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses may be plain text, JSON, or saved avatar files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses NOMI_API_KEY for Nomi API access and may write non-secret local state under ./nomi/.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
