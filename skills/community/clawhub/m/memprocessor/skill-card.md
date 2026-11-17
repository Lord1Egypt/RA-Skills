## Description:

Enables AI agents to develop independent, evolving personas through organic memory growth, self-reflection, and layered memory management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfanmy](https://clawhub.ai/user/zfanmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Memory Processor to provide agents with persistent memory, semantic recall, persona generation, persona evolution, and reflection through a local FastAPI service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and persona controls are exposed without authentication by default.

Mitigation: Run only on localhost or behind strong authentication before connecting it to real agents or user data.

Risk: Stored memories or generated persona histories may contain sensitive personal data or secrets.

Mitigation: Avoid storing sensitive data until deletion, redaction, retention, and access-control policies are implemented and tested.

Risk: Unpinned dependencies and model revisions can change runtime behavior or introduce supply-chain risk.

Mitigation: Pin dependencies and model revisions before production or commercial deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zfanmy/skills/memprocessor)
- [README](artifact/README.md)
- [Skill overview](artifact/SKILL.md)
- [Version isolation notes](artifact/VERSION-ISOLATION.md)
- [Changelog](artifact/CHANGELOG.md)
- [Python project metadata](artifact/pyproject.toml)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP API examples, JSON API responses, Python service code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a local FastAPI memory and persona service with persistent storage layers and semantic search.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
