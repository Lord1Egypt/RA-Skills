## Description:

Provides Douyin public-data search, creator-post retrieval, comment collection, and real-time hot-list queries for content research, competitor analysis, public-opinion review, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to collect structured JSON from Douyin public content for short-video topic research, competitor monitoring, comment analysis, and hot-list tracking. It is not intended for publishing, editing, downloading videos, follower-growth consulting, private data access, or non-Douyin platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags credential-handling risk because GUAIKEI_API_TOKEN is sent in URL query strings to www.guaikei.com.

Mitigation: Use a scoped token that can be rotated, avoid sharing logs or request traces, and rotate the token after testing or suspected exposure.

Risk: The security evidence notes disclosure mismatches around runtime authentication contact or promotional output.

Mitigation: Review runtime error output before deployment and treat authentication prompts that include contact or promotional content as requiring remediation.

Risk: The skill saves query results locally under logs/, which may contain collected public-data research terms and results.

Mitigation: Use non-sensitive research terms, restrict access to generated log files, and remove logs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-content-decision-data)
- [Guaikei token and usage site](https://www.guaikei.com)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON Schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Files, Guidance]

**Output Format:** [JSON on stdout with logs on stderr and optional JSON files under logs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; commands must run from the skill root.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
