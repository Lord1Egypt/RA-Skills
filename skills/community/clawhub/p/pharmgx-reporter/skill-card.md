## Description: <br>
Pharmacogenomic report from DTC genetic data (23andMe/AncestryDNA). <br>

This skill is for research and development only. <br>

## Publisher: <br>
[manuelcorpas](https://clawhub.ai/user/manuelcorpas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, educators, and bioinformatics developers use this skill to parse consumer genetic data, profile pharmacogenomic variants, and generate Markdown reports with gene profiles and drug-response recommendations for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Genetic input files and generated reports may contain sensitive health information. <br>
Mitigation: Run the skill only on genetic files intentionally selected by the user and store generated reports in a private location. <br>
Risk: Pharmacogenomic report content could be mistaken for clinical or medication-changing advice. <br>
Mitigation: Use reports for research and education only; medication changes should be reviewed by a qualified clinician and confirmed with clinical-grade testing. <br>
Risk: Local execution depends on trusting the installed artifact and selected inputs. <br>
Mitigation: Install only from trusted sources and review the skill before running it on sensitive genetic data. <br>


## Reference(s): <br>
- [PharmGx Reporter on ClawHub](https://clawhub.ai/manuelcorpas/pharmgx-reporter) <br>
- [ClawBio homepage](https://github.com/ClawBio/ClawBio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report and concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected genetic data file and writes a user-selected Markdown report.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
