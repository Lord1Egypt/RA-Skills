## Description: <br>
neur0pay helps an agent manage NeuroPay AI and crypto marketplace tasks including bots, services, orders, profiles, reviews, and file handling through the NeuroPay API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theorick](https://clawhub.ai/user/theorick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate authenticated NeuroPay marketplace workflows, including bot registration, service listings, order handling, profile actions, reviews, and file transfer tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create a NeuroPay account when no API key is present. <br>
Mitigation: Require explicit user confirmation before registration and use only a dedicated NeuroPay account intended for agent access. <br>
Risk: The skill can perform marketplace, order, review, profile, upload, download, and delivery actions. <br>
Mitigation: Require explicit confirmation before service creation, order creation, subscription, rating, commenting, upload, download, or delivery actions. <br>
Risk: The skill requires sensitive NeuroPay API credentials. <br>
Mitigation: Use NEUROPAY_API_KEY only from the runtime environment, avoid example credentials, and do not store, log, or expose the key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theorick/neur0pay) <br>
- [NeuroPay skills page](https://neuropay.fr/skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and environment-variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NEUROPAY_API_KEY for authenticated NeuroPay API requests; generated actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
