## Description: <br>
Provides a simplified set of 10 free search engine options focused on domestic and accessible search routes for finding current information online. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhc888007](https://clawhub.ai/user/jhc888007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to choose from a short list of search providers, especially China-accessible search routes, when looking up current information online. It is a search-helper skill rather than a result aggregation tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to and logged by third-party search providers. <br>
Mitigation: Do not use private passwords, keys, confidential business information, or sensitive personal details as search queries. <br>
Risk: The skill may try one search route and stop after a successful response, so results are not an exhaustive multi-engine aggregation. <br>
Mitigation: Ask the agent to try specific listed providers when broader comparison or provider diversity is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jhc888007/multi-search-engine-simple) <br>
- [Artifact README](artifact/README.md) <br>
- [Search engine configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown guidance with search engine URLs and query templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not aggregate all engine results; the agent may choose one accessible provider and stop after a successful request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
