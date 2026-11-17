## Description:

Manages persistent caller memory by retrieving caller context at call start and saving call summaries, identity facts, communication style, and memories after calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noahvandal](https://clawhub.ai/user/noahvandal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators building ClawdTalk or OpenClaw calling agents use this plugin to load caller context before a call and persist useful caller memory after the call ends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses sensitive caller memory, including call summaries, identity facts, and persona observations.

Mitigation: Install only with caller notice or consent, clear retention and deletion rules, and limits on what transcript-derived details are stored.

Risk: A misconfigured or untrusted Persona API endpoint could expose caller memory or API credentials.

Mitigation: Use a trusted endpoint, prefer HTTPS for non-local servers, restrict who can configure the endpoint, and protect the API key as sensitive configuration.

Risk: Persistent persona updates can accumulate incorrect, stale, or overly sensitive information.

Mitigation: Review saved summaries and persona updates, avoid unnecessary sensitive details, and provide a process to correct or delete caller records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noahvandal/skills/persona-plugin)
- [Publisher profile](https://clawhub.ai/user/noahvandal)
- [Skill instructions](artifact/SKILL.md)
- [Plugin manifest](artifact/openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON-formatted text from Persona API tool calls, with caller-context guidance for the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Persona API key, a configured Persona API endpoint, and E.164 caller phone numbers.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
