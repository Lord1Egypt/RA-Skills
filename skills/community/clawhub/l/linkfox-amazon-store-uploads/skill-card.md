## Description:

This third-party skill helps agents create Amazon SP-API upload destinations, compute contentMD5 values, and upload images or attachments to returned presigned URLs for A+ Content, Messaging, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Amazon store operators use this skill to prepare upload resources for Amazon SP-API workflows, especially A+ Content and Messaging attachments. It can guide API-key setup, create upload destinations through LinkFox, compute file digests, upload local file content to returned URLs, and preserve JSON results for later inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local files and upload their bytes to a returned upload URL.

Mitigation: Confirm the selected file is intended for the Amazon workflow and verify that upload URLs come from Amazon or LinkFox before running upload commands.

Risk: The skill uses LinkFox API credentials and may expose sensitive values through environment variables, logs, transcripts, or shell history.

Mitigation: Run with trusted environment variables, avoid sharing command transcripts containing credentials, and rotate any API key that appears in logs or history.

Risk: The onboarding flow can guide phone/SMS account setup and initiate payment-order flows.

Mitigation: Use onboarding only for explicit authentication or billing recovery, and confirm account, plan, payment method, and order details before proceeding.

Risk: The skill persists complete API responses locally, which may include operational or account-related data.

Mitigation: Review saved JSON files before sharing them and remove session data that is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-uploads)
- [API reference](references/api.md)
- [Onboarding reference](references/onboarding.md)
- [Amazon createUploadDestinationForResource reference](https://developer-docs.amazon.com/sp-api/reference/createuploaddestinationforresource)
- [Amazon Create an upload destination guide](https://developer-docs.amazon.com/sp-api/docs/create-an-upload-destination)
- [Amazon Messaging API reference](https://developer-docs.amazon.com/sp-api/docs/messaging-api-v1-reference)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown guidance with shell commands, JSON stdout, and persisted JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes complete responses under a linkfox session data directory and may print summaries for larger responses.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
