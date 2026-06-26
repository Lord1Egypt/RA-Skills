## Description: <br>
Send real-time alerts to NotiLens from any script, app, or AI agent - task lifecycle events, errors, completions, and metric tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notilens](https://clawhub.ai/user/notilens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this plugin to let agents and scripts report task lifecycle events, failures, retry loops, human-input requests, and generated outputs to NotiLens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin sends caller-provided messages, URLs, tags, and metadata to NotiLens. <br>
Mitigation: Do not include secrets, raw prompts, customer data, private URLs, or sensitive error text in message, URL, or meta fields. <br>
Risk: The plugin requires NotiLens credentials in environment variables. <br>
Mitigation: Use a dedicated NotiLens token and secret with the minimum scope needed for the topic. <br>


## Reference(s): <br>
- [NotiLens homepage](https://www.notilens.com) <br>
- [ClawHub skill page](https://clawhub.ai/notilens/notilens-clawhub-plugin) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/notilens) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, text, configuration] <br>
**Output Format:** [JavaScript function calls with JSON-compatible notification payloads and webhook responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTILENS_TOKEN and NOTILENS_SECRET; sends caller-provided messages, URLs, tags, and metadata to NotiLens.] <br>

## Skill Version(s): <br>
0.2.0 (source: SKILL.md frontmatter, package.json, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
