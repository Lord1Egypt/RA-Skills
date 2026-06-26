## Description: <br>
Provides Chinese legal consulting automation for contract review, legal Q&A, compliance checks, labor disputes, intellectual property protection, and debt collection using bundled Chinese legal knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Small business owners, entrepreneurs, individual users, and legal assistants use this skill to receive informational China-law analysis, including contract review, legal Q&A, compliance checks, labor dispute guidance, intellectual property guidance, and debt collection guidance. <br>

### Deployment Geography for Use: <br>
Global, for China-law informational use <br>

## Known Risks and Mitigations: <br>
Risk: Users may over-rely on generated legal analysis as licensed legal advice. <br>
Mitigation: Treat outputs as informational only and consult a qualified lawyer for material legal decisions. <br>
Risk: Legal questions may include personal, privileged, confidential, or business-sensitive details, and configured DeepSeek use can send prompts to an external API. <br>
Mitigation: Redact unnecessary sensitive details and submit privileged or confidential material only when DeepSeek use is acceptable. <br>
Risk: Broad file or write access could expose unrelated documents or reports during use. <br>
Mitigation: Grant access only to documents and reports involved in the current legal-consulting task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/legal-consulting-bundle) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Civil Code knowledge base](artifact/knowledge_base/civil_code.md) <br>
- [Contract law knowledge base](artifact/knowledge_base/contract_law.md) <br>
- [Labor law knowledge base](artifact/knowledge_base/labor_law.md) <br>
- [Company law knowledge base](artifact/knowledge_base/company_law.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style legal analysis or JSON API responses containing generated guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can operate with a DeepSeek API key or use built-in template responses when no API key is configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
