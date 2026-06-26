## Description: <br>
Queries EHunt Temu store data through LinkFox so agents can filter stores by name or ID, country site, category, fulfillment mode, sales, revenue, ratings, reviews, followers, product count, and opening date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and commerce operators use this skill to retrieve and compare Temu store records from LinkFox/EHunt for product sourcing, seller discovery, and store performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends user-supplied Temu store search and filter terms to LinkFox/EHunt. <br>
Mitigation: Install only when that data sharing is acceptable, keep LINKFOXAGENT_API_KEY out of logs and committed files, and send only the query terms needed for the task. <br>
Risk: Persisted large responses may contain sensitive store, pricing, or user-relevant query data. <br>
Mitigation: Use a temporary output directory outside any git working tree, review saved files before sharing, and delete them after use. <br>
Risk: Feedback submission can disclose user intent, results, or issue details to the feedback API. <br>
Mitigation: Submit feedback content only after the user has explicitly agreed to share it. <br>


## Reference(s): <br>
- [EHunt Temu Store Query API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-ehunt-temu-store-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API parameters and optional shell commands; API responses are JSON and large responses may be persisted to files for selective reading.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for direct script use; optional response helper can write full API responses to a temporary output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
