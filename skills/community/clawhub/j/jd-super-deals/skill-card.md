## Description: <br>
Provides a JD Super Deals shopping search tool for finding JD self-operated subsidized products with keyword, price, rating, sorting, and pagination filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to search JD Super Deals products, compare prices and subsidy amounts, filter by category or budget, and receive structured product details with purchase links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping searches, price filters, and pagination requests are sent through the publisher's Tencent cloud proxy. <br>
Mitigation: Avoid entering sensitive personal data in search terms and install only when this proxy data flow is acceptable. <br>
Risk: Returned purchase links may be affiliate or tracking links, and product availability or prices can change after retrieval. <br>
Mitigation: Review the destination link and confirm final merchant, price, subsidy, and terms on JD before buying. <br>
Risk: The security summary warns not to assume every result is exclusively JD self-operated despite the skill description. <br>
Mitigation: Treat product metadata as advisory and verify seller status on the product page before purchase. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cn-shopping/jd-super-deals) <br>
- [Publisher profile](https://clawhub.ai/user/cn-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON response containing a summary string and structured product list suitable for Markdown rendering with product images and links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include product name, image URL, price, coupon price, subsidy amount, shop and brand names, category fields, sales, rating, and buy URL.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
