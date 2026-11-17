## Description:

Searches torrent indexes for movie magnet links and returns candidate download metadata for lawful, authorized use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beancookie](https://clawhub.ai/user/beancookie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search third-party torrent indexes for media-related magnet links and return ranked result metadata. Use should be limited to lawful, authorized content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches torrent indexes and returns magnet links, creating legal-use ambiguity around copyrighted or unauthorized content.

Mitigation: Restrict use to lawful, authorized content and require users to confirm that requested downloads are permitted in their jurisdiction.

Risk: Search terms are sent to third-party torrent services and network destinations may not be fully disclosed to users.

Mitigation: Review and allow-list external destinations before deployment, and avoid submitting sensitive or confidential queries.

Risk: HTTPS certificate validation is disabled, so network responses and magnet results could be tampered with.

Mitigation: Restore certificate verification or run the skill only in a controlled environment with monitored outbound traffic.

Risk: The package appears incomplete or broken and may not run correctly.

Mitigation: Run syntax and functional tests before enabling the skill for agent use, and block execution until packaging defects are resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beancookie/skills/magnet-search)
- [Publisher profile](https://clawhub.ai/user/beancookie)
- [ThePirateBay API endpoint](https://apibay.org)
- [Nyaa torrent index](https://nyaa.si)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text result listings or JSON records containing title, quality, size, seed and leech counts, source labels, upload dates, and magnet links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-backed results depend on third-party torrent services and user-selected filters such as result limit, minimum seeders, quality, size, and timeout.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
