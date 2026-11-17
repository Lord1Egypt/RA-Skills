## Description:

Read transcripts and summaries from Pocket AI (heypocket.com) recording devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmustier](https://clawhub.ai/user/tmustier)

### License/Terms of Use:

MIT

## Use Case:

Developers and Pocket users use this skill to retrieve, search, and analyze their own Pocket recordings, transcripts, summaries, action items, speaker metadata, and recording metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill extracts a live Pocket account token from browser storage and caches it at ~/.pocket_token.json.

Mitigation: Use it only on a trusted machine and account, treat the token file as a password-equivalent secret, delete it when finished, avoid logged or shared terminals, and require owner-only file permissions.

Risk: The token extraction flow may store refresh-token material and prints an access-token fragment after extraction.

Mitigation: Review the script before installing, avoid storing refresh tokens, remove token-fragment logging, and keep terminal output out of shared logs.

Risk: The skill accesses private Pocket recordings through an unofficial reverse-engineered API.

Mitigation: Confirm the account and recordings are appropriate for agent access before use, and review outputs before sharing them outside the trusted workspace.

## Reference(s):

- [Pocket AI](https://heypocket.com)
- [Pocket Web App](https://app.heypocket.com)
- [Anthropic Browser Skill](https://github.com/anthropics/skills/tree/main/skills/browser)
- [ClawHub Skill Page](https://clawhub.ai/tmustier/skills/heypocket-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; API client calls return transcript text, summary markdown, action-item data, and recording metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Pocket account, Chrome with the browser skill, and a short-lived Firebase bearer token cached at ~/.pocket_token.json.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
