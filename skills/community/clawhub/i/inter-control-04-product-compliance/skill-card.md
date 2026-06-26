## Description: <br>
Performs pre-release and follow-up compliance checks for Taobao Flash Sale product listings by identifying prohibited goods, pricing-fraud risks, misleading advertising, and remediation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operations, compliance, and product-governance teams use this skill to review Taobao Flash Sale listings before launch, after complaints, during routine patrols, or during price-monitoring investigations. It returns compliance ratings, issue lists, supporting rationale, and remediation guidance for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compliance ratings or enforcement suggestions may be mistaken for official Alibaba decisions or legal advice. <br>
Mitigation: Treat outputs as advisory and require qualified compliance, legal, or platform-policy review before delisting, refund, penalty, or merchant-action decisions. <br>
Risk: The skill references supporting glossary, insufficiency-handling, rule-update, and conflict-resolution documents that are not included in the artifact. <br>
Mitigation: Confirm current Taobao rules and internal procedures before relying on the skill for final determinations. <br>
Risk: Pricing-fraud analysis depends on accurate historical pricing, transaction, inventory, and promotion data supplied by the user or platform. <br>
Mitigation: Validate all material claims against authoritative price history and transaction records before acting on the assessment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/inter-control-04-product-compliance) <br>
- [Publisher profile](https://clawhub.ai/user/nic-yuan) <br>
- [Taobao Rules Center](https://rule.taobao.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown compliance report with ratings, risk tables, rationale, and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output based on user-supplied product, pricing, credential, and rule-update information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); artifact frontmatter reports 1.7.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
