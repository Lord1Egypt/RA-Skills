## Description:

Guides agents through Python-based paper reproduction, including source extraction, modular implementation, experiment logging, result verification, and bilingual documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celynnmoonlight](https://clawhub.ai/user/celynnmoonlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research engineers use this skill to convert paper sources into reproduction plans and Python implementations, then document, run, and compare experiments against paper-reported results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may read local paper sources and create or modify project files, including code, logs, results, figures, and bilingual README files.

Mitigation: Run it in the intended repository, review generated file changes before committing, and override bilingual README output when only one documentation language is desired.

Risk: Reproduction outputs may differ from paper-reported results because of ambiguous methods, preprocessing differences, random seeds, datasets, or hyperparameters.

Mitigation: Compare reproduced metrics against the paper, document discrepancies, and keep configuration snapshots and logs with each experiment run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/celynnmoonlight/skills/paper-repro-python)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, Python code, shell commands, configuration files, logs, and experiment outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create source-derived extraction notes, Python modules, experiment logs, result files, figures, and README files in English and Chinese.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
