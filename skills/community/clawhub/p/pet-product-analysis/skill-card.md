## Description: <br>
生成专业的宠物科技用品（智能猫砂盆、自动喂食器等）分析文档，包含产品参数对比、真实用户评测收集（小红书/B站）、优缺点分析，并自动筛选排除厂商软广内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hwl1413520](https://clawhub.ai/user/hwl1413520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to research smart pet products, compare competing products, filter likely sponsored reviews, and generate structured Markdown buying-analysis reports. It is intended for public product research and recommendation workflows, not for handling private account data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review filtering and sponsored-content detection are heuristic and may misclassify authentic or promotional content. <br>
Mitigation: Verify source links, compare multiple independent sources, and treat generated buying advice as research support rather than a final purchasing authority. <br>
Risk: Product prices, availability, firmware features, and user-review sentiment can change over time. <br>
Mitigation: Refresh searches near the purchase date and include the analysis date and source dates in generated reports. <br>
Risk: Using private platform content or account-specific data could expose information the skill does not need. <br>
Mitigation: Use public product information and public reviews by default, and avoid private account data unless permission and need are clear. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/hwl1413520/pet-product-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/hwl1413520) <br>
- [Analysis framework](references/ANALYSIS_FRAMEWORK.md) <br>
- [Sponsored content guide](references/SPONSORED_CONTENT_GUIDE.md) <br>
- [Report template](assets/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with product comparisons, review summaries, scoring tables, source links, and purchase guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured review data and credibility ratings when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
