## Description: <br>
Audits food package labels from images or PDFs against GB7718, GB28050, and claim-language guidance, then produces a structured compliance report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudyxuq](https://clawhub.ai/user/cloudyxuq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and compliance reviewers use this skill to review food packaging label artwork for required label elements, nutrition label correctness, claim-language compliance, allergen labeling, formatting issues, and remediation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food label compliance conclusions may be incomplete or legally insufficient if OCR, vision extraction, or regulatory interpretation is wrong. <br>
Mitigation: Use the output as an audit aid and have qualified legal or regulatory reviewers confirm conclusions before relying on them for packaging release. <br>
Risk: Uploaded packaging artwork may contain confidential product or design information. <br>
Mitigation: Confirm how the runtime agent processes images and PDFs, including whether any third-party OCR or vision services are used, before submitting confidential materials. <br>


## Reference(s): <br>
- [GB7718 Prepackaged Food Label Standard](references/gb7718-standard.md) <br>
- [GB28050 Nutrition Label Standard](references/gb28050-standard.md) <br>
- [Claim Language Compliance Guide](references/claims-guideline.md) <br>
- [Label Audit Checklist Template](assets/audit-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown compliance report with checklist findings, risk levels, and remediation suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on the agent's native OCR or vision handling for uploaded image and PDF label artwork.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
