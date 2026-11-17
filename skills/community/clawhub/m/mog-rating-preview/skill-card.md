## Description:

Use when a user provides an authorized 18+ face, selfie, or portrait photo and asks for an official MogScore, mog rating, AI face rating, face score, or free Mog Rating preview through the existing MogScore website.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roooo-798](https://clawhub.ai/user/roooo-798)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run the official MogScore free AI Face Rating preview for an authorized 18+ user-supplied face photo and return the preview JSON. The skill is limited to the free preview flow and avoids paid report, identity, medical, surveillance, or non-consensual use cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uploads a sensitive face photo to a website and the base URL is configurable.

Mitigation: Use only photos the user is authorized to submit, assume the photo leaves the machine for processing, and keep MOGSCORE_BASE_URL unset or restricted to the official HTTPS MogScore origin.

Risk: The script accepts a local image path for upload.

Mitigation: Avoid arbitrary local file paths and verify the selected image is the intended user-provided photo before running the workflow.

## Reference(s):

- [MogScore Free AI Face Rating Preview](https://mogscore.ai/mog-rating)
- [ClawHub Skill Page](https://clawhub.ai/roooo-798/skills/mog-rating-preview)
- [Publisher Profile](https://clawhub.ai/user/roooo-798)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON success or failure payload with preview metadata, report data, or retryable error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a readable local image path, Node 20+, playwright-core, and a local Chrome-compatible browser when the host browser cannot complete the workflow.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
