## Description: <br>
Use Mercado Libre to search, compare, buy, sell, and automate decisions with pricing, safety, and dispute workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Mercado Libre buyers, sellers, and operators use this skill to discover products, compare listings, validate deals, plan purchases, optimize listings, handle disputes, and design safer marketplace automations. It supports decision-making and live operations while requiring explicit confirmation before high-impact account, listing, order, pricing, or automation changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with account-affecting marketplace workflows such as listings, orders, pricing, purchases, and automation. <br>
Mitigation: Require explicit user approval before any listing, order, pricing, purchase, account, or live automation change. <br>
Risk: Local memory under ~/mercado-libre/ may contain budgets, watchlists, seller notes, dispute logs, and operational history. <br>
Mitigation: Store only information that improves future decisions, avoid credentials and payment-sensitive data, and keep user-managed secrets outside shared notes. <br>
Risk: Live API or panel automation can create operational drift if the scope, rollback path, or reconciliation step is unclear. <br>
Mitigation: Define scope and guardrails, run a narrow first live execution only after confirmation, reconcile results against Mercado Libre, and keep a manual fallback path. <br>


## Reference(s): <br>
- [Mercado Libre ClawHub page](https://clawhub.ai/ivangdavila/mercado-libre) <br>
- [Mercado Libre skill homepage](https://clawic.com/skills/mercado-libre) <br>
- [Mercado Libre website](https://www.mercadolibre.com) <br>
- [Mercado Libre API](https://api.mercadolibre.com) <br>
- [Mercado Libre Developers](https://developers.mercadolibre.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, API Calls] <br>
**Output Format:** [Markdown with decision templates, comparison tables, checklists, API workflow plans, and local memory structure guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local notes under ~/mercado-libre/ for continuity; live buying, selling, pricing, listing, order, or automation actions require user-approved Mercado Libre access and explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
