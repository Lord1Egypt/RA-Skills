## Description: <br>
法眼 is a Chinese-law assistant skill for legal issue triage, contract review, litigation drafting, compliance checks, rights guidance, and legal document generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoho-x](https://clawhub.ai/user/hoho-x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to understand Chinese-law situations, compare action paths, review contracts, draft legal documents, and prepare practical next steps before seeking professional legal advice. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles high-stakes legal drafting and may produce incorrect, outdated, or misleading legal guidance. <br>
Mitigation: Use it as a drafting and education aid, then verify laws, filing rules, deadlines, and enforceability with official sources or a licensed lawyer before acting. <br>
Risk: Legal workflows can involve sensitive identity data and third-party personal information. <br>
Mitigation: Redact or replace full ID numbers, addresses, phone numbers, identity-document scans, and third-party personal data unless the information is truly necessary. <br>
Risk: The artifact describes legal research and timeliness validation workflows that still require current external verification. <br>
Mitigation: Treat generated citations, status checks, and litigation steps as prompts for independent verification against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoho-x/law-expert) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Usage guide](artifact/ç¨æ³æå.md) <br>
- [Contract review SOP](artifact/references/sops/sop-01-contract-review.md) <br>
- [Litigation drafting SOP](artifact/references/sops/sop-12-litigation-drafting.md) <br>
- [Legal Q&A SOP](artifact/references/sops/sop-08-legal-qna.md) <br>
- [Regulation search tool](artifact/scripts/regulation_search.py) <br>
- [Regulation validator tool](artifact/scripts/regulation_validator.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown-style legal analysis, checklists, comparisons, drafts, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include professional and plain-language versions, risk labels, action steps, legal document drafts, and verification prompts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
