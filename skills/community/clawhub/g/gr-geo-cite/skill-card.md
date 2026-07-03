## Description: <br>
GEO citation tracking and optimization skill that helps agents audit whether Claude, GPT, Perplexity, and Gemini cite a target domain, then prepare Citable Statistics and llms.txt updates for better AI citation readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gingiris-1031](https://clawhub.ai/user/gingiris-1031) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and growth operators use this skill to check whether AI answer engines cite their domain for fixed weekly queries and to generate concrete GEO improvements such as Citable Statistics blocks, FAQ Schema guidance, and llms.txt content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports under-disclosed outbound calls to AI providers and GitHub using environment credentials. <br>
Mitigation: Install only after reviewing the provider behavior, use narrowly scoped API keys, and run the scripts in an environment where those credentials are intentionally available. <br>
Risk: The weekly citation checker includes a DeepSeek fallback branch that is not part of the four-provider workflow described in the public skill summary. <br>
Mitigation: Review or remove the DeepSeek branch unless that provider is explicitly required for the deployment. <br>
Risk: The URL citability scorer fetches arbitrary pages supplied by the user. <br>
Mitigation: Avoid running it against internal, private, or sensitive URLs; prefer local file input for private content. <br>
Risk: Generated citation reports and llms.txt content may contain inaccurate, stale, or publication-sensitive claims. <br>
Mitigation: Treat generated reports and llms.txt output as review-before-publish material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gingiris-1031/gr-geo-cite) <br>
- [Publisher profile](https://clawhub.ai/user/gingiris-1031) <br>
- [Gingiris Growth Tools](https://gingiris.tools/) <br>
- [geo-seo-claude citability scorer reference](https://github.com/zubair-trabzada/geo-seo-claude) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON citation reports, llms.txt text, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use API credentials for AI providers and GitHub when running bundled scripts; generated reports and llms.txt output should be reviewed before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
