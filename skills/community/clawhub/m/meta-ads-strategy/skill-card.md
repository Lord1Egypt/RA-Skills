## Description:

Guides users through planning, creating, launching, and optimizing Facebook and Instagram ads, including strategy, creative, copy, campaign structure, targeting, budgeting, ROAS tracking, Pixel setup, and an ad brief workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeannen](https://clawhub.ai/user/jeannen)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, founders, and marketers use this skill to decide whether Meta ads fit their product, prepare campaign inputs, write ad copy, plan creative, configure account and Pixel setup, launch campaigns, and diagnose ad performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead to live ad-account actions, including campaign creation, budgets, publishing decisions, and AdKit command suggestions.

Mitigation: Use it for planning unless a human is prepared to review and approve each command, campaign, budget, and publishing action before execution.

Risk: Tracking and audience workflows may involve pixels, email lists, retargeting audiences, or session-recording tools that process privacy-sensitive advertising data.

Mitigation: Add privacy, consent, data-use, and platform-policy checks before using tracking, retargeting, uploaded audiences, or session-recording tools.

Risk: Account restriction guidance includes advice around spare ad accounts and VPN use that was flagged for review.

Mitigation: Ignore or revise that guidance and follow Meta policies, payment rules, and local legal or compliance requirements.

## Reference(s):

- [AdKit](https://adkit.so)
- [When Should a SaaS Run Ads?](https://adkit.so/resources/when-to-run-ads-for-saas)
- [AdKit Ad Library](https://adkit.so/features/ad-library?utm_source=skill)
- [Safe Zones Checker Tool](https://adkit.so/tools/safe-zones/meta?utm_source=skill)
- [Lead Magnets Skill](https://github.com/coreyhaines31/marketingskills/blob/main/skills/lead-magnets/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/jeannen/skills/meta-ads-strategy)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, decision tables, ad brief content, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update an ad brief file and may suggest AdKit CLI commands when AdKit is installed.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
