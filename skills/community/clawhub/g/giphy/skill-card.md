## Description:

Search and send contextual Giphy GIFs in Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minbang930](https://clawhub.ai/user/minbang930)

### License/Terms of Use:


## Use Case:

Discord users and agent operators use this skill to find a safe-for-work Giphy result for an explicit GIF request or an occasional visual reaction in a conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GIF search keywords are sent to Giphy.

Mitigation: Use concise, non-sensitive search terms and avoid private, identifying, or confidential conversation details.

Risk: The skill requires a Giphy API key to function.

Mitigation: Store the API key in the configured environment variable and avoid exposing it in chat or committed files.

## Reference(s):

- [Giphy Search API endpoint](https://api.giphy.com/v1/gifs/search)
- [ClawHub skill page](https://clawhub.ai/minbang930/skills/giphy)
- [Publisher profile](https://clawhub.ai/user/minbang930)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions and plain text Discord response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a single Giphy page URL when a GIF is found; otherwise returns a short fallback request for more specific keywords.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
