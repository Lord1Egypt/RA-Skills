## Description:

Downloads text ebooks from Z-Library mirrors and sends them to a configured Kindle email address.

This skill is for research and development only.

## Publisher:

[xiehaixin](https://clawhub.ai/user/xiehaixin)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to search for text ebooks, resolve ambiguous search results, download the selected file, and send it to a Kindle address by email. It requires configured SMTP, Kindle, and Z-Library credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles SMTP and Z-Library credentials.

Mitigation: Use dedicated, low-privilege accounts; prefer environment variables or a secrets manager; if auth.json is used, keep it outside the skill directory with strict local permissions.

Risk: The configured Z-Library mirror list may send credentials or downloads through domains the user has not verified.

Mitigation: Review and verify every mirror domain before use, and avoid entering credentials into unexpected or changed domains.

Risk: Installation guidance includes curl-to-bash and sudo-style dependency installation commands.

Mitigation: Install dependencies from independently verified upstream sources and review installer scripts before running privileged commands.

Risk: The skill downloads files from external sites and emails them as Kindle attachments.

Mitigation: Run the workflow in an isolated user account or container and use it only for content the user is legally permitted to download and send.

Risk: The artifact includes agent-control instructions unrelated to the ebook workflow.

Mitigation: Review the skill instructions before installation and ensure local agent policy takes precedence over skill-authored control language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiehaixin/skills/kindle-download)
- [Publisher profile](https://clawhub.ai/user/xiehaixin)
- [Z-Library](https://zlibrary-global.se/)
- [Amazon Kindle personal documents settings](https://www.amazon.com/myk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Plain text status messages with shell command execution and optional image references for search-result selection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce local ebook file paths, progress messages, and email-send results during the workflow.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
