## Description:

Queries published MaxKB agents so an LLM can choose one, then sends a question to the selected agent and returns its answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuruibin](https://clawhub.ai/user/liuruibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route user questions to published MaxKB agents in a configured workspace and return the selected agent's answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and MaxKB credentials can be sent to an operator-configured endpoint that is not required to use HTTPS.

Mitigation: Use only a trusted HTTPS MaxKB endpoint, avoid non-loopback HTTP, protect the .env file, and use a least-privileged service account or scoped token.

Risk: Questions routed through this skill are sent to the configured MaxKB server.

Mitigation: Treat routed questions as data shared with that MaxKB deployment and avoid sending content that the server is not authorized to process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuruibin/skills/maxkb)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON strings containing published agent metadata or the selected agent answer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a single response for each invocation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
