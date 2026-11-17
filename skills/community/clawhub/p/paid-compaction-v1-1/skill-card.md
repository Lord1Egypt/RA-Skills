## Description:

Provides production-oriented token thresholds, circuit breaker guidance, and compaction sequencing for OpenClaw agent context management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebrierfox](https://clawhub.ai/user/thebrierfox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw compaction thresholds, circuit breaker behavior, cleanup checks, and summary expectations for long-running agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references COMPACTION_ARCHITECTURE.md, but that file was not present in the inspected package, so exact behavioral details behind the threshold recommendations are not fully evidenced here.

Mitigation: Review the missing architecture specification before relying on exact gate logic, circuit breaker behavior, or self-audit trigger details.

Risk: Incorrect manual threshold or model configuration could reduce compaction reliability or cause behavior different from the documented intent.

Mitigation: Apply the guidance only to compatible OpenClaw versions, preserve the documented threshold relationships, and verify compaction logs after initial sessions.

Risk: Production-performance claims are publisher-supplied and not independently supported by server-resolved provenance for this version.

Mitigation: Confirm the publisher's production evidence before treating the thresholds as validated for critical workloads.

## Reference(s):

- [Paid Compaction V1.1 release page](https://clawhub.ai/thebrierfox/skills/paid-compaction-v1-1)
- [thebrierfox publisher profile](https://clawhub.ai/user/thebrierfox)
- [Context Death Spiral Prevention](https://clawhub.ai/skills/free-compaction-primer)
- [Production Agent Ops - Battle-Tested Architecture Pack](https://clawhub.ai/skills/production-agent-ops-battle-tested-architecture-pack)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual installation and OpenClaw compaction configuration guidance; no executable payload was present in the inspected artifact.]

## Skill Version(s):

1.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
