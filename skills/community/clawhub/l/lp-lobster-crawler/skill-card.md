## Description:

Lobster Crawler Skill helps agents run targeted Webnovel and ReelShorts crawls, classify collected content, generate feeds, and send DingTalk summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[7487](https://clawhub.ai/user/7487)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect structured novel and short-drama metadata from configured target sites, maintain local crawl state, schedule updates, publish RSS or Atom feeds, and broadcast prioritized summaries to DingTalk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler contacts Webnovel/ReelShorts and can send collected summaries to a DingTalk webhook.

Mitigation: Run it only in an environment authorized for those outbound requests, and configure DINGTALK_WEBHOOK only for intended broadcast destinations.

Risk: The package includes an agent automation loop that can persist state outside the project and let repository files steer Claude execution.

Mitigation: Do not run scripts/claude_loop.sh in a normal agent environment unless that behavior is intentionally reviewed; remove or ignore global memory instructions first.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/7487/skills/lp-lobster-crawler)
- [Publisher Profile](https://clawhub.ai/user/7487)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Webnovel](https://www.webnovel.com)
- [ReelShort](https://www.reelshort.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; executed commands may produce SQLite data, RSS or Atom XML, logs, and DingTalk Markdown messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the uv binary and DINGTALK_WEBHOOK for DingTalk broadcast workflows.]

## Skill Version(s):

0.7.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
