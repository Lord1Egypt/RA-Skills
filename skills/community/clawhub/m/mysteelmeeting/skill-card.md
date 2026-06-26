## Description: <br>
Searches Mysteel conference listings on huizhan.mysteel.com by industry, region, province, status, charge type, activity type, keyword, and pagination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyb92](https://clawhub.ai/user/wyb92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find Mysteel industry conferences and meeting registration options using natural language filters for sector, location, status, and pricing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases could run a Mysteel conference web query when the user intended a general meeting or location question. <br>
Mitigation: Use explicit prompts that name Mysteel meeting search, and ask for clarification before using the skill for ambiguous meeting requests. <br>
Risk: Conference-search terms are sent to huizhan.mysteel.com and small local cache files may be kept. <br>
Mitigation: Avoid sensitive search terms, install only when this data sharing is acceptable, and use the cache-clear option when local cached category data should be removed. <br>


## Reference(s): <br>
- [Mysteel Meeting API Reference](artifact/references/api_reference.md) <br>
- [Mysteel conference activity API](https://huizhan.mysteel.com/event/activity) <br>
- [ClawHub skill page](https://clawhub.ai/wyb92/mysteelmeeting) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Human-readable terminal text and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include conference names, locations, dates, status, fees, detail URLs, matched industry or area IDs, and cache-management guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
