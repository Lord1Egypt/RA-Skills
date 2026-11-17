## Description:

Memory Ebbinghaus manages AI agent memory with Ebbinghaus-style strength decay, review reinforcement, archiving, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subcoldzhang](https://clawhub.ai/user/subcoldzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain local memory records, identify fading memories, and decide whether to review, archive, or delete stale items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memory records or archive entries may later reappear in agent context.

Mitigation: Keep database and archive paths pointed at intended files, review records before archiving, and avoid storing untrusted instructions or sensitive data unless reuse in future context is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subcoldzhang/skills/memory-ebbinghaus)
- [Publisher profile](https://clawhub.ai/user/subcoldzhang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Terminal text, Markdown archive entries, and JSON memory database files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local file paths configured through EBBINGHAUS_DB and EBBINGHAUS_ARCHIVE.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
