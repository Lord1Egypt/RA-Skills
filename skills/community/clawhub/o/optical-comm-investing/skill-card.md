## Description:

Chinese-language optical-communications investing framework that helps agents analyze related stocks, technology routes, supply-chain position, valuation posture, and optional knowledge updates from cited Xueqiu sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanweisean](https://clawhub.ai/user/seanweisean)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment-research agents use this skill to structure Chinese-language analysis of optical module, optical chip, PCB, CPO, NPO, OCS, and related A-share investment topics. It supports reference-grounded stock review, technology-route comparison, supply-chain mapping, valuation framing, and cautious manual knowledge updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional update workflow can use a logged-in Xueqiu browser session.

Mitigation: Run updates only after explicit user request, review any browser use of the login session, and avoid storing credentials.

Risk: The skill contains ambiguous scheduled-check wording for future knowledge updates.

Mitigation: Do not run the update workflow on a schedule; trigger it manually and inspect appended reference changes before relying on new analyses.

Risk: Investment analysis can become stale as market, company, and industry conditions change.

Mitigation: Treat outputs as reference-grounded analysis, verify against current market disclosures and source posts, and preserve uncertainty in conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanweisean/skills/optical-comm-investing)
- [闷得而蜜 Xueqiu profile](https://xueqiu.com/u/5672579962)
- [查尔斯大风车 Xueqiu profile](https://xueqiu.com/u/8755156034)
- [查尔斯大风车 2026-04-21 article](https://xueqiu.com/8755156034/384873103)
- [core-framework.md](references/core-framework.md)
- [tech-landscape.md](references/tech-landscape.md)
- [supply-chain.md](references/supply-chain.md)
- [methodology.md](references/methodology.md)
- [update-log.md](references/update-log.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown or plain-text analysis with referenced reasoning steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock-analysis checklists, technology-route comparisons, valuation framing, supply-chain summaries, and manual update guidance.]

## Skill Version(s):

2.0.0 (source: server release metadata, created 2026-04-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
