## Description: <br>
Generate and check privacy policy documents. Use when creating a privacy policy from scratch, checking existing policy completeness, or adding GDPR and CCPA compliance clauses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and policy authors can use this skill to draft privacy policy text, generate GDPR or CCPA supplemental clauses, update data-collection notices, and check existing policies for common completeness signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated privacy policies may be incomplete, jurisdiction-specific, or unsuitable as legal advice. <br>
Mitigation: Treat generated policies as drafts and review them with qualified legal or privacy reviewers before publication. <br>
Risk: The checker reads the local file path provided by the user. <br>
Mitigation: Run the checker only on policy files you intend the skill to read. <br>
Risk: The security guidance notes that the checker appears buggy until fixed. <br>
Mitigation: Use checker results as a rough completeness aid and manually verify required privacy-policy sections. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Plain text and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated policy text should be treated as a draft and reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
