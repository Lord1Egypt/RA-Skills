## Description: <br>
Published as Neoantigen Predictor, this release installs an NIH biosketch generator that creates 2022 OMB-approved NIH biosketch documents from structured input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use the installed artifact to generate NIH biosketch DOCX files from JSON data and optionally retrieve publication metadata from PubMed. Users should confirm that they intended to install an NIH biosketch generator because the published name and slug describe a different tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is published as Neoantigen Predictor but the artifact installs an NIH biosketch generator, which can cause users to install or run the wrong tool. <br>
Mitigation: Confirm the intended tool before installation and use this release only when the desired workflow is NIH biosketch generation. <br>
Risk: PubMed import and author search options make network requests that send PMIDs or author query terms to NCBI. <br>
Mitigation: Run the skill in an isolated Python environment and avoid using network-backed options with sensitive or unapproved query data. <br>
Risk: The dependency declaration lists docx while the script expects python-docx behavior. <br>
Mitigation: Review and correct the dependency declaration to the intended python-docx package before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/neoantigen-predictor) <br>
- [NIH Biosketch Format Instructions](https://grants.nih.gov/grants/forms/biosketch.htm) <br>
- [SciENcv](https://www.ncbi.nlm.nih.gov/sciencv/) <br>
- [NCBI Entrez Utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [Audit Reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [DOCX files, JSON files, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local output files and may call PubMed or NCBI endpoints when publication import or search options are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
