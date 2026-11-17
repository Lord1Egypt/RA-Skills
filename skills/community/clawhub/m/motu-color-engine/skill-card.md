## Description:

MotuArt Color Engine helps agents call the hosted MotuArt Color Engine API for identity-preserving portrait grading, skin smoothing, segmentation masks, approved outfit replacement, AI headshots, ID/passport crops, compliance checks, upload optimization, and print sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chancipher](https://clawhub.ai/user/chancipher)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare portrait and identity-photo deliverables through the MotuArt Color Engine API, including graded portraits, masks, approved outfit changes, AI headshot candidates, ID/passport crops, compliance reports, upload-ready images, and print sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive portrait, passport, ID, and reusable headshot reference images may be sent to an environment-selected API server along with an API key.

Mitigation: Use a least-privilege MCE_API_KEY, keep MCE_API_BASE unset or restricted to the official HTTPS service unless intentionally using a separate trusted deployment, and avoid pasting full keys into chat or client code.

Risk: Some API-controlled filenames are not safely contained according to the server security evidence.

Mitigation: Run outputs in a dedicated directory and review generated files before reusing or publishing them, especially for headshot candidate downloads and ID-photo packages.

Risk: Processing calls consume account credits and failed credit checks should not be retried unchanged.

Mitigation: Use catalog discovery before processing where possible, surface 402 insufficient_credits responses to the user, and do not retry the same paid request without a user decision.

## Reference(s):

- [MotuArt Color Engine Skill Page](https://clawhub.ai/chancipher/skills/motu-color-engine)
- [MotuArt Developer Homepage](https://mce.motu.art/developers)
- [MotuArt Color Engine API Reference](references/api.md)
- [Headshots API Reference](references/headshots-api.md)
- [Crop Specs Reference](references/crop-specs.md)
- [Styles Reference](references/styles.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands and references to generated image or report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PNG, JPEG, WebP, and JSON report files through API-backed scripts; processing requires scoped API credentials and may consume credits.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
