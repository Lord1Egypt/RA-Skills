## Description:

HTML PPT Studio helps agents author professional static HTML presentations using bundled themes, layouts, full-deck templates, animations, and rendering utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewislulu](https://clawhub.ai/user/lewislulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and presentation authors use this skill to turn outlines or source material into polished HTML slide decks, reports, pitch decks, technical talks, and social-card style slide sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional rendering and template execution can expose users to unsafe behavior when decks or templates come from untrusted sources.

Mitigation: Review decks before rendering, avoid untrusted decks, and run rendering inside an isolated container for sensitive workflows.

Risk: Some presentation templates may load remote JavaScript or other CDN-hosted assets.

Mitigation: Vendor or integrity-pin remote assets before using chart, code, or template features in sensitive environments.

Risk: Installing an unpinned skill source can make later installs differ from the reviewed release.

Mitigation: Pin the skill source to a reviewed commit or release before deployment.

## Reference(s):

- [Authoring Guide](references/authoring-guide.md)
- [Themes Catalog](references/themes.md)
- [Layouts Catalog](references/layouts.md)
- [Animations Catalog](references/animations.md)
- [Full-Deck Templates Catalog](references/full-decks.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces static presentation assets and optional PNG exports through bundled templates and scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
