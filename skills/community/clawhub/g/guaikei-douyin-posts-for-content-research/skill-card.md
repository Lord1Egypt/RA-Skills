## Description:

Helps an agent gather public Douyin search results, creator posts, video comments, and real-time trending topics for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content researchers, marketers, and analysts use this skill to run Douyin content discovery workflows over public data, including keyword search, creator-post retrieval, comment extraction, and hot-list checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUAIKEI_API_TOKEN-backed requests send search terms, Douyin URLs or IDs, and limits to www.guaikei.com.

Mitigation: Use a dedicated, revocable token and avoid sensitive investigations on shared machines.

Risk: Fetched results are saved locally under logs/ and may contain research-sensitive public content metadata.

Mitigation: Clear logs after use and restrict access to workspaces where the skill runs.

Risk: Runtime authentication failures may show contact details that the security review did not treat as vetted support channels.

Mitigation: Do not rely on runtime contact details for trusted support; use vetted release or publisher channels instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-posts-for-content-research)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei token and help site](https://www.guaikei.com)
- [Usage documentation](readme.md)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON on stdout with logs and prompts on stderr; fetched results may also be saved as JSON files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; user-controlled limits can request up to 10000 public Douyin records per command.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, references/changelog.md, src/config/constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
