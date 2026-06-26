## Description: <br>
Generate a personalised nutrition report from genetic data in 23andMe, AncestryDNA, or VCF formats, analysing nutrition-related genes while processing data locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drdaviddelorenzo](https://clawhub.ai/user/drdaviddelorenzo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and health-oriented developers use this skill to turn consumer genetic files into educational nutrigenomics reports with nutrient risk scores, genotype summaries, visualisations, and dietary guidance. It is not medical advice and should be reviewed with qualified healthcare providers for clinical decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports contain sensitive derived genotype results and nutrition-related interpretations. <br>
Mitigation: Run the skill in a private workspace, avoid shared or synced folders, review outputs before sharing, and delete the generated nutrigenomics_output directory after saving needed results. <br>
Risk: Nutrigenomics risk scores and recommendations are educational indicators rather than clinical diagnoses. <br>
Mitigation: Use the report as informational guidance and consult qualified healthcare providers before making medical or supplementation decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drdaviddelorenzo/nutrigenomics) <br>
- [Publisher profile](https://clawhub.ai/user/drdaviddelorenzo) <br>
- [PubMed MEDLINE](https://pubmed.ncbi.nlm.nih.gov/) <br>
- [GWAS Catalog](https://www.ebi.ac.uk/gwas/) <br>
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report plus local image files and reproducibility text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local genetic data and writes generated reports, figures, checksums, and provenance files to a timestamped output directory that persists until manually deleted.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata, CHANGELOG, SKILL.md, openclaw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
