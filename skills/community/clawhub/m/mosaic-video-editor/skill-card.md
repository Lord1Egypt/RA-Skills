## Description:

AI-powered video editing via the Mosaic API for creating agents, running video workflows, managing social accounts, publishing content, uploading assets, and handling credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyle1373](https://clawhub.ai/user/kyle1373)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to automate Mosaic video editing workflows: create or manage agents, run edits on uploaded or linked media, publish outputs to social platforms, and manage credits or billing when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Mosaic API-key access can authorize actions across the user's Mosaic account.

Mitigation: Use a session-scoped or limited token when available, keep the key in the environment, and confirm account scope before making API calls.

Risk: Billing, plan upgrades, and auto top-ups can create costs.

Mitigation: Review plan details, credit thresholds, quantities, and checkout requirements with the user before approving upgrades or auto top-ups.

Risk: Social publishing actions can connect, update, delete, or publish public content on linked platforms.

Mitigation: Confirm the exact platform, account, post, title, description, media, and requested action before publish, update, delete, or disconnect calls.

Risk: Uploaded media and webhook URLs may expose user content or send callbacks to untrusted destinations.

Mitigation: Use only media the user is authorized to upload and only trusted callback or webhook URLs.

## Reference(s):

- [Mosaic Video Editor Skill Page](https://clawhub.ai/kyle1373/skills/mosaic-video-editor)
- [Mosaic Homepage](https://edit.mosaic.so)
- [Mosaic API Reference](https://docs.mosaic.so/api/introduction)
- [Mosaic API Endpoint Map](references/docs-endpoints.md)
- [Mosaic Node Reference](nodes/README.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with JSON and HTTP command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOSAIC_API_KEY and can guide API calls that affect Mosaic account state, billing, social publishing, and uploaded media.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
