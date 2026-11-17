## Description:

Language and NLP services for translation, text-to-speech, dictionaries, word tools, Bible text, and linguistic corpora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and query Pilot Protocol language-service agents for translation, dictionary lookup, text-to-speech voice catalogs, word tools, and related linguistic data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may be sent over Pilot Protocol to remote agents and upstream language or NLP providers.

Mitigation: Avoid sending secrets, credentials, confidential documents, or regulated personal data unless that sharing is acceptable for the use case.

Risk: Remote service responses may vary by provider, including dialect, register, freshness, and availability.

Mitigation: Use fresh list-agent discovery, read each agent's help contract before querying, and review returned data before relying on it.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-language)
- [Publisher profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and reachable remote language-service agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
