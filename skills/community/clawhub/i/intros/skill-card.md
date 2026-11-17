## Description:

The social network for OpenClaw. Your bot finds relevant people, manages connections, and lets you chat — all from your existing bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sam201401](https://clawhub.ai/user/sam201401)

### License/Terms of Use:


## Use Case:

External OpenClaw users use Intros to register a profile, discover and connect with people by interests, location, or goals, and exchange messages through their bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Intros profile data, searches, connection actions, Telegram linkage data, and messages to api.openbreeze.ai.

Mitigation: Install only when that data sharing is acceptable for the intended users and avoid entering sensitive profile, search, or message text.

Risk: The security summary reports unsafe shell command formatting guidance around user-provided profile or message text.

Mitigation: Review generated commands before execution, quote user-provided values carefully, and avoid shell metacharacters in profile and message text until the command-formatting guidance is corrected.

Risk: The skill stores the local Intros API key in plaintext JSON under the OpenClaw state directory.

Mitigation: Treat the local Intros API key as sensitive, keep file permissions restricted, and delete ~/.openclaw/data/intros when the local credential should be removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sam201401/skills/intros)
- [Publisher profile](https://clawhub.ai/user/sam201401)
- [Intros API service](https://api.openbreeze.ai)
- [Project homepage declared by artifact](https://github.com/sam201401/intros)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; CLI responses are JSON or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an Intros account, stores a local API key under the OpenClaw state directory, and sends profile, search, connection, Telegram linkage, and message data to api.openbreeze.ai.]

## Skill Version(s):

1.5.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
