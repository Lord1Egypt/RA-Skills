## Description: <br>
Ozon product-selection skill that searches market trends for a user-specified category, extracts promising niche keywords, calls 1688 search APIs, filters candidates, and recommends the best products for each niche. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators and sourcing teams use this skill to identify Ozon product opportunities, search matching 1688 supply, apply price and operational filters, and produce concise product recommendations with SKU-level details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AlphaShop API credentials and may expose sensitive keys if they are pasted into shared chats or committed to files. <br>
Mitigation: Configure ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY through the platform environment or a secrets manager, and do not paste real keys into shared chats or source control. <br>
Risk: AlphaShop searches can consume quota or paid credits, and insufficient balance can interrupt the workflow. <br>
Mitigation: Monitor AlphaShop quota and billing before running repeated searches, and stop the workflow when the API reports insufficient balance. <br>
Risk: Unpinned or stale dependencies can increase maintenance and supply-chain risk. <br>
Mitigation: Run the skill in a controlled environment with pinned, current dependency versions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1688AiInfra/ozon-product-selection) <br>
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management) <br>
- [AlphaShop API billing and credits](https://www.alphashop.cn/seller-center/home/api-list) <br>
- [AlphaShop skill hub](https://skill.alphashop.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown product recommendations with tables, image links, product links, SKU details, plus JSON returned by the search script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs up to three product recommendations after applying optional price, MOQ, 48-hour shipping-rate, and sales filters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
