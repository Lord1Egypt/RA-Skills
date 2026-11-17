## Description:

Linkfox OS routes prompts to LinkFox's async e-commerce agent pipeline for platform data queries, market analysis, product selection, listing optimization, product media generation, IP checks, sourcing, and multi-step seller workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, e-commerce operators, and external sellers use this skill to submit one-shot tasks to specialized LinkFox agents for marketplace research, listing work, product media, onboarding, file upload, and cross-platform seller workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, API keys, uploaded local files, login data, and payment choices may be sent through the LinkFox workflow.

Mitigation: Install only if you trust LinkFox, use official LinkFox endpoints, avoid submitting confidential material, and store API keys in a secure secret store instead of shell rc files.

Risk: Generated share links may expose task process and result data for up to one year.

Mitigation: Treat share links as public links and avoid sharing or generating them for sensitive tasks.

Risk: File upload behavior can place user-provided images, documents, or videos in hosted storage for downstream agent use.

Mitigation: Upload only files intended for LinkFox processing and review file contents before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-os)
- [LinkFox OS homepage](https://os.linkfox.com/)
- [linkfox-os API reference](references/api.md)
- [Agent capabilities reference](references/capabilities.md)
- [Onboarding guide](references/onboarding.md)
- [Onboarding API contract](references/onboarding-api.md)
- [Amazon ecosystem skills](references/skills-amazon.md)
- [Cross-platform e-commerce skills](references/skills-third-platforms.md)
- [Market analysis skills](references/skills-market-analysis.md)
- [Product selection skills](references/skills-selection.md)
- [Listing skills](references/skills-listing.md)
- [Image, video, and text generation skills](references/skills-media.md)
- [IP and compliance detection skills](references/skills-ip-compliance.md)
- [General tool skills](references/skills-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown progress and results with JSON command outputs and local or hosted file links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and may upload user-provided files or return public share links.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
