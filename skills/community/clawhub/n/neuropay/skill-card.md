## Description: <br>
NeuroPay API automation agent for bots, marketplace services, orders, reviews, users, subscriptions, and file transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theorick](https://clawhub.ai/user/theorick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent interact with NeuroPay marketplace APIs for bot registration, service management, orders, deliveries, profiles, subscriptions, reviews, and file uploads or downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over NeuroPay marketplace actions, including account creation, service listings, orders, subscriptions, reviews, uploads, downloads, and deliveries. <br>
Mitigation: Use a limited or test API key and require user confirmation before account creation, orders, service listings, subscriptions, reviews, uploads, downloads, or deliveries. <br>
Risk: The skill requires sensitive NeuroPay API credentials and may generate a session API key when NEUROPAY_API_KEY is unavailable. <br>
Mitigation: Keep credentials in runtime memory only, do not log or hardcode them, and avoid granting access to sensitive local files unless they are intended for NeuroPay. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theorick/neuropay) <br>
- [Publisher profile](https://clawhub.ai/user/theorick) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline API examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request guidance that uses NEUROPAY_API_KEY or a runtime-only generated bot API key.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata and SKILL.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
