## Description: <br>
Screens companies, people, wallet identifiers, names, or domains for sanctions, KYB/KYC, AML, OFAC, PEP, and watchlist risk, returning compliance verdicts and risk scores through paid GoCreative API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinhughes2121](https://clawhub.ai/user/colinhughes2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill before onboarding, paying, contracting, or transacting with customers, vendors, counterparties, or wallet/name targets. It provides PASS/WARN/BLOCK compliance input, sanctions matches, KYB detail, and risk scores for downstream review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends names, domains, wallet identifiers, or company details to GoCreative and may trigger USDC x402 payment for each request. <br>
Mitigation: Confirm data-sharing, wallet, and payment policy before installation and use. <br>
Risk: PASS/WARN/BLOCK verdicts and risk scores may be insufficient as the sole basis for sensitive onboarding, payment, or contracting decisions. <br>
Mitigation: Treat results as compliance input and route sensitive or adverse decisions through human or policy review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/colinhughes2121/gocreative-compliance) <br>
- [GoCreative Agent Compliance & Data API](https://api.gocreativeai.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with HTTPS GET endpoints and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 requests can return PASS/WARN/BLOCK verdicts, sanctions matches, KYB reports, and entity risk scores.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
