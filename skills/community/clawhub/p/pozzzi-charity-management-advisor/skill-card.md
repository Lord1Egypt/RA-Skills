## Description: <br>
噗滋（pozzzi）慈善 management-advisor Skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and charity operations staff use this skill to ask China-focused charity management, compliance, governance, tax, and HR questions and receive knowledge-base-grounded reference answers with required disclaimers. Human review is required before using outputs for organizational decisions. <br>

### Deployment Geography for Use: <br>
Global (China-focused regulatory content) <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat reference answers as legal, tax, fundraising, HR, or final management advice. <br>
Mitigation: Use the skill as a reference aid only, preserve the required disclaimer, and require human or qualified professional review before action. <br>
Risk: User prompts may contain beneficiary names, phone numbers, ID numbers, or sensitive case details. <br>
Mitigation: Avoid entering personal or sensitive case details; redact inputs before use and rely on the skill's PII filtering where available. <br>
Risk: Audit log storage location and retention depend on the configured storage adapter. <br>
Mitigation: Confirm the storage adapter, audit log location, and retention policy before production deployment. <br>


## Reference(s): <br>
- [Ministry of Civil Affairs source referenced by knowledge base](https://www.mca.gov.cn) <br>
- [Charity law knowledge base](templates/knowledge-charity-law.md) <br>
- [Compliance FAQ knowledge base](templates/knowledge-compliance-faq.md) <br>
- [Governance knowledge base](templates/knowledge-governance.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown Q&A response with structured sections and disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include metadata such as model, provider, degraded status, duration, detected category, knowledge sources, and knowledge version.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
