## Description: <br>
Agent skill for x402-paid global news aggregation and source/time-filtered search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parsonssss](https://clawhub.ai/user/parsonssss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to search global news through a paid x402 API, with filters for source domain, publication time, country, and language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid remote news-search API and sends search queries to a third-party service. <br>
Mitigation: Treat searches as third-party API requests and avoid submitting sensitive or confidential queries. <br>
Risk: The skill requires a crypto private key or signer for x402 payments. <br>
Mitigation: Use a dedicated low-balance wallet or delegated signer, keep keys out of prompts, logs, and source control, and require explicit per-call approval or spending limits. <br>
Risk: The artifact labels the skill as local-only even though it calls a remote paid API. <br>
Mitigation: Review the network and payment behavior before installation and deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/parsonssss/multi-news-aggregator) <br>
- [x402 API service](https://www.x402api.app/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes payment-flow handling, search parameters, source and time filters, and error handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
