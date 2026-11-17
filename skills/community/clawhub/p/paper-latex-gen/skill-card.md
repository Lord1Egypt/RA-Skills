## Description:

Paper Latex Gen is a legacy compatibility skill for generating structured academic LaTeX paper files and related resources through the newer unified paper command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and writers use this skill to request structured academic paper LaTeX assets for conference-style submissions such as NeurIPS, ICML, and ICLR. It is primarily useful for backward-compatible workflows that still call the older latex entry point.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on this legacy compatibility entry point instead of the current unified paper command.

Mitigation: Prefer the documented paper latex command when available and treat this skill as a backward-compatible path for LaTeX paper generation.

Risk: Generated academic paper structure, citations, or template choices may be incomplete or unsuitable for a target venue.

Mitigation: Review generated LaTeX, BibTeX, and conference template files before submission or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/paper-latex-gen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command examples and generated LaTeX/BibTeX file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or describes paper.tex, references.bib, figures/, and conference template files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
