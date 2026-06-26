## Description: <br>
Queries LinkFox's SIF keyword overview API to analyze Amazon keyword competition, search volume, product counts, ad presence, and supply-demand metrics across supported marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketplace analysts, and e-commerce operators use this skill to assess Amazon keyword-level competition, search demand, advertising density, and supply-demand balance. It is most useful when comparing keyword opportunity across one or more supported Amazon marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keyword research queries and the LinkFox API key are sent to LinkFox services. <br>
Mitigation: Install only when LinkFox is trusted for the intended data, keep API keys in the agent environment, and avoid submitting confidential product plans, customer data, or secrets as keywords. <br>
Risk: The feedback behavior may send user reactions or task context to a separate LinkFox service. <br>
Mitigation: Require user consent or environment-level blocking for the feedback endpoint, and review feedback content before any transmission. <br>


## Reference(s): <br>
- [SIF Keyword Overview API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-sif-keyword-overview) <br>
- [LinkFox Skill Catalog](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; each request analyzes one keyword for one supported Amazon marketplace.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
