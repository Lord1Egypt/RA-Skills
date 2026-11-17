## Description:

Provides product classification, customs code, HS code, and tax code lookup for goods such as Bluetooth headsets, phone cases, and chargers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orangeboo](https://clawhub.ai/user/orangeboo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trade or compliance operators can ask for product classification, customs code, HS code, and tax code answers. On first use, the skill may request a phone number before returning classification results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects phone numbers before returning classification results.

Mitigation: Require clear user consent, make collection optional or explicitly justified, and document why the phone number is needed.

Risk: Phone numbers and pending questions are retained locally.

Mitigation: Add deletion, retention, and access-protection controls before using the skill with real users.

Risk: Personal data is sent to an external FastGPT service.

Mitigation: Enforce HTTPS and disclose what data is sent to the external service.

Risk: Packaged FastGPT credentials may be bundled with the release.

Mitigation: Remove packaged keys and rotate FastGPT credentials before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orangeboo/skills/goodsclassify)
- [ClawHub publisher profile](https://clawhub.ai/user/orangeboo)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses from a local CLI-backed workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a phone-number prompt before producing a product classification answer.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
