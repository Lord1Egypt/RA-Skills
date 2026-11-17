## Description:

Mesagona namespace for Netsnek e.U. event and conference management platform, providing brand identity, feature information, and structured metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to answer questions about the Mesagona event-management brand, list its advertised capabilities, or return machine-readable brand metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled shell script may not run correctly because of a UTF-8 BOM and CRLF line endings.

Mitigation: Normalize the script to UTF-8 without BOM and Unix line endings before relying on executable behavior.

Risk: The skill requires local script execution.

Mitigation: Review the small bundled script before deployment and run it in the expected Linux environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kleberbaum/skills/mesagona)
- [Publisher Profile](https://clawhub.ai/user/kleberbaum)
- [Netsnek Website](https://netsnek.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Plain text, Markdown summaries, or JSON metadata from the bundled shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports default, --features, and --json modes; output is static brand and feature information.]

## Skill Version(s):

0.1.0 (source: artifact frontmatter, claw.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
