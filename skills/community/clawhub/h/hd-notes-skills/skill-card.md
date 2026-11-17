## Description:

话袋笔记 Skill helps agents create, update, and search personal notes through the Huadai OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monkeydb](https://clawhub.ai/user/monkeydb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to connect a compatible agent to Huadai Notes so it can save new notes, search existing notes, and update confirmed notes through the Huadai OpenAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts may execute unintended local code when handling note identifiers.

Mitigation: Review before installing and avoid arbitrary or externally supplied note IDs until upload.sh and update.sh serialize unique_id safely.

Risk: The Huadai API key can be sent to an overridden endpoint if HUADAI_BASE_URL points away from Huadai.

Mitigation: Use only a Huadai API key you are comfortable exposing to this skill and do not set HUADAI_BASE_URL to a non-Huadai host.

## Reference(s):

- [API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/monkeydb/skills/hd-notes-skills)
- [ClawHub Marketplace Page](https://clawhub.ai/monkeydb/hd-notes-skills)
- [Huadai Open Platform](https://ihuadai.cn/desktop/openai)
- [Huadai OpenAPI Base URL](https://openapi.ihuadai.cn/open/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with shell commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HUADAI_API_KEY for authenticated Huadai OpenAPI calls.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package metadata report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
