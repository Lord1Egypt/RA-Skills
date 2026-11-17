## Description:

Papyrus transforms arXiv papers into bilingual, annotation-rich PDFs with preserved original text, Chinese translation, expert commentary, figures, formulas, and academic typesetting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zanechen76](https://clawhub.ai/user/zanechen76)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent users use Papyrus to turn arXiv papers into bilingual deep-read study documents with structured translation, commentary, figures, rendered formulas, and PDF export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts process untrusted paper content and user-provided paths, which may execute code.

Mitigation: Run Papyrus only in a constrained workspace, review downloaded arXiv sources as untrusted, and avoid attacker-controlled paths or filenames.

Risk: Formula rendering can send formula content to a third-party online renderer.

Mitigation: Prefer local-only LaTeX rendering and avoid using the skill on private or sensitive papers until the scripts are fixed.

Risk: Agent adapters could run in environments with excessive privileges or credentials.

Mitigation: Do not enable the adapters in privileged or credential-rich environments.

## Reference(s):

- [Papyrus on ClawHub](https://clawhub.ai/zanechen76/skills/papyrus)
- [arXiv e-print source](https://arxiv.org/e-print/)
- [arXiv HTML papers](https://arxiv.org/html/)
- [CodeCogs LaTeX rendering](https://latex.codecogs.com/)
- [OpenClaw Kami design language](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML and Python adapter definitions, HTML skeletons, PNG assets, and PDF output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user- or agent-supplied paper content, formula extraction, translation, commentary, and quality review before final PDF delivery.]

## Skill Version(s):

0.2.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
