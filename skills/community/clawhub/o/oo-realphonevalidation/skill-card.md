## Description: <br>
RealPhoneValidation helps agents validate individual 10-digit phone numbers through OOMOL's connected RealPhoneValidation connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to validate phone numbers and retrieve available caller enrichment fields through a connected RealPhoneValidation account. It is suited for workflows that need schema-guided connector calls and JSON responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected RealPhoneValidation account and may depend on account credentials, scopes, and billing state. <br>
Mitigation: Use the OOMOL-connected account flow described by the skill, avoid handling raw API tokens, and resolve authentication, scope, credential, or billing errors before retrying. <br>
Risk: Incorrect action payloads can lead to failed validation calls or misleading results. <br>
Mitigation: Inspect the live connector schema before constructing each action payload and pass only fields supported by that schema. <br>


## Reference(s): <br>
- [RealPhoneValidation homepage](https://realphonevalidation.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-realphonevalidation) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action payloads and returns RealPhoneValidation data with execution metadata when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
