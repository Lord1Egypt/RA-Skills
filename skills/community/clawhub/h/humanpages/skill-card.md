## Description: <br>
Search and hire real humans for tasks -- photography, delivery, research, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[human-pages-ai](https://clawhub.ai/user/human-pages-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search for real people, view profiles, create job offers, coordinate payment workflows, and leave reviews for completed real-world tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive human profile details and payment destination information. <br>
Mitigation: Require user approval before viewing full profiles, and verify recipient identity, wallet address, network, amount, and job status before any payment action. <br>
Risk: The workflow can create offers, record payments, change payment streams, and post reviews in a real hiring marketplace. <br>
Mitigation: Require manual approval before creating offers, marking payments, changing streams, or posting reviews. <br>
Risk: Human Pages API keys and webhook secrets provide account-level access. <br>
Mitigation: Store HUMANPAGES_AGENT_KEY and webhook secrets securely and treat them like account credentials. <br>


## Reference(s): <br>
- [Human Pages](https://humanpages.ai) <br>
- [ClawHub Humanpages release](https://clawhub.ai/human-pages-ai/humanpages) <br>
- [Publisher profile](https://clawhub.ai/user/human-pages-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline commands and MCP tool call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and HUMANPAGES_AGENT_KEY for authenticated Human Pages MCP workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
