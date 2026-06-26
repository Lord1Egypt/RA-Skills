## Description: <br>
Analyze consumer DNA data from WeGene, 23andMe, AncestryDNA, VCF, BAM, or CRAM files and generate evidence-based reports covering health risks, pharmacogenomics, ancestry, nutrition, exercise traits, and supplement guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanzhanglee](https://clawhub.ai/user/yanzhanglee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze their consumer genetic testing or sequencing files, review genetic risk and pharmacogenomics findings, and produce reports, supplement plans, screening schedules, and physician-facing summaries. It is intended for informational genomics interpretation and should not replace clinical genetic counseling or medical care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive DNA files and health details. <br>
Mitigation: Keep raw genetic files and generated reports local, avoid shared or cloud-synced folders, and disclose only the minimum health context needed for the analysis. <br>
Risk: The skill can produce medical-style recommendations about medications, supplements, screening, and risk follow-up. <br>
Mitigation: Treat outputs as informational risk estimates, require a clear medical disclaimer, and consult a qualified clinician, pharmacist, or genetic counselor before changing medication, supplements, or screening plans. <br>
Risk: Optional CRAM reference fetching and third-party tool setup can introduce network access or unverified binaries. <br>
Mitigation: Prefer local reference genomes, review third-party tools before building or running them, and avoid network reference fetching unless the user explicitly accepts it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yanzhanglee/personal-genomics-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/yanzhanglee) <br>
- [Supported Genetic Data Formats](artifact/references/supported_formats.md) <br>
- [Personal Genomics SNP Database Reference](artifact/references/snp_database.md) <br>
- [Personalized Supplement Recommendation Guide](artifact/references/supplement_guide.md) <br>
- [Tool Setup Guide](artifact/references/tool_setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional generated Python analysis scripts, HTML reports, Excel schedules, and summary documents.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles local genomic files and may guide optional samtools, bcftools, and Python package setup for variant parsing and verification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
