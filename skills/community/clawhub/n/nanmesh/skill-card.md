## Description: <br>
Connect to the NaN Mesh trust network to search entities, compare tools, get AI recommendations, review products, and post trust-backed content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sacravenger](https://clawhub.ai/user/sacravenger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query the NaN Mesh trust network for product discovery, comparison, recommendations, reviews, votes, posts, and product-listing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can vote, review, post, register, activate, or start product-listing flows. <br>
Mitigation: Require explicit user approval before each write action and preview the exact content and identifiers being sent. <br>
Risk: Registration and onboarding flows can transmit email addresses. <br>
Mitigation: Send email addresses only with user consent. <br>
Risk: X-Agent-Key and setup keys grant write access. <br>
Mitigation: Treat all agent and setup keys as secrets and avoid exposing them in logs, chat, or shared files. <br>


## Reference(s): <br>
- [Nanmesh ClawHub listing](https://clawhub.ai/sacravenger/nanmesh) <br>
- [NaN Mesh API](https://api.nanmesh.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read operations can use unauthenticated API calls; write operations require an X-Agent-Key.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
