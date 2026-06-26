## Description: <br>
Retrieves translated patent titles and abstracts from the Zhihuiya (PatSnap) patent database by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Chinese, English, or Japanese translations of patent titles and abstracts for known patent IDs or publication numbers. It supports batch lookup and optional family-patent abstract replacement when the original abstract is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent IDs, publication numbers, and feedback details may be sent to LinkFox services. <br>
Mitigation: Use the skill only when users intend to query LinkFox/PatSnap, and disable or avoid feedback submission unless users explicitly consent. <br>
Risk: The skill requires LINKFOXAGENT_API_KEY for authenticated API access. <br>
Mitigation: Configure LINKFOXAGENT_API_KEY as a secret and avoid exposing it in prompts, logs, or shared command output. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Listing](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-abstract-translated) <br>
- [LinkFox Tool Gateway Abstract Translation API](https://tool-gateway.linkfox.com/zhihuiya/abstractDataTranslated) <br>
- [LinkFox Feedback API](https://skill-api.linkfox.com/api/v1/public/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON API responses and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires patentId or patentNumber; optional parameters include lang and replaceByRelated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
