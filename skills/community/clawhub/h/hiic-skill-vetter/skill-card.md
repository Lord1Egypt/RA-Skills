## Description:

Practical skill vetting workflow for AI agents. Prioritizes clear yes/no risk judgments, concise conclusions, and business-aware risk tolerance before installing a skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waytobetter619](https://clawhub.ai/user/waytobetter619)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to quickly vet agent skills before installation, producing concise risk judgments and installation recommendations. It is intended for quick install checks, portfolio-wide skill reviews, and second-opinion risk screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scanner can overread local files when pointed at an untrusted skill directory.

Mitigation: Run scans in a sandbox or on a copy of the target directory with symlinks removed.

Risk: Raw scanner output may expose matched lines that contain secrets or sensitive local paths.

Mitigation: Review and redact raw JSON or text findings before sharing or publishing them.

Risk: The skill is a manual triage aid and should not be treated as a final security authority.

Mitigation: Pair its conclusion with manual inspection of SKILL.md prose, helper scripts, and any files excluded by the scanner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waytobetter619/skills/hiic-skill-vetter)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JSON]

**Output Format:** [Concise Markdown or text risk report, with optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner output may include matched source lines; treat raw findings as sensitive.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
