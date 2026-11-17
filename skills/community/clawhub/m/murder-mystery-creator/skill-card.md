## Description:

Murder Mystery Creator helps agents generate complete murder mystery game packages from a requested theme, style, player count, or reference work, including plot outlines, character cards, clue cards, host materials, visual assets, and an interactive HTML view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongsunyanming](https://clawhub.ai/user/gongsunyanming)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to draft playable murder mystery scripts and supporting host materials. It can generate a standard script from direct requirements or analyze a reference work's structure before producing a new game package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill asks agents to persist generated analysis into trusted reference markdown files.

Mitigation: Do not allow the skill to modify its own reference files as a cache; store generated analysis in a separate user-controlled workspace file when persistence is needed.

Risk: The security evidence reports that generated visualizations can expose private player material.

Mitigation: Treat visualization HTML as host-only unless private character fields and other non-player information are removed before sharing.

Risk: The security evidence warns that generated HTML may execute unsafe page content.

Mitigation: Review generated HTML before opening or sharing it, escape dynamic content, and vendor or pin D3 with integrity checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gongsunyanming/skills/murder-mystery-creator)
- [Project homepage](https://github.com/yiqi-ai/murder-mystery-creator)
- [Professional analysis framework](artifact/references/professional-analysis-framework.md)
- [Outline template](artifact/references/outline-template.md)
- [Character template](artifact/references/character-template.md)
- [Clue template](artifact/references/clue-template.md)
- [Host guide](artifact/references/host-guide.md)
- [Logic check](artifact/references/logic-check.md)
- [Image generation guide](artifact/references/image-generation-guide.md)
- [Visualization template](artifact/references/visualization-template.html)
- [Design tips](artifact/references/design-tips.md)
- [Writing techniques](artifact/references/writing-techniques.md)
- [Snowstorm Manor example script](artifact/snowstorm-manor.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown script package with optional image-generation prompts, JSON-like configuration, and generated HTML visualization.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include private character sections and host-only material that should be kept separate from player-facing content.]

## Skill Version(s):

1.8.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
