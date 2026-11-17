## Description:

Launch Asset Packager helps agents assemble tier-scoped launch asset manifests, press kit specs, demo and screenshot specs, launch FAQ outlines, store listing metadata drafts, and technical go-live checklist manifests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, launch operators, and marketing teams use this skill to prepare launch-ready asset packages for declared product tiers, including press kit specs, store listing drafts, checklist manifests, owners, statuses, and handoff gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Launch plans, store listing exports, pricing or asset inventories, and analytics verification data may contain sensitive business context.

Mitigation: Share only the context needed for packaging, avoid unnecessary saved memory, and confirm before allowing manifest or registry proposal writes.

Risk: Pasted asset lists, store exports, and press-kit drafts may contain untrusted instructions or unsupported claims.

Mitigation: Treat submitted documents as data, trace claims to accepted source material, and mark unresolved wording as needing a source before launch-ready status.

Risk: The skill can draft launch manifests and proposals but does not execute store submission, technical SEO changes, or go-live actions.

Mitigation: Route execution to the responsible downstream skills or human owners and require explicit confirmation before any operational change.

## Reference(s):

- [Launch Asset Specs](artifact/references/asset-specs.md)
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/launch-asset-packager)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured tables, checklists, character counts, and handoff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose saved manifest records only with user permission; does not perform store submission or site go-live changes.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
