## Description:

Mia Content Creator is a local CLI for template-based social post drafting, schedule previewing, and basic local analytics across Moltbook and Twitter/X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arubiku](https://clawhub.ai/user/arubiku)

### License/Terms of Use:

MIT

## Use Case:

External creators and agents can use this skill to draft template-based social posts for Moltbook or Twitter/X, preview simple posting schedules, and summarize locally logged post history. It is best treated as a content-template helper rather than a live publishing or monetization integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated post history is written to content-log.json in the directory where the CLI runs.

Mitigation: Run the skill in a non-sensitive working directory or remove content-log.json when local post history should not be retained.

Risk: The artifact behaves as a local post generator and does not provide real automated publishing or monetization integrations.

Mitigation: Treat generated content, schedule previews, and analytics as local helper output unless separate platform integrations are added and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arubiku/skills/mia-content-creator)
- [Publisher profile](https://clawhub.ai/user/arubiku)
- [Moltbook profile](https://moltbook.com/u/MiaBloomx)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [CLI text and JSON objects for generated posts, schedule previews, and analytics summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a local content-log.json file in the current working directory when generating posts.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
