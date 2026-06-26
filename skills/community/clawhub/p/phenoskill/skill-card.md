## Description: <br>
Extract clinical phenotypes and medication entities from user-provided text using PhenoSnap, producing a timestamped JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaichop](https://clawhub.ai/user/kaichop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, clinicians, and clinical informatics users can use this skill to extract phenotype and medication entities from their own clinical free text while keeping processing local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download and run unpinned third-party Python code and install dependencies before processing clinical text. <br>
Mitigation: Run it in a dedicated virtual environment or sandbox, and consider pre-installing a reviewed, pinned PhenoSnap version before use. <br>
Risk: User-provided clinical text and extracted results may contain sensitive health information stored in local input and output artifacts. <br>
Mitigation: Provide de-identified text, confirm before processing highly identifying PHI, and delete generated input and output artifacts when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaichop/phenoskill) <br>
- [PhenoSnap source repository](https://github.com/WGLab/PhenoSnap.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown response with local file paths and a timestamped JSON artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python, an HPO OBO file, and first-run network access for PhenoSnap and dependency bootstrap.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
