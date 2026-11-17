## Description:

Optimize IHC/IF protocols for specific tissues and antigens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and wet-lab developers use this skill to generate starting-point IHC/IF staining protocol recommendations for tissues, antigen locations, and detection difficulty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated wet-lab recommendations may be incorrect, incomplete, or unsuitable for a specific experimental or clinical setting.

Mitigation: Have a qualified reviewer validate recommendations against local protocols, controls, reagent datasheets, and safety requirements before use.

Risk: The artifact documentation lists some CLI options and file-output behavior that the actual script does not implement.

Mitigation: Use the script-supported arguments and treat documentation-only options as unavailable until the artifact is corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/ihc-if-optimizer)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Plain text protocol recommendations printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies or network calls are indicated by the release evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
