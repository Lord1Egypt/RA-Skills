## Description:

Checks product images with LinkFox Ruiguan design-patent detection to surface visually similar patents, TRO enforcement signals, similarity scores, and AI radar analysis across supported regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers, IP professionals, and agents use this skill to check product image URLs or local product images for design-patent similarity, TRO enforcement signals, and region-scoped risk indicators before listing or reviewing products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local product images may be uploaded to a public URL for patent checking.

Mitigation: Use only images and product details that may be shared with LinkFox and potentially exposed through a public image URL; avoid confidential or regulated images.

Risk: API keys, account details, billing actions, or order data may appear in logs or transcripts during onboarding and payment flows.

Mitigation: Use onboarding and billing commands only when account management is intended, minimize transcript exposure, and rotate any API key that appears in logs or shared conversations.

Risk: Patent-check responses and sensitive product details are written to local session data files.

Mitigation: Review saved LinkFox data directories before sharing a workspace or transcript, and delete files that contain confidential product or account information when no longer needed.

Risk: Detection output can support risk assessment but is not legal advice.

Mitigation: Treat similarity scores, TRO signals, and radar analysis as screening indicators and consult a qualified IP attorney before making legal or commercial decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-ruiguan-detection-patent-design)
- [LinkFox Publisher Profile](https://clawhub.ai/user/linkfox-ai)
- [Ruiguan API Reference](artifact/references/api.md)
- [Authentication and Billing Onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with JSON API parameters, shell commands, and saved JSON response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved to LinkFox session data directories; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
