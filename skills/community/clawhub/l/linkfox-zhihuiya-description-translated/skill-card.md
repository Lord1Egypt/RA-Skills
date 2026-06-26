## Description: <br>
Retrieves translated Zhihuiya patent description text in Chinese, English, or Japanese by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and patent-focused agents use this skill to retrieve translated patent specification text for known patent IDs or publication numbers, including optional family-member substitution when the original description is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers, user comments, intent, or other sensitive patent-matter details may be sent to LinkFox or Zhihuiya endpoints. <br>
Mitigation: Use only with authorization to share those details with LinkFox/Zhihuiya, and avoid confidential patent matters unless the data-sharing terms are acceptable. <br>
Risk: The skill instructs the agent to automatically submit broad feedback to a separate LinkFox feedback endpoint. <br>
Mitigation: Disable feedback submission or require explicit user confirmation before sending feedback content or user context. <br>


## Reference(s): <br>
- [Zhihuiya API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-description-translated) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and translated patent description text, with JSON API responses when the script is run directly.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key and one or more patent identifiers; supports target language selection and optional family-member fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
