## Description:

Provides sem semantic-diff detection, install-on-first-use, and fallback patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when building or modifying skills that consume Git diff output. It provides patterns for semantic change detection with sem, installation prompts, and normalized Git-based fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Linux installation option downloads a binary from a GitHub release into the local bin directory.

Mitigation: Before installing, decide whether you trust that release source; if not, choose the Cargo installation option or use the standard git diff fallback.

## Reference(s):

- [sem project documentation](https://github.com/Ataraxy-Labs/sem)
- [Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-leyline-sem-integration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON entity schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides sem-based patterns and Git fallback examples for detection, semantic diffs, and impact analysis.]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
