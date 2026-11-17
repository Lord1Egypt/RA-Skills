## Description:

Connect to Google Search and Gemini through the built-in local-mcp Google adapter and one fixed UXC link. Use when the user wants to run Google searches, chat with Gemini, or download generated Gemini images from an authenticated browser profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to Google Search and Gemini through an authenticated local browser profile for search, chat, and generated image download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated Google browser profile for Search and Gemini.

Mitigation: Use a dedicated Google profile that is separate from personal browsing and avoid secrets or regulated data in prompts and searches.

Risk: Fresh installs may resolve the latest Playwright package through npx.

Mitigation: Prefer a pinned or lockfile-managed Playwright install before using the bridge.

Risk: Gemini may require sign-in before tools work through the managed profile.

Mitigation: Check authentication state first and use the documented bootstrap or headed session flow when the profile is not ready.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Google Search](https://www.google.com)
- [Gemini](https://gemini.google.com)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/google-webmcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results are expected as JSON with ok/data on success and ok/error on failure.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
