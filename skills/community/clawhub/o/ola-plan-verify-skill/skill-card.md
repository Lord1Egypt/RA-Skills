## Description:

Plan Verify Skill is a CruiseSkillBridge-published skill that provides a POST request pattern for submitting analysis input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill as a ClawHub-installed agent skill for submitting plan-analysis requests through a CruiseSkillBridge-published POST interface. Review data handling before sending sensitive plans or proprietary content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis input may be sent to an external API or replacement gateway without documented data handling terms.

Mitigation: Do not use confidential, personal, credential, proprietary, or security-sensitive content unless the publisher documents routing, logging, retention, and user consent controls.

Risk: The artifact contains placeholder capability text, so the actual plan-verification behavior is not fully documented.

Mitigation: Require publisher documentation for real capabilities, inputs, outputs, and applicable scenarios before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/309441738/skills/ola-plan-verify-skill)
- [Publisher profile](https://clawhub.ai/user/309441738)
- [CruiseSkillBridge](https://cruiseskillbridge.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions, Shell commands, JSON]

**Output Format:** [Markdown guidance with JSON request examples and shell installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit user-provided input to an external POST endpoint or replacement gateway.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
