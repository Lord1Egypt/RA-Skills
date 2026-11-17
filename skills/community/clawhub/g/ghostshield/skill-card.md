## Description:

GhostShield helps agents analyze repositories for personal or sensitive traces, apply multi-level code and document obfuscation, and evaluate the resulting style and privacy changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13770626440](https://clawhub.ai/user/13770626440)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare code or documentation for sharing by detecting PII, reducing identifiable style signals, optionally adding anti-distillation markers, and reviewing the effect on output quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secrets or sensitive strings may remain in generated output.

Mitigation: Do not treat GhostShield as a complete sanitizer; inspect processed files and run an independent secret scan before publishing or executing the output.

Risk: Processing repositories with symlinks may copy files outside the selected repository.

Mitigation: Run the tool only on disposable repository copies after reviewing symlinks and excluding untrusted paths.

Risk: Level 3 watermarking can persist hidden markers in generated code.

Mitigation: Avoid custom watermark IDs unless needed, disclose watermark use where appropriate, and inspect output before sharing.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/13770626440/skills/ghostshield)
- [Publisher Profile](https://clawhub.ai/user/13770626440)
- [Microsoft Presidio](https://github.com/microsoft/presidio)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets; when the tool is run, it can produce processed files and evaluation reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes three processing levels and optional watermark behavior; generated repository output should be inspected before use.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
