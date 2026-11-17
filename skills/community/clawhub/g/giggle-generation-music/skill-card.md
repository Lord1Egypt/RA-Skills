## Description:

Generates AI music through giggle.pro from text descriptions, custom lyrics, or instrumental requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit music descriptions, lyrics, or instrumental requests to giggle.pro and later check generation status. It helps create AI-generated music and return generated audio links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, titles, and style instructions are sent to giggle.pro.

Mitigation: Use only content appropriate for that third-party service and avoid submitting confidential material.

Risk: Generated audio may be returned through signed URLs that can grant access to anyone with the full link.

Mitigation: Treat generated audio links as private download links and share them only with intended recipients.

Risk: Runtime use depends on GIGGLE_API_KEY and the requests Python package.

Mitigation: Run the skill in a restricted environment that exposes only the required API key, and pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/giggle-generation-music)
- [Giggle.pro](https://giggle.pro/)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Markdown, Text, Guidance]

**Output Format:** [Markdown and JSON status messages with generated audio links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GIGGLE_API_KEY and may return signed audio URLs for generated music.]

## Skill Version(s):

0.0.10 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
