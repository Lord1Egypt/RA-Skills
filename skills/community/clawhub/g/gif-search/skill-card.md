## Description:

Search Tenor for GIFs and return matching media links, trending results, random picks, or metadata for a GIF ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and automation agents use this skill to query Tenor for GIF search results, trending GIF descriptions, random GIF media URLs, or metadata for a known GIF ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the package recommends downloading and running mutable remote Python code.

Mitigation: Use the bundled artifact or a pinned release with a verified checksum instead of a mutable curl command.

Risk: GIF queries are sent to Tenor and may disclose search terms.

Mitigation: Avoid sensitive search terms and use an appropriately restricted TENOR_API_KEY.

Risk: The included verifier can inspect and run checks against folders supplied to it.

Mitigation: Run verifier commands only on trusted folders or inside a sandbox.

Risk: Security evidence notes that documentation does not match the actual tool behavior.

Mitigation: Validate expected commands against the bundled gif_search.py before relying on claimed bulk download, caching, or conversion features.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/gif-search)
- [Tenor API endpoint](https://tenor.googleapis.com/v2)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [CLI text output with GIF descriptions, IDs, media URLs, and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to Tenor and an optional TENOR_API_KEY environment variable.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
