## Description:

Learns a tenant user's writing style from connected outbound-message channels and produces per-channel style prompts for drafting outreach in that user's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milstan](https://clawhub.ai/user/milstan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and outreach teams use this agent skill to learn channel-specific writing patterns from their own outbound messages, then save reusable style prompts for future email, social, chat, and messaging drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect and persist private outbound messages from connected communication channels.

Mitigation: Install only after confirming style-learning consent and ensuring raw-message retention is removed or tightly controlled.

Risk: Outbound samples may contain customer data, business-sensitive content, personal conversations, secrets, or regulated information.

Mitigation: Review connected sources and exclude sensitive channels or data categories before running style learning.

Risk: LinkedIn browser scraping is listed as a possible collection path.

Mitigation: Disable LinkedIn browser scraping or separately confirm that it is permitted and properly controlled before use.

Risk: Learned style files must remain tenant-scoped to avoid cross-tenant leakage.

Mitigation: Use the resolver-mandated tenant path for style files and verify generated files stay under the intended tenant scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/milstan/skills/outclaw-style)
- [OpenClaw homepage](https://github.com/leadbay/outclaw)
- [Prompt Learning Protocol](https://gist.github.com/milstan/3b12f938f344f4ae1f511dd19e56adce)
- [Style Learning Reference](references/style-learning.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown style prompt files with YAML frontmatter and concise training reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-channel sample counts, best scores, discovered dimensions, conformity logs, and references to raw sample files.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata; artifact frontmatter reports 2.1.33)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
