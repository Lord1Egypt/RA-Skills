## Description: <br>
Normalizes testing engineers' written defect reasons against product codebooks by correcting typos, abbreviations, ambiguous or mixed Chinese-English descriptions, then segmenting reasons, matching codes, calibrating confidence, and validating station scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing test, quality, and data teams use this skill to standardize free-text failure reasons into product-codebook failure codes, labels, confidence scores, and rationales. It helps segment raw reason text, respect station-specific code constraints, and surface UNKNOWN when evidence is weak. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manufacturing logs and codebooks may contain sensitive or unrelated operational records. <br>
Mitigation: Limit file access to the intended CSVs and codebooks, and avoid including unrelated sensitive records. <br>
Risk: Incorrect normalization can assign invalid station-specific codes or overstate weak matches. <br>
Mitigation: Enforce station scope, use UNKNOWN when best-match evidence is weak, and review sample outputs before operational use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or structured text with normalized failure-code fields, confidence scores, and rationales] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One prediction per segment; confidence rounded to 4 decimals; UNKNOWN used when best evidence is weak.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
