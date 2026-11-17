## Description:

Save bookmarks to Karakeep (self-hosted bookmark manager). Use when the user wants to save a URL, bookmark a link, or add something to their reading list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickian](https://clawhub.ai/user/nickian)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to save links and optional notes to a configured self-hosted Karakeep bookmark manager.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided URLs and optional notes to the configured Karakeep server using an API key.

Mitigation: Install only when this data transfer is intended, configure the destination Karakeep instance deliberately, and keep KARAKEEP_API_KEY scoped and private.

Risk: Using a plain HTTP KARAKEEP_URL can expose the API key and bookmark data in transit.

Mitigation: Use an https:// Karakeep URL except for tightly controlled local testing, and rotate the API key if it may have crossed an untrusted HTTP connection.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KARAKEEP_URL, KARAKEEP_API_KEY, curl, and jq; sends the supplied URL and optional note to the configured Karakeep server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
