## Description: <br>
Provides AI-assisted legal and compliance automation skills for Chinese enterprise legal teams, covering contract review, legal Q&A, labor compliance, intellectual property, data protection, and corporate compliance workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese enterprise legal, HR, privacy, and compliance teams use this skill bundle to draft, review, score, and summarize contracts, policies, legal questions, labor matters, IP issues, data protection obligations, and corporate compliance materials. Outputs are drafts and checklists intended for qualified human review before operational use. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that one legal Q&A path can send sensitive questions to DeepSeek when an API key is configured. <br>
Mitigation: Use only non-confidential test data unless the DeepSeek data flow is approved, and avoid setting DEEPSEEK_API_KEY when local-only processing is required. <br>
Risk: The security review reports that some legal-risk outputs overstate limited checks, including legal opinions, compliance ratings, and risk assessments. <br>
Mitigation: Treat generated legal outputs as drafts and require review by qualified legal, HR, privacy, or compliance professionals before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/legal-compliance-bundle) <br>
- [Publisher profile](https://clawhub.ai/user/daimingvip-a11y) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, generated document templates, checklists, JSON-like structured results, and command-line guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Legal opinions, compliance ratings, risk scores, and assessment reports should be treated as drafts requiring qualified human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
