## Description:

Provides read-only searches of public Kuaishou videos, creator posts and follower data, and video comments as structured JSON for competitor and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing teams, and analysts use this skill to research public Kuaishou videos, benchmark creator accounts, review comment sentiment, and inform content and competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and account or video links are sent to the third-party service; some files were only partly inspected in the security scan.

Mitigation: Avoid sending sensitive terms or links, and review the skill's behavior before use.

## Reference(s):

- [Parameter reference](references/options.md)
- [Frequently asked questions](references/faq.md)
- [Guaikei service and API access](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Structured JSON containing video search results, creator posts and profile statistics, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN. Query limits depend on the service plan; plan-limit errors should be resolved by lowering the requested count or obtaining user consent before upgrading.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
