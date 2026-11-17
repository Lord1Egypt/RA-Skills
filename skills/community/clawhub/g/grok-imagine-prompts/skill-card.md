## Description:

Searches community-curated Grok Imagine video generation prompts from X/Twitter and helps agents present prompt previews, source links, and YouMind gallery links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find community examples for Grok Imagine video prompt creation, browse recent prompt ideas, and receive concise Markdown results with attribution and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to YouMind's API.

Mitigation: Avoid submitting sensitive or confidential search terms, and review whether use of the external prompt API fits the deployment environment.

Risk: Installer commands may execute third-party package code.

Mitigation: Prefer the ClawHub install path, or pin and review any npx-based installer before use.

Risk: Prompt results require visible YouMind attribution when displayed.

Mitigation: Keep the attribution link in responses that present prompt results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dophinl/skills/grok-imagine-prompts)
- [YouMind Grok Imagine Gallery](https://youmind.com/grok-imagine-prompts)
- [YouMind video prompts API](https://youmind.com/youhome-api/video-prompts)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with prompt previews, source links, gallery links, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents up to three prompt results per search and includes YouMind attribution when prompts are shown.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
