## Description: <br>
Search your professional network and research people using the Happenstance API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almostimplemented](https://clawhub.ai/user/almostimplemented) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Professionals, recruiters, founders, and agents use this skill to search connected professional networks, research people, list available groups, and check Happenstance credit usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Happenstance API key that grants access to the user's Happenstance account. <br>
Mitigation: Treat HAPPENSTANCE_API_KEY like a password, provide it only in trusted environments, and avoid exposing it in prompts, logs, or shared outputs. <br>
Risk: Search and research operations can involve professional-network and profile details about people. <br>
Mitigation: Use the skill only when authorized and comfortable sending the relevant person or network information to Happenstance, and limit sharing of returned profile details. <br>
Risk: Search and research requests consume credits and asynchronous work can be rate limited. <br>
Mitigation: Check usage before bulk activity, pace polling and retries, and confirm the user wants to spend credits before starting large searches or research runs. <br>


## Reference(s): <br>
- [Happenstance Developer Documentation](https://developer.happenstance.ai) <br>
- [Happenstance API Base URL](https://api.happenstance.ai) <br>
- [Happenstance API Settings](https://happenstance.ai/settings/api) <br>
- [ClawHub Happenstance Skill](https://clawhub.ai/almostimplemented/happenstance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Text, Markdown] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HAPPENSTANCE_API_KEY and curl; API use may consume Happenstance credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
