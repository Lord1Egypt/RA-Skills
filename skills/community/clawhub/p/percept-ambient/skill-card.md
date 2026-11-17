## Description:

Continuously captures and summarizes ambient conversations to build a local knowledge graph for context-aware assistance without explicit commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis563](https://clawhub.ai/user/jarvis563)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to maintain passive, local conversation memory so agents can retrieve relevant people, project, decision, and relationship context during later work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for always-on conversation capture and searchable memory, which can expose sensitive participant, project, and relationship context if enabled without clear consent and access controls.

Mitigation: Enable only in approved spaces or sessions with opt-in recording, visible status indication, participant consent, local authentication, encryption, retention limits, and easy pause, export, and permanent deletion controls.

Risk: Searchable ambient transcripts and derived knowledge graphs can retain context longer than users expect.

Mitigation: Configure TTL auto-purge and review privacy settings before deployment so retained transcripts and derived entities match the intended retention policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarvis563/skills/percept-ambient)
- [Project link listed in skill artifact](https://github.com/GetPercept/percept)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local context packets, entity and relationship context, search guidance, and dashboard usage details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
