## Description:

Redefines LaTeX verbatim blocks with varwidth and center environments so code blocks and ASCII diagrams can be horizontally centered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:

MIT-0

## Use Case:

Document editors, technical writers, and developers use this skill to fix LaTeX documents where verbatim code blocks or ASCII diagrams stay left-aligned despite center formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package-manager commands such as tlmgr install can change the local TeX installation.

Mitigation: Review commands before running them and install only the required package through trusted TeX Live tooling.

Risk: Example absolute paths may expose user-specific local file paths if redistributed.

Mitigation: Replace local paths with generic placeholders before sharing or publishing derived documentation.

Risk: Global verbatim redefinition may conflict with fancyvrb or existing verbatim customizations.

Mitigation: Test in a copy of the document first, or create a separate centered verbatim environment when compatibility matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bg1avd/skills/latex-verbatim-center)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [Quick reference](artifact/QUICKREF.md)
- [Creation report](artifact/report.md)
- [CTAN varwidth package documentation](https://ctan.org/pkg/varwidth)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with LaTeX configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes package checks, preamble configuration, compile guidance, validation checklist, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
