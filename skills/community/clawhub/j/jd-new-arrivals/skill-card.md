## Description: <br>
Provides JD self-operated new-arrival product recommendations with keyword, price, review-rate, sorting, and pagination filters, returning product details, image URLs, and purchase links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping assistants use this skill to find JD self-operated new arrivals by category, budget, review threshold, and discount priority. It helps compare product options and follow purchase links, but does not place orders or create arrival alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to the publisher's Tencent cloud proxy. <br>
Mitigation: Install only if this data flow is acceptable for the intended users and review the publisher before deployment. <br>
Risk: The security review reports a reusable proxy token and broader JD affiliate operations than the advertised new-arrivals feature. <br>
Mitigation: Treat the release as suspicious until the publisher rotates and scopes the token, narrows the backend surface, and the deployment is re-reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/jd-new-arrivals) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, markdown, guidance] <br>
**Output Format:** [JSON string with summary text and product-list JSON; image URLs and purchase links may be rendered as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns paginated product recommendations with names, prices, discounts, review rates, sales counts, image URLs, and purchase links.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
