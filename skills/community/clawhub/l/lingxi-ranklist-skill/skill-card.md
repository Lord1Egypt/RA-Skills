## Description: <br>
国泰海通证券-灵犀市场热榜查询skill，支持涨跌幅、成交额、成交量、换手率、当日资金净流入等市场排行榜查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtht-tech](https://clawhub.ai/user/gtht-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent for A-share market ranking lists such as gainers, losers, turnover, volume, amplitude, valuation, and same-day capital inflow rankings. The skill maps supported rank-list requests to the configured ranklist gateway after API key authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires brokerage API credentials and may save the API key in local workspace-adjacent files. <br>
Mitigation: Use a limited, revocable API key where possible, keep the workspace private, and remove or rotate the key after use. <br>
Risk: The artifact claims Guotai Haitong official status, while server evidence does not prove the publisher is NVIDIA or validate that affiliation. <br>
Mitigation: Verify the publisher's Guotai Haitong affiliation through an official channel before installation or production use. <br>
Risk: Authorization uses QR/API-key flows and may involve localhost proxy behavior. <br>
Mitigation: Review the authorization flow in a controlled workspace before use, especially on shared machines or shared agent environments. <br>
Risk: The skill can fall back to a related financial-search skill when rank-list parameters cannot answer a request. <br>
Mitigation: Confirm installed companion skills and data boundaries before enabling cross-skill fallback in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gtht-tech/lingxi-ranklist-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gtht-tech) <br>
- [Lingxi API key activity](https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1) <br>
- [Ranklist gateway endpoint](https://zx.app.gtja.com:8443/mcp/hq-20200002) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown responses with inline Node.js commands and ranked market-data results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally stored API key before market-data requests; results should preserve requested ranking order and avoid truncating returned entries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 0.0.9) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
