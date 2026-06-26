## Description: <br>
Provides Chinese-language wealth-management Q&A and bank product-matching suggestions using local FAQ and product materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krillingone](https://clawhub.ai/user/krillingone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask Chinese-language questions about bank wealth-management products, yield rules, holding periods, holiday income behavior, and product-fit suggestions. It provides informational matching guidance and does not perform account actions or make purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat product-matching suggestions as independent financial advice or as a purchase decision. <br>
Mitigation: Present responses as informational guidance, avoid deciding for the user, and direct users to verify suitability and risk disclosures before investing. <br>
Risk: Product yields, rankings, dates, liquidity tags, or suitability details may become stale. <br>
Mitigation: Check the latest official product page, sales page, and disclosure documents before relying on product information. <br>
Risk: The skill appends a bank mini-program purchase prompt and loads a disclosed external image. <br>
Mitigation: Disclose the prompt clearly and treat the image as an external resource rather than independent validation of a product. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/krillingone/personal-finance-skill) <br>
- [Mini-program purchase prompt image](https://static.hepei.club/contact.png) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Routing and response patterns](artifact/patterns.md) <br>
- [Product source list](artifact/products/理财产品全量列表.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language informational responses with product-fit rationale, risk reminders, source freshness notes for product data, and a disclosed mini-program image prompt.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
