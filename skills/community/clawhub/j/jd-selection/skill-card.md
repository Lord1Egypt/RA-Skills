## Description: <br>
京东精选 helps agents search six JD shopping channels for JD self-operated products, with filtering by channel, keyword, price, quality threshold, sort order, and page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to discover JD self-operated products by shopping channel, category keyword, budget, quality threshold, sort order, and page. The skill returns product information, purchase links, and concise browsing guidance; it does not place orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping searches and selected filters are sent through the skill's disclosed cloud proxy. <br>
Mitigation: Avoid entering sensitive personal information in shopping queries, and review the query and filters before relying on results. <br>
Risk: Short follow-up phrases such as "next page" may continue the shopping flow in some agents. <br>
Mitigation: Confirm the intended channel, query, and page before using follow-up results. <br>
Risk: Product prices, inventory, and purchase conditions can change after results are returned. <br>
Mitigation: Verify the final price, stock status, and seller details on JD before making a purchase decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/jd-selection) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON envelope containing a product-list JSON string and a summary string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 50 product entries per page, including names, prices, discount data, shop and brand details, product links, and browsing hints.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
