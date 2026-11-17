## Description:

Use when a check-engine light is on, an OBD2 scan returns P0xxx/P2xxx/B/C/U codes, or you need to know if the car is safe to drive, what the code means in plain language, likely causes with fix cost bands, and DIY difficulty. Decodes 70+ generic codes, detects multi-code patterns (lean-both-banks, misfire+catalyst chains), and gives a STOP-DRIVING / SOON / MONITOR verdict per code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Drivers and used-car buyers can interpret generic OBD2 scan codes, understand likely causes and cost ranges, and use the decoder's general guidance when deciding what to discuss with a mechanic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A driver may treat a code-based verdict as confirmation that the vehicle is safe to drive.

Mitigation: Treat driving recommendations as general guidance, not confirmation of vehicle safety; have serious symptoms assessed separately.

Risk: Unknown or manufacturer-specific codes are excluded from the overall verdict.

Mitigation: Have unknown codes assessed separately using make-specific diagnostics.

## Reference(s):

- [OBD2 Code Decoder Reference](references/code-knowledge.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text with code meanings, likely causes, cost bands, DIY difficulty, and a verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes multi-code patterns and manufacturer-specific code fallbacks when applicable.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
