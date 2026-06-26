## Description: <br>
Startup idea validation skill. Helps indie developers validate product ideas, analyze competitive landscapes, and assess market saturation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Indie developers and product builders use this skill to evaluate startup ideas, inspect competitive landscape assumptions, validate user needs, and produce MVP planning guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated market, competitor, and MVP recommendations are template-based and may be generic or outdated. <br>
Mitigation: Treat the reports as planning guidance, verify claims with current market research, and keep missing or uncertain values marked as unavailable. <br>
Risk: The artifact imports a network-capable dependency and exposes web flags, although live web research is not currently implemented. <br>
Mitigation: Re-review future versions if real web research is added or if capability tags are used for permission decisions. <br>


## Reference(s): <br>
- [YC Guide to Product Market Fit](https://www.ycombinator.com/library/5z-the-real-product-market-fit) <br>
- [YC Startup School](https://www.ycombinator.com/ys) <br>
- [Pre-Build Idea Validator Agent Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/pre-build-idea-validator.md) <br>
- [Market Research Product Factory Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/market-research-product-factory.md) <br>
- [Hacker News: AI Startup Idea Validation Tool Discussion](https://news.ycombinator.com/item?id=41986396) <br>
- [Reddit r/startups: Idea Validator AI](https://www.reddit.com/r/startups/comments/1055d61yyz/idea_validator_ai/) <br>
- [WeChat: YC Startup Methodology and AI Product-Market Fit Validation](https://mp.weixin.qq.com/s/UKUXDPXDWTGUNLGOOWTZXV) <br>
- [Xiaohongshu: Startup Idea Validation and Market Space Analysis](https://www.xiaohongshu.com/explore/645265627819645573051491) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports printed to stdout, with command-line execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include key findings, metric tables, detailed analysis, and prioritized recommendations; missing data is marked as Data Unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
