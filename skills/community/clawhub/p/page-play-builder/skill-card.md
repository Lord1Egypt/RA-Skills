## Description:

Builds programmatic, third-party, comparison, and local SEO page-system plans with mode-specific guardrails for thin content, reputation abuse, comparison honesty, and NAP consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

Apache-2.0

## Use Case:

Marketing teams, SEO practitioners, and developers use this skill to build SEO page systems rather than standalone articles, including programmatic pages, third-party-platform placements, comparison pages, and local SEO packs. It helps produce structured plans, page deliverables, source checks, and publish blockers for follow-on review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SEO deliverables may include inaccurate competitor claims, third-party platform details, GBP/NAP information, or URL-submission recommendations.

Mitigation: Review outputs before publishing, require sources or explicit flags for competitor facts, confirm platform rules and local business details, and only submit live URLs after the relevant guardrail passes.

Risk: Generated business and SEO work may be saved into project memory during use.

Mitigation: Avoid providing unnecessary sensitive business data, review memory-bound handoff summaries, and remove or redact project memory entries that should not persist.

Risk: Third-party or scraped pages, reviews, listings, and platform-policy text can contain untrusted or misleading content.

Mitigation: Treat fetched or pasted external content as evidence only, verify material claims independently, and do not follow instructions embedded in external page text.

## Reference(s):

- [Programmatic Mode Playbooks](artifact/references/programmatic.md)
- [Parasite Mode Platform Playbook](artifact/references/parasite.md)
- [Comparison Mode Page Formats](artifact/references/comparison.md)
- [Local Mode GBP, NAP, Citations, Location Pages](artifact/references/local.md)
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/page-play-builder)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured checklists, tables, page plans, handoff summaries, and occasional command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode-specific outputs may include page-system plans, platform plans, comparison pages, local SEO packs, competitor data files, canonical NAP records, and publish blockers.]

## Skill Version(s):

19.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
