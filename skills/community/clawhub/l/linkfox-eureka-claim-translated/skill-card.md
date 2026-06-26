## Description: <br>
Retrieves translated patent claim text from the Eureka patent data platform in Chinese, English, or Japanese by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve translated patent claims for one or more patents, including optional family-patent substitution when claims are unavailable. It returns claim text only and does not perform patent search, legal-status analysis, portfolio analytics, or claim comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent lookup requests are sent to LinkFox's Eureka API and may expose patent identifiers or user-provided context to a third-party service. <br>
Mitigation: Use approved API credentials only and avoid sending secrets, private client information, unpublished patent strategy, or unnecessary conversation text. <br>
Risk: The artifact tells agents to send broad interaction feedback to a separate LinkFox endpoint without interrupting the user flow. <br>
Mitigation: Require explicit user approval before feedback submission and limit feedback content to minimal, non-sensitive operational details. <br>


## Reference(s): <br>
- [Eureka API reference](artifact/references/api.md) <br>
- [Eureka Claim Translated on ClawHub](https://clawhub.ai/linkfox-ai/linkfox-eureka-claim-translated) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with translated patent claims and optional JSON output from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; supports patentId or patentNumber, lang values en/cn/jp, replaceByRelated, and batches up to 100 patents.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
