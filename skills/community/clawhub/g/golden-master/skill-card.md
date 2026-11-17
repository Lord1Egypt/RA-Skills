## Description:

Track source-of-truth relationships between files - know when derived content becomes stale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to identify source and derived file relationships, establish checksum tracking metadata, and validate when derived documentation or code-adjacent files become stale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read repository documentation or source files while analyzing source and derived relationships.

Mitigation: Install only in repositories where that file access is acceptable under the agent's trust boundary.

Risk: Suggested relationships and stale reports can be incomplete or misleading because relationship discovery requires human confirmation and checksums do not prove semantic correctness.

Mitigation: Review suggested relationships, checksum metadata, and stale reports before adding or refreshing Golden Master comments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/golden-master)
- [Source homepage](https://github.com/live-neon/skills/tree/main/pbd/golden-master)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON result objects and metadata comment snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checksum metadata and staleness reports; does not auto-modify files without explicit request.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter says 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
