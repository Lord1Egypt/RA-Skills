## Description:

Professional PPT presentation generation assistant that guides an agent through research, outline planning, slide-by-slide content planning, HTML slide design, and optional conversion to editable PPTX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[in12hacker](https://clawhub.ai/user/in12hacker)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to turn topics, outlines, or source materials into polished presentation decks with structured research, planning, HTML slide generation, and PPTX export support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local conversion tooling may run Python and Node scripts, install dependencies, and drive browser automation during deck packaging.

Mitigation: Use a dedicated workspace or container and review generated slide HTML before packaging.

Risk: Converting untrusted HTML or documents may expose local files or execute unsafe conversion behavior.

Mitigation: Avoid untrusted inputs and inspect source materials before running conversion scripts.

Risk: Optional WPS setup includes sudo package installation from an external archive.

Mitigation: Run WPS installation steps only after verifying the package source and hash.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/in12hacker/skills/ppt-pro)
- [PPTX pipeline](references/pptx-pipeline.md)
- [Execution rules](references/execution-rules.md)
- [Quality checks](references/quality-checks.md)
- [Resource registry](references/resource-registry.md)
- [Planning schema](references/planning.schema.json)
- [WPS Office validation notes](WPS_TESTING.md)
- [WPS Office 11.1.0.11719 archive](https://github.com/peeweep/gentoo-go-deps/releases/tag/wps-office_11.1.0.11719)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON planning artifacts, HTML slide files, shell commands, and optional PPTX output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and Node.js for the automated packaging and PPTX conversion paths.]

## Skill Version(s):

9.7.0 (source: frontmatter, server release metadata; pyproject.toml reports 9.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
