## Description:

Search, browse, and rediscover your Kindle highlights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gofordylan](https://clawhub.ai/user/gofordylan)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Hi Lite to import Kindle highlights into a local markdown library, search and browse those highlights, create themed collections, and optionally fetch highlights from Amazon through a local browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and rewrite the user's local Kindle-highlight library.

Mitigation: Use explicit /hi-lite commands, review import results, and keep a backup of ~/.openclaw/workspace/hi-lite/ before large imports or rewrites.

Risk: The Amazon fetch flow opens a browser and stores a reusable local login profile.

Mitigation: Run fetch only when intended, avoid shared machines for account access, and delete ~/.openclaw/workspace/hi-lite/.browser-data/ when the saved session is no longer needed.

Risk: Custom Amazon domains are not constrained by a documented allowlist.

Mitigation: Avoid custom Amazon domains unless the skill is updated with an allowlist or the domain is independently reviewed.

## Reference(s):

- [OpenClaw](https://openclaw.org)
- [Amazon Kindle Notebook](https://read.amazon.com/notebook)
- [Bookcision](https://readwise.io/bookcision)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses, markdown library files, JSON fetch files, and optional Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under ~/.openclaw/workspace/hi-lite/; optional Amazon fetch stores a local browser profile.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
