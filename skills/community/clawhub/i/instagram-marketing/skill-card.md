## Description: <br>
Generate Instagram marketing content from product URLs, including product information, image suggestions, captions, hashtags, and story or reel ideas optimized for engagement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[insight68](https://clawhub.ai/user/insight68) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External marketers, creators, and ecommerce sellers use this skill to turn public product URLs into Instagram content packages for feed posts, carousels, stories, reels, and campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching a user-provided product URL can expose private, internal, admin, cart, or token-bearing pages if the wrong URL is supplied. <br>
Mitigation: Use only public product pages that are safe to fetch from the execution environment. <br>
Risk: Generated marketing copy may include inaccurate product claims or unsupported promotional language. <br>
Mitigation: Review product details, pricing, claims, captions, and calls to action before publishing. <br>
Risk: Automated product extraction can fail or return incomplete details for some ecommerce pages. <br>
Mitigation: Use the manual extraction fallback and verify product name, price, features, audience, and visual assets against the source page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/insight68/instagram-marketing) <br>
- [Instagram Hashtag Strategy](references/HASHTAG_STRATEGY.md) <br>
- [Instagram Content Package Output Template](templates/OUTPUT_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown content package with optional JSON product extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes product overview, content format rationale, image or video brief, caption, hashtags, posting strategy, engagement preparation, metrics, and repurposing ideas.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
