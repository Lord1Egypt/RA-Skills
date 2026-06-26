## Description: <br>
Search 8 knowledge domains in one query: live web, academic papers, scholarly works, arXiv preprints, biomedical literature, chemical compounds, government datasets, and dictionary results via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plagtech](https://clawhub.ai/user/plagtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route research questions across live web, academic, biomedical, chemistry, government data, and dictionary sources, then synthesize cited results from the selected domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and extracted URLs are sent to the configured external research gateway. <br>
Mitigation: Avoid submitting secrets, proprietary text, regulated personal data, or sensitive investigations unless the gateway and its billing setup have been reviewed. <br>
Risk: The skill uses paid x402 or subscription-backed endpoints and may incur per-call costs. <br>
Mitigation: Review endpoint pricing and configure RESEARCH_API_KEY or wallet access only for users authorized to spend on searches. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/plagtech/multi-search-skill) <br>
- [Research Gateway](https://gateway.spraay.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and cited search results returned as gateway responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESEARCH_API_KEY for authenticated or subscription access; RESEARCH_GATEWAY_URL can override the default gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
