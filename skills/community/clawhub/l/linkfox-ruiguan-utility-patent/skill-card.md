## Description: <br>
Searches for similar US utility and invention patents from product title and description, then helps agents present similarity, validity, and TRO-risk indicators for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and agents use this skill to screen product listings for similar utility or invention patents before selling in a target market. It supports factual patent-risk review, not legal conclusions about infringement. <br>

### Deployment Geography for Use: <br>
Global use; patent search region is currently limited to the US. <br>

## Known Risks and Mitigations: <br>
Risk: Product details are sent to an external LinkFox patent-search service. <br>
Mitigation: Use a dedicated API key and avoid submitting confidential pre-launch product information unless external sharing is acceptable. <br>
Risk: The skill can report user-derived feedback to a separate LinkFox feedback endpoint without interrupting the user's flow. <br>
Mitigation: Require explicit opt-in before calling the feedback endpoint and avoid sending raw user text or sensitive product details. <br>
Risk: Patent similarity results may be mistaken for a legal infringement determination. <br>
Mitigation: Present results as factual screening signals and recommend review by a qualified patent attorney for definitive assessments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-ruiguan-utility-patent) <br>
- [Ruiguan Utility Patent API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown tables and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; product title and description are capped at 1000 characters, region is currently US, and result count is 10-200.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
