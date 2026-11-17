## Description:

Generates a personalized nutrition report from consumer genetic data by analyzing nutritionally relevant SNPs and producing educational dietary and supplementation guidance.

This skill is for research and development only.

## Publisher:

[manuelcorpas](https://clawhub.ai/user/manuelcorpas)

### License/Terms of Use:


## Use Case:

Developers, bioinformatics practitioners, and health-adjacent users use this skill to analyze consumer genetic files locally and generate educational nutrition risk summaries, recommendations, charts, and reproducibility files. It should be used only with the user's own DNA data or data they have clear consent to analyze.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive genetic information and outputs report artifacts that may reveal genotype-derived findings.

Mitigation: Use only DNA data the user owns or has consent to analyze, keep the output directory private, and treat reports, charts, and reproducibility files as sensitive.

Risk: Security evidence says the skill stores exact genotype data despite claiming it will not.

Mitigation: Review generated outputs before sharing, update privacy claims before release, and avoid retaining genotype tables longer than necessary.

Risk: Security evidence flags unsafe shell quoting in the generated commands.sh reproducibility script.

Mitigation: Do not run commands.sh with untrusted or unusual file paths until quoting is fixed; inspect and safely quote command arguments first.

Risk: Nutrition and supplement recommendations may be mistaken for clinical advice.

Mitigation: Present recommendations as educational and advise users to discuss significant diet, supplement, or health changes with a qualified clinician.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manuelcorpas/skills/nutrigx-advisor)
- [Skill documentation](artifact/SKILL.md)
- [Curated SNP panel](artifact/data/snp_panel.json)
- [Example generated report](artifact/examples/output/nutrigx_report.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown report with optional PNG charts and reproducibility files including commands.sh, environment.yml, checksums.txt, and provenance.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on supported genetic data files and may write sensitive genotype-derived outputs to the selected output directory.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
