## Description:

Fetches public Douyin search results, creator posts, comments, and trending topics through JSON-producing Node.js CLIs for content research, competitor analysis, comment insight, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve public Douyin data for short-video topic research, competitor account monitoring, comment analysis, marketing reports, and trend tracking. It is intended for public data lookup and analysis, not publishing, editing, downloading, or private account access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service token may be exposed through URL query parameters.

Mitigation: Use a dedicated, revocable API token; avoid shared environments or logging proxies that retain request URLs; publisher should move the token out of query strings.

Risk: Search terms and Douyin URLs are sent to www.guaikei.com.

Mitigation: Submit only public, non-sensitive research terms and public Douyin URLs; review data-sharing requirements before use.

Risk: Result JSON files are saved under the skill directory.

Mitigation: Review, retain, or delete generated logs according to the user's data handling policy.

Risk: Runtime auth and quota messaging may include promotional or contact guidance that conflicts with the documented neutral-error posture.

Mitigation: Review stdout and stderr behavior before automated use; publisher should remove runtime promotional and contact output.

Risk: Download-related returned fields or behavior may be inconsistent with the documented no-download scope.

Mitigation: Use the skill only for public-data analysis and avoid workflows that download, redistribute, or otherwise reuse media outside platform terms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-public-data-fetcher)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [Guaikei Service Site](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [JSON from stdout, operational messages on stderr, and optional JSON log files under the skill directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and a GUAIKEI_API_TOKEN environment variable; common limits are 1 to 10000 results per request.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog, constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
