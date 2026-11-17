## Description:

Pindou Skill helps an agent turn a photo or text description into a printable Perler bead-style pixel grid with color codes and a bill of materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciawevy](https://clawhub.ai/user/ciawevy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, makers, and developers use this skill in an agent to collect bead-pattern preferences, generate or edit a pixel image, map it to a MARD 221 palette, and produce printable pattern assets and a purchase list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photos, prompts, masks, and API credentials may be sent to api.bianxie.ai by default.

Mitigation: Use the skill only with data appropriate for that endpoint, switch to a trusted endpoint when needed, and avoid processing sensitive personal or copyrighted images without clear consent.

Risk: The documentation recommends putting API keys directly in source files.

Mitigation: Prefer environment variables or a secret manager, and avoid committing real credentials to the skill directory.

Risk: The installation guidance uses unpinned Python dependencies.

Mitigation: Install in a virtual environment and pin dependency versions before using the skill in repeatable or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ciawevy/skills/pindou-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [OpenAI Images API guide](https://platform.openai.com/docs/guides/images)
- [MARD 221 palette](artifact/palettes/mard_221.csv)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown instructions with JSON configuration examples and Python command snippets; workflow outputs include PNG, SVG, CSV, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before image selection or retries; image generation may use a third-party relay endpoint by default.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
