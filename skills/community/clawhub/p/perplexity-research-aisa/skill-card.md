## Description: <br>
Produce citation-backed deep research answers through Perplexity Sonar models via AISA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users can use this skill to produce synthesized research, comparative analysis, and long-form cited answers through AISA-backed search and Perplexity Sonar calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AISA API key and sends research queries and user-supplied URLs to api.aisa.one. <br>
Mitigation: Use only with credentials and queries approved for that service, and avoid confidential, internal, localhost, or private-network URLs unless stronger scoping and consent controls are documented. <br>
Risk: The scanner found the runtime broader than the Sonar-focused description because it supports multi-source search and remote URL extraction. <br>
Mitigation: Treat the skill as a broader multi-source web research client, review selected commands before execution, and verify cited outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bibaofeng/perplexity-research-aisa) <br>
- [AISA API service](https://api.aisa.one/apis/v1) <br>
- [AISA](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Terminal text and citation-backed summaries suitable for Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends research queries or user-supplied URLs to api.aisa.one.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
