## Description:

Searches and navigates stored knowledge in memory palaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the skill to find concepts and information within or across memory palaces, follow cross-references, and retrieve stored review knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some referenced CLI files were unavailable to the scan, so its benign verdict is based on incomplete evidence.

Mitigation: Inspect the referenced CLI files and review the skill behavior before installing it.

Risk: The skill includes a PR review trigger alongside its knowledge search purpose, which may create a trigger conflict in some setups.

Mitigation: Review the trigger configuration and enable PR review search only where it is intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-memory-palace-knowledge-locator)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown retrieval guidance and search results, with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval depends on available indexed memory palaces and the configured companion skills.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
