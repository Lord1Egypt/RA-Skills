## Description: <br>
电商导购助手 is a conversational shopping assistant that uses haohuo-cps product data to provide end buyers with product recommendations, price checks, deal reminders, and shopping advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachariah-77](https://clawhub.ai/user/zachariah-77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External CPS promoters can embed this skill in apps, websites, customer-service windows, or shopping groups to answer buyer shopping questions, retrieve product data through haohuo-cps, and present buyer-facing recommendations without exposing commission fields. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on sensitive credential setup through haohuo-cps; missing or incorrect LINKBOT_API_KEY configuration may prevent promoter attribution for purchase links. <br>
Mitigation: Configure LINKBOT_API_KEY in haohuo-cps before deployment and test generated purchase links with a non-production buyer flow. <br>
Risk: Buyer-facing replies could accidentally expose promoter-only information such as commission rate, CPS terminology, or product IDs. <br>
Mitigation: Review responses for the required field filtering before publishing them to buyer channels. <br>
Risk: Product prices, coupons, stock, and regional subsidy details can change after haohuo-cps returns data. <br>
Mitigation: Use fresh haohuo-cps results for each buyer request and include clear reminders to confirm time-limited or region-limited offers before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zachariah-77/haohuo-recommend) <br>
- [Haohuo homepage](https://www.haohuo.com) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Buyer-facing conversational Markdown with short product cards, prices, offer notes, rationale, and purchase links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters promoter-only fields such as commission rate, CPS terminology, and product ID from buyer replies.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
