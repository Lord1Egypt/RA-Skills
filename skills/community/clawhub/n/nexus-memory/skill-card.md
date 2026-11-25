## Description:

Persistent memory for Claude Code and supported agent harnesses, with automatic recall before prompts and capture after turns, backed by Qdrant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neboy72](https://clawhub.ai/user/neboy72)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Nexus Memory to recall project context and save facts, decisions, and session summaries across Claude Code and supported agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maintenance-generated memories can lack an individual agent attribution.

Mitigation: When attribution matters, filter entries written by consolidation or dreaming, as documented by the skill.

Risk: Automatic capture can retain sensitive details in persistent shared memory.

Mitigation: Tell users what will be stored and avoid saving passwords, tokens, or payment-card data.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/neboy72/skills/nexus-memory)

## Skill Output:

**Output Type(s):** [Text, Guidance, Structured data]

**Output Format:** [Memory excerpts and structured tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automatic recall is limited to three entries and an 800-character budget per prompt.]

## Skill Version(s):

0.1.17 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
