## Description:

Analyzes multi-species FASTA inputs for protein families to produce consensus sequences, conserved key fragments, amino-acid composition summaries, and heuristic functional predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhen9nine](https://clawhub.ai/user/wuhen9nine)

### License/Terms of Use:

MIT-0

## Use Case:

Bioinformatics users and developers use this skill to run local protein-family analysis over FASTA sequences, compare conserved fragments across species, and generate structured reports for follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling can write analysis files outside the intended results directory.

Mitigation: Run the skill in a disposable or project-specific workspace and reject species names containing path separators, '..', or absolute paths.

Risk: The skill creates files locally while running bioinformatics scripts.

Mitigation: Avoid running the analysis as root and review generated files before moving them into shared or production locations.

Risk: Biological function and disulfide-bond claims are heuristic.

Mitigation: Treat predictions as candidates until supported by explicit domain hits, structural prediction, or experimental evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhen9nine/skills/protein-key-fragment-analysis)
- [Analysis method](references/method.md)
- [Functional domain reference](references/functional_domains.md)
- [Fibrinogen domain reference](references/fibrinogen_domains.md)
- [Pfam](http://pfam.xfam.org/)
- [InterPro](https://www.ebi.ac.uk/interpro/)
- [UniProt](https://www.uniprot.org/)
- [PROSITE](https://prosite.expasy.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown reports, JSON fragment files, consensus FASTA files, and console progress text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python scripts and requires ClustalOmega for multi-sequence alignment.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
