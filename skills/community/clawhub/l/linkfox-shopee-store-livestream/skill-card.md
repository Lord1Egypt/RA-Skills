## Description:

Provides agent-facing scripts and references for managing authorized Shopee store livestream sessions, products, comments, images, and metrics through Shopee Open API Livestream endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopee store operators and commerce automation agents use this skill to create, start, update, end, inspect, and moderate livestream sessions for authorized Shopee stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopee livestream operations can change live sessions, item lists, comments, and moderation state.

Mitigation: Require explicit user confirmation before deleting items, posting comments, banning users, starting sessions, ending sessions, or applying item sets.

Risk: The skill handles LinkFox API keys, phone/SMS onboarding, billing orders, and payment flows.

Mitigation: Use only in a private workspace, keep API keys out of shared logs and shell history where possible, and install only when LinkFox is trusted for these flows.

Risk: Full responses are persisted to local session files and may contain store or livestream data.

Mitigation: Review saved JSON files before sharing the workspace or outputs, and avoid running the skill in directories that are broadly synchronized or published.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-livestream)
- [Shopee Livestream API index](https://open.shopee.com/documents/v2/v2.livestream.upload_image?module=125&type=1)
- [Artifact API reference](references/api.md)
- [Artifact onboarding reference](references/onboarding.md)

## Skill Output:

**Output Type(s):** [shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with Python command examples, JSON API responses, and saved response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a linkfox session data directory; large responses print summaries unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
