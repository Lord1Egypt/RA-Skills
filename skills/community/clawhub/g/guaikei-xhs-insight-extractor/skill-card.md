## Description:

Searches public Xiaohongshu notes by keyword and retrieves note details, author information, engagement metrics, comments, creator posts, and source links for social content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, market researchers, and analysts use this skill to collect structured public Xiaohongshu data for topic discovery, competitor monitoring, KOL screening, trend research, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be exposed because the security evidence reports that request URLs can include credential material.

Mitigation: Use a limited, rotatable Guaikei token; avoid shared terminals and CI logs; rotate the token if it has been printed or logged.

Risk: The skill automatically saves token-bearing links and retrieved public Xiaohongshu data locally.

Mitigation: Protect or clean the generated logs/ directory after use, and avoid pasting token-bearing Xiaohongshu URLs into public places.

Risk: The security verdict is suspicious even though no specific risk findings were listed.

Mitigation: Review before installing and confirm that data collection, storage, and external API use fit the intended authorization scope.

## Reference(s):

- [Guaikei website](https://www.guaikei.com)
- [Skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-insight-extractor)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON results with command-line status messages and saved log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and a GUAIKEI_API_TOKEN; commands may save retrieved public data and request metadata under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
