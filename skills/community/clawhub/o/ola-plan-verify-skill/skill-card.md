## Description: <br>
Plan Verify Skill is a CruiseSkillBridge-published skill that submits analysis requests to an external POST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[309441738](https://clawhub.ai/user/309441738) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and skill users can submit plan analysis payloads through the skill's documented POST interface. The publisher should define the real analysis purpose and data boundaries before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends analysis data to an external API while the real purpose and data boundaries are undefined. <br>
Mitigation: Review and trust the external endpoint before use, and do not send confidential prompts, files, credentials, customer data, or proprietary plans unless the publisher documents what is transmitted and how it is protected. <br>
Risk: The artifact documentation contains placeholder capability text, so users may not know what analysis the skill performs. <br>
Mitigation: Require the publisher to document concrete capabilities, inputs, outputs, and applicable scenarios before relying on the skill for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/309441738/skills/ola-plan-verify-skill) <br>
- [CruiseSkillBridge](https://cruiseskillbridge.com) <br>
- [Documented sample POST endpoint](https://httpbin.org/post) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Markdown instructions with a JSON request example; external API response format is not specified] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [External POST request behavior and data boundaries are undefined in the artifact documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
