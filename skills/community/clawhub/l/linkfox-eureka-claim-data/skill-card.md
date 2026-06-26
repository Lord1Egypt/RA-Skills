## Description: <br>
Retrieves patent claim text and claim counts from the Eureka patent database for one or more patent IDs or publication numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and patent-focused agents use this skill to retrieve, count, compare, and present patent claims from Eureka by patent ID or publication number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive LinkFox API key to retrieve patent-claim data. <br>
Mitigation: Store the API key only in LINKFOXAGENT_API_KEY, restrict access to the runtime environment, and rotate the key if exposure is suspected. <br>
Risk: Interaction feedback may be sent to a separate LinkFox service without interrupting the user's flow. <br>
Mitigation: Avoid confidential patent strategy, unpublished invention details, and sensitive business context unless feedback reporting is removed or requires explicit user approval. <br>
Risk: Eureka database coverage and claim availability may be incomplete for some patents, especially recent or early-stage applications. <br>
Mitigation: Tell users when no claims are returned, suggest checking identifiers, and use replaceByRelated only when related-patent fallback is appropriate. <br>


## Reference(s): <br>
- [Eureka claim data API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-eureka-claim-data) <br>
- [LinkFox publisher profile](https://clawhub.ai/user/linkfox-ai) <br>
- [Eureka claim data endpoint](https://tool-gateway.linkfox.com/tool-eureka/claimData) <br>
- [LinkFox feedback endpoint](https://skill-api.linkfox.com/api/v1/public/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with patent-claim summaries, claim text, counts, fallback notices, and optional command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one patentId or patentNumber and may use replaceByRelated for related-patent fallback.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
