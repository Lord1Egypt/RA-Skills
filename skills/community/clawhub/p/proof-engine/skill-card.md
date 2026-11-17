## Description:

Transforms business results into structured proof records, financial dashboards, storytelling arcs, content briefs, opportunity reports, and deployable credibility assets across workspace skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business builders use Proof Engine to capture proof from revenue, agent, content, testimonial, media, and partnership workflows, then turn those records into dashboards, narratives, and content assets. It is intended for proof-driven marketing, operational reporting, and cross-skill deployment in a ClawHub/OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive business proof data, including financial, testimonial, revenue, brand, content, and memory-adjacent workspace files.

Mitigation: Install only in workspaces where this access is intended, and review the declared read paths before enabling capture or deployment commands.

Risk: Telegram notifications can externally share proof data when TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are configured.

Mitigation: Use a limited bot token and controlled chat, verify notification content, and avoid notification-triggering commands when proof data is sensitive.

Risk: Generated proof, stories, content, and dashboard updates may be incomplete, unverified, or misleading if source workspace data is stale or inaccurate.

Mitigation: Review generated proof records and content before using them in funnels, outreach, VSL scripts, or public marketing.

Risk: The security summary reports that the skill can write outside its declared skill area and warns against arbitrary output paths.

Mitigation: Restrict workspace write access where possible and avoid using output options with unreviewed or arbitrary paths.

## Reference(s):

- [Proof Engine ClawHub Skill Page](https://clawhub.ai/georges91560/skills/proof-engine)
- [Publisher Profile](https://clawhub.ai/user/georges91560)
- [Storytelling Reference](artifact/storytelling.md)
- [Telegram Bot API Endpoint](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [CLI text, Markdown story/content files, JSON proof/dashboard/opportunity records, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes proof vault, dashboard, story, opportunity, content, and audit files in the workspace; Telegram notifications may be sent when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0 and README reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
