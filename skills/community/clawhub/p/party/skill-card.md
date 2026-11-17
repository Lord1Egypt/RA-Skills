## Description:

Run a sequential multi-agent roundtable meeting. Use when the user invokes /party, asks for Party Mode, or wants several available agents to discuss a topic one at a time and produce a final transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshrajds](https://clawhub.ai/user/adarshrajds)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Party Mode Meeting to run a structured /party roundtable where available agents discuss a user-provided topic, react in sequence, and produce a concise transcript with a wrap-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive meeting topics may be shared across multiple available agents during the roundtable.

Mitigation: Review privacy expectations before using the skill with confidential or regulated topics.

Risk: Inviting several agents to discuss a topic can increase model usage costs.

Mitigation: Use the small 3-4 agent group described by the artifact and avoid unnecessary reactions when cost control matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshrajds/skills/party)
- [Project homepage](https://github.com/mixmash11/openclaw_agent_party)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown transcript with participant list, agent responses, optional reactions, and wrap-up summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; no tools, files, credentials, persistence, or external execution are requested.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
