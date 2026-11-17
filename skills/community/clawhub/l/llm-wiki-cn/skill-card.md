## Description:

用于构建、维护、查询、归档和体检一个由 LLM 持续维护的 Markdown / Obsidian 知识 Wiki。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengsusky](https://clawhub.ai/user/fengsusky)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to initialize and maintain a Markdown / Obsidian Knowledge wiki, import source materials, update structured wiki pages, answer from the wiki, archive durable answers, and audit links, coverage, indexes, and encoding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update a user-designated Knowledge wiki and may change curated notes if granted broad write access.

Mitigation: Grant access only to the intended Knowledge directory and keep source materials read-only unless you explicitly want them changed.

Risk: Bulk renaming or restructuring can break wiki links, index coverage, or source-page mappings.

Mitigation: Review restructuring plans before approval and run the packaged wiki verification script after batch imports, renames, or theme-map updates.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fengsusky/skills/llm-wiki-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown wiki pages, concise text responses, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains Obsidian-style wikilinks, index/log entries, and verification reports.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
