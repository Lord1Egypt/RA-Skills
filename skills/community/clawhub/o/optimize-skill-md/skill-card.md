## Description:

Optimizes existing SKILL.md files against the Skills MD standard format by improving descriptions, section organization, concision, and formatting consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit, rewrite, and standardize SKILL.md files before release or library-wide maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may rewrite target SKILL.md files to include RedFox API-key instructions.

Mitigation: Review generated diffs before accepting changes, especially authentication sections and external service references.

Risk: The skill may report usage to RedFox using a bundled key or REDFOX_API_KEY.

Mitigation: Install only where external usage reporting is permitted, and remove or disable the reporting step when policy requires local-only operation.

Risk: Credential-handling guidance in generated content could affect how users expose or configure API keys.

Mitigation: Verify that generated API-key instructions match organizational secret-management policy before release.

## Reference(s):

- [Skills MD Standard Format](artifact/references/standard-format.md)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/optimize-skill-md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with edited SKILL.md content, change summary, line-count statistics, and occasional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write changes to the target SKILL.md and may invoke a RedFox usage-recording script after optimization.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
