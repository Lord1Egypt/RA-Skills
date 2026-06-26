## Description: <br>
Generates a personalized nutrition report from consumer genetic data by analyzing nutritionally relevant SNPs and producing dietary and supplementation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manuelcorpas](https://clawhub.ai/user/manuelcorpas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run local nutrigenomics analysis on consumer genetic data and generate a readable nutrition report with risk scores, recommendations, figures, and reproducibility files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes genetic data and writes derived health and genotype reports to disk. <br>
Mitigation: Use a private, non-synced output folder and review generated files before sharing them. <br>
Risk: Generated nutrition recommendations could be mistaken for medical advice. <br>
Mitigation: Treat the report as educational guidance and consult qualified health professionals before making medical, supplement, or major diet decisions. <br>
Risk: The reproducibility bundle writes commands.sh for rerunning analysis. <br>
Mitigation: Review or fix shell quoting for all paths and arguments before running commands.sh. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/manuelcorpas/nutrigx-advisor) <br>
- [NutriGx Advisor skill documentation](artifact/SKILL.md) <br>
- [Curated SNP panel](artifact/data/snp_panel.json) <br>
- [Example NutriGx report](artifact/examples/output/nutrigx_report.md) <br>
- [David de Lorenzo GitHub profile](https://github.com/drdaviddelorenzo) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with generated image files and reproducibility artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports, figures, checksums, environment.yml, commands.sh, and provenance.json to a local output directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata; artifact files reference 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
