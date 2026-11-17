## Description:

Provides a neuroscience-inspired 6-tier automated memory system with WAL protocol, semantic search, emotional tagging, and value-based retention for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add persistent local memory, session recall, search, diary notes, error learning, and neuroscience-inspired ranking to OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain sensitive agent history in local memory files.

Mitigation: Do not store secrets in memory entries, and review memory files before loading them into future sessions.

Risk: The ACC cron pipeline can send transcript snippets to configured model command-line tools.

Mitigation: Use local models or redaction, and avoid enabling the default Claude command unless transcript sharing is acceptable.

Risk: Learned or unsanitized content can be fed back into future sessions.

Mitigation: Review ACC_STATE.md and other generated state files before using them as session context.

Risk: Cleanup and maintenance commands may affect diary or daily memory files.

Mitigation: Back up diary and daily files before running cleanup or maintenance workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/broedkrummen/skills/overkill-memory-system)
- [Overkill Memory System README](artifact/README.md)
- [Overkill Memory System Skill Documentation](artifact/SKILL.md)
- [Final Architecture](artifact/FINAL_ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with inline shell commands, Python code references, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory files, search results, diary entries, state summaries, and learned correction records when installed and run.]

## Skill Version(s):

1.9.5 (source: server release evidence; artifact metadata and SKILL.md mention 1.9.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
