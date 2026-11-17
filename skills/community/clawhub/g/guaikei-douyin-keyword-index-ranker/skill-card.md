## Description:

This skill helps agents collect structured JSON from public Douyin keyword searches, creator posts, video comments, and real-time hot lists for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and content research teams use this skill to query public Douyin search results, creator posts, video comments, and hot-list data for short-video planning, competitor monitoring, public-comment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party guaikei.com API and sends Douyin research requests with GUAIKEI_API_TOKEN as a credential.

Mitigation: Install only if third-party API use is acceptable, keep GUAIKEI_API_TOKEN in the environment, avoid exposing the token in prompts or logs, and avoid sending sensitive research targets unless intended.

Risk: The skill saves result logs under logs/, which may retain searched keywords, account identifiers, video identifiers, comments, or trend data.

Mitigation: Review or delete generated logs after use and avoid collecting data that should not be retained locally.

Risk: The activation guidance can apply to generic short-video, trend, or competitor-research requests even when the user does not explicitly say Douyin.

Mitigation: Prefer explicit Douyin-scoped prompts or confirm the target platform before using the skill for broad trend research.

## Reference(s):

- [Skill README](readme.md)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Guaikei API token documentation](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [Structured JSON on stdout, stderr logs, and JSON log files saved under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; outputs are documented by the bundled JSON Schema files.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
