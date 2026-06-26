## Description: <br>
Verifies hadith authenticity against major collections before Islamic content is published, using public hadith datasets for Arabic and English lookup, source matching, and grading signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m7madash](https://clawhub.ai/user/m7madash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and content reviewers use this skill to check hadith text, claimed sources, and hadith numbers before publishing or citing Islamic material. It helps identify verified matches, likely matches, weak matches, missing references, and cases that require manual scholarly review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network access to jsDelivr is required to download public hadith datasets and may reveal which collections were queried. <br>
Mitigation: Use the skill only where outbound access to jsDelivr is acceptable, and review network policy before deployment. <br>
Risk: Automated text matching and grading signals may be incomplete or ambiguous for partial, translated, shortened, or paraphrased hadith text. <br>
Mitigation: Treat partial, weak, missing, or mismatched results as requiring manual review by qualified scholars before publication. <br>


## Reference(s): <br>
- [Hadith Verifier on ClawHub](https://clawhub.ai/m7madash/hadith-verifier) <br>
- [m7madash publisher profile](https://clawhub.ai/user/m7madash) <br>
- [fawazahmed0/hadith-api public dataset via jsDelivr](https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch public hadith collection data from jsDelivr; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
