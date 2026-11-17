## Description:

Persistent Browser Scraper uses Playwright persistent browser context to extract text from login-required sites such as YouTube, GitHub, Hugging Face, Reddit, Kaggle, and X/Twitter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckncg](https://clawhub.ai/user/ckncg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to browse authenticated or JavaScript-rendered web pages with a persistent browser profile and return extracted page text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browsing with a persistent logged-in profile can expose the main identity and session state to broad browsing requests.

Mitigation: Use a dedicated automation profile and require explicit confirmation before browsing authenticated content.

Risk: Deleting browser profile lock files can interfere with an active profile.

Mitigation: Do not delete SingletonLock unless you have verified the profile is not in use.

Risk: Launching Chromium with --no-sandbox reduces browser isolation.

Mitigation: Remove --no-sandbox unless the execution environment specifically requires it and compensating controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckncg/skills/persistent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; runtime result is extracted plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers plain-text extraction over screenshots.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
