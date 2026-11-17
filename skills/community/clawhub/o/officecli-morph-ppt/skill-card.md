## Description:

Creates PowerPoint .pptx decks with smooth cross-slide Morph transitions by guiding agents through shape-name pairing, scene actors, ghosting, OfficeCLI commands, and visual style selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceyliu](https://clawhub.ai/user/iceyliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation-building agents use this skill when a user specifically requests a PowerPoint deck with continuous cross-slide motion or Morph transitions. It is not intended for generic slide decks that do not need cross-slide animation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include remote pipe-to-shell installers for OfficeCLI.

Mitigation: Review and install OfficeCLI through a verified release path yourself; do not let an agent run pipe-to-shell setup commands unattended.

Risk: The Bash verifier can turn crafted PPTX content into code execution when checking untrusted decks.

Mitigation: Prefer the Python helper for verification and avoid using morph-helpers.sh on untrusted PPTX files.

Risk: Cleanup or demo build scripts may modify decks.

Mitigation: Back up decks before running cleanup or demo build scripts and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iceyliu/skills/officecli-morph-ppt)
- [OfficeCLI releases](https://github.com/iOfficeAI/OfficeCLI/releases)
- [Decision rules](artifact/reference/decision-rules.md)
- [PPTX design guidance](artifact/reference/pptx-design.md)
- [Style library index](artifact/reference/styles/INDEX.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with OfficeCLI shell commands and helper script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single .pptx deck when executed by an agent with OfficeCLI available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
