## Description:

Helps agents build fundraising and investor pitch decks as single PowerPoint files using OfficeCLI, with stage-specific guidance for seed, Series A, Series B, Series C, SAFE, convertible-note, and strategic raise scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceyliu](https://clawhub.ai/user/iceyliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to create a fundraising-focused investor deck rather than a generic business presentation. It guides stage diagnosis, narrative structure, slide recipes, OfficeCLI commands, and delivery checks for pitch decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include remote installer commands that execute downloaded scripts directly.

Mitigation: Prefer a pinned OfficeCLI release from the official release page and verify checksums or signatures before installation.

Risk: Investor decks can contain misleading or unsupported fundraising claims if generated content is not reviewed.

Mitigation: Review financial figures, source footnotes, chart axes, use-of-funds details, and stage-specific assertions before sharing a deck.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iceyliu/skills/officecli-pitch-deck)
- [OfficeCLI releases](https://github.com/iOfficeAI/OfficeCLI/releases)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with OfficeCLI command examples; the intended final artifact is a local .pptx file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pitch-deck delivery checks for stage fit, sourcing, financial figures, chart axes, use of funds, and visual review.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
