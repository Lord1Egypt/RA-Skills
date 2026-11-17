## Description:

Captures learnings, errors, and corrections to enable continuous improvement across agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lipairui](https://clawhub.ai/user/lipairui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture corrections, command failures, knowledge gaps, feature requests, and reusable best practices as structured workspace learning logs. It also guides review and promotion of broadly useful learnings into agent memory or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived learnings can persist sensitive, incorrect, or overly broad guidance into future agent sessions.

Mitigation: Review each learning before writing or promoting it, and avoid saving secrets, raw prompts, customer data, full transcripts, or unnecessary stack traces.

Risk: Global hooks and cross-session sharing can spread low-quality or sensitive learning content beyond the current task.

Mitigation: Keep installation project-scoped where possible, make hooks opt-in, and review shared or promoted entries before they affect other sessions.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [ClawHub release page](https://clawhub.ai/lipairui/skills/perrytest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-scoped learning entries and optional hook or skill-scaffold outputs when configured by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
