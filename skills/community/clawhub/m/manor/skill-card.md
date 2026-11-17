## Description:

Install the MANOR Edge app on this Apple silicon Mac and guide the owner through pairing it with their home and adding cameras. Use when the owner asks to install, set up or check MANOR Edge on this Mac, asks whether it is already installed or paired, asks how MANOR Free differs from Premium, or wants help adding a camera. Downloads the notarized app from downloads.mymanor.click, verifies its SHA-256 checksum, signing team and Apple notarization, copies it into /Applications, and opens the pairing window. The owner approves the code the app shows in their own MANOR account; the agent never handles a key or a sign-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getmanor](https://clawhub.ai/user/getmanor)

### License/Terms of Use:

MIT-0

## Use Case:

Mac owners use this skill to install or check MANOR Edge on an Apple silicon Mac, understand Free and Premium setup, and get owner-led pairing and camera setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Premium setup can prompt for macOS administrator approval.

Mitigation: The owner should review the prompt and approve it themselves only when proceeding with the expected Premium setup.

Risk: Pairing keys and camera passwords are sensitive credentials.

Mitigation: The owner enters credentials directly in MANOR's account or app; the agent must not request, handle, or repeat them.

## Reference(s):

- [MANOR Edge download and setup](https://mymanor.click/download)
- [MANOR account and pairing approval](https://mymanor.click/account)
- [MANOR plans and pricing](https://mymanor.click/pricing)
- [MANOR support](https://mymanor.click/support)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
