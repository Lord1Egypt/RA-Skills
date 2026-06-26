## Description: <br>
Helps users document e-commerce consumer disputes by collecting order evidence through browser automation and generating refund requests, 12315 complaint letters, civil complaint drafts, and related guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to organize e-commerce order disputes, preserve relevant order evidence, and draft consumer complaint or lawsuit materials for review before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may expose sensitive order, logistics, seller, and personal dispute information while viewing logged-in shopping pages and collecting evidence. <br>
Mitigation: Run the skill only for the specific dispute being documented, use a trusted browser automation MCP, and review or redact personal details before filing or sharing generated documents. <br>
Risk: Evidence files saved locally may be unintentionally shared if the target folder is synced or broadly accessible. <br>
Mitigation: Keep the evidence folder out of shared or cloud-synced locations when possible and restrict access to the collected files. <br>
Risk: Generated complaint and lawsuit drafts may be incomplete or unsuitable for complex or high-value disputes. <br>
Mitigation: Treat generated documents as editable drafts and consult a qualified lawyer for large, complex, or uncertain claims. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaoyaner0201/jd-lawsuit-skill) <br>
- [Platform guide](references/platform-guide.md) <br>
- [Evidence collection guide](references/evidence-collection.md) <br>
- [Legal templates](references/legal-templates.md) <br>
- [Legal basis quick reference](references/legal-basis.md) <br>
- [Complaint channel guide](references/complaint-channels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, guidance] <br>
**Output Format:** [Markdown documents, structured JSON evidence data, local evidence files, and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots, evidence indexes, raw-data JSON, and generated dispute documents under ~/Downloads/dispute-evidence/{orderId}/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
