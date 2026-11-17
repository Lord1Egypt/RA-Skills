## Description:

Kakao Local API CLI: keyword/category search, geocode, reverse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to install and run a Kakao Local API command-line tool for place search, geocoding, and reverse geocoding workflows with JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install executable code from an unpinned external repository that was not included for review.

Mitigation: Review the external repository before installation, prefer a pinned release or commit, and install in an isolated environment such as pipx.

Risk: Kakao Local API requests may send addresses, coordinates, search terms, and nearby-place queries to an external API provider.

Mitigation: Treat location and query values as external API data and avoid submitting sensitive or restricted information unless that use is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/kakao-local-cli)
- [Project homepage](https://github.com/ChloePark85/kakao-local-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KAKAO_REST_API_KEY for authenticated Kakao Local API calls.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
