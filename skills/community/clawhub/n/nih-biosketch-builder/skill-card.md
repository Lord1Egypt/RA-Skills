## Description: <br>
Generate NIH Biosketch documents compliant with the 2022 OMB-approved format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, grant writers, and agent operators use this skill to prepare NIH biosketch DOCX files from structured JSON input. It can also generate template JSON and optionally import publication details from PubMed using PMIDs or author search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional PubMed import and search can send publication IDs, names, and optional affiliation terms to NCBI/PubMed. <br>
Mitigation: Use networked PubMed features only with data approved for external lookup, or run the skill without PubMed import/search. <br>
Risk: The script writes DOCX or JSON files to the output path supplied by the user. <br>
Mitigation: Review output paths before execution and run the skill in a workspace or sandbox with appropriate file permissions. <br>
Risk: Dependencies are required for document generation and network lookup behavior. <br>
Mitigation: Pin and audit dependencies in managed environments before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/nih-biosketch-builder) <br>
- [Audit reference](references/audit-reference.md) <br>
- [NIH Biosketch Format Instructions](https://grants.nih.gov/grants/forms/biosketch.htm) <br>
- [SciENcv](https://www.ncbi.nlm.nih.gov/sciencv/) <br>
- [NCBI Entrez E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [DOCX and JSON files, with Markdown guidance and shell commands for agent execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to user-provided output paths; optional PubMed import and search use NCBI/PubMed network APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
