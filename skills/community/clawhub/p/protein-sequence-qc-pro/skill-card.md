## Description:

Professional protein sequence quality control and visualization workflow with a complete QC pipeline, conservation and coevolution analysis, and publication-ready figures for protein family analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billwanttobetop](https://clawhub.ai/user/billwanttobetop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformatics practitioners, and researchers use this skill to run protein sequence QC, alignment filtering, conservation and coevolution analysis, and generation of paper-ready QC figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that scripts ignore documented user-selected paths and operate on hard-coded root-directory locations.

Mitigation: Review and fix path handling before deployment, and run only in a disposable, unprivileged environment with no sensitive files accessible.

Risk: The security evidence reports unsafe shell command execution.

Mitigation: Inspect commands before execution, avoid untrusted path or sequence inputs, and replace shell-based subprocess calls with explicit argument lists before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billwanttobetop/skills/protein-sequence-qc-pro)
- [Skill documentation](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate FASTA files, JSON/CSV analysis outputs, logs, and PNG/PDF figures when the referenced scripts are executed.]

## Skill Version(s):

5.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
