## Description:

Browser automation CLI for AI agents that interact with websites by navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, and automating browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libi](https://clawhub.ai/user/libi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to drive Chrome or Chromium through the ko-browser CLI for browser interaction, data extraction, web app testing, screenshots, session workflows, and related automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over browser sessions, including logged-in accounts.

Mitigation: Use it only where browser automation is appropriate, avoid high-value accounts, and require explicit approval before login or sensitive browser actions.

Risk: Profiles, auth state files, recordings, traces, downloads, clipboard data, cookies, storage, and credentials can expose sensitive information.

Mitigation: Control where these files and data are stored, keep them out of shared workspaces, and approve access to cookies, storage, clipboard, uploads, downloads, recordings, traces, and session export.

Risk: Installation examples use an unpinned upstream kbr version.

Mitigation: Pin and verify the upstream kbr version before installation or deployment.

Risk: Raw debugging access and JavaScript evaluation can alter page state or expose page data.

Mitigation: Require explicit approval before CDP URL use, JavaScript evaluation, and debugging operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libi/skills/ko-browser)
- [Google Chrome download](https://www.google.com/chrome/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated browser artifacts such as screenshots, PDFs, traces, recordings, downloads, state files, and JSON output when those commands are used.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
