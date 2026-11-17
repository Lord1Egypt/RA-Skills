## Description:

Helps authors plan and generate long-form Chinese fiction with character, world-building, outline, chapter generation, and writing-style controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanbinsite](https://clawhub.ai/user/hanbinsite)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and developers use this skill to plan Chinese long-form fiction projects, manage character, world, outline, and chapter state, and generate or regenerate chapters through an OpenAI-compatible LLM provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling or regeneration behavior could overwrite local novel project files.

Mitigation: Run the skill in an isolated workspace, keep backups before regeneration or batch generation, and review output paths before writing or exporting files.

Risk: Custom API settings could send drafts, outlines, character notes, summaries, or API keys to an unintended service.

Mitigation: Set NOVEL_API_BASE_URL only to a trusted HTTPS provider and provide NOVEL_API_KEY through environment variables rather than checked-in configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanbinsite/skills/my-novel-writer)
- [README](artifact/README.md)
- [Novel structure guide](artifact/guides/novel_structure_guide.md)
- [Chapter outline template](artifact/templates/chapter_outline.md)
- [Character card template](artifact/templates/character_card.md)
- [World-building template](artifact/templates/world_building.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with CLI commands, JSON configuration and examples, and generated chapter text or files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated chapters, outlines, project memory, logs, and exports may be written to local files in the configured workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
