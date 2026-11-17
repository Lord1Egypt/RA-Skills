## Description:

Meridian provides anti-FOMO AI intelligence for product leaders through landscape scans, entity tracking, and product discovery, producing timeline narratives with real source links instead of link dumps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheibjkb](https://clawhub.ai/user/cheibjkb)

### License/Terms of Use:

MIT-0

## Use Case:

Product leaders and strategy teams use Meridian to scan recent AI developments, track people or companies, and discover breakout products in a target ecosystem. It turns source-verified findings into concise timeline narratives, briefings, and product-decision takeaways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-based search examples may interpolate user-derived keywords into curl or Python snippets.

Mitigation: Run only in sandboxed or approval-gated environments, and prefer built-in web and API tools over copying shell snippets.

Risk: Reports are saved by default and may retain researched entities, queries, and gathered links locally.

Mitigation: Confirm output paths and retention expectations before allowing the skill to create files.

Risk: AI intelligence reports can become misleading if source links, publication dates, or time windows are not checked.

Mitigation: Keep only source-linked facts, enforce the requested date window, and downgrade unsupported findings instead of presenting them as storylines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cheibjkb/skills/meridian-intel)
- [Briefing Template](artifact/references/briefing-template.md)
- [Entity Report Template](artifact/references/entity-report-template.md)
- [Product Discovery Template](artifact/references/product-discovery-template.md)
- [Search Playbook](artifact/references/search-playbook.md)
- [Storyline Template](artifact/references/storyline-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance, Files]

**Output Format:** [Markdown intelligence reports and timeline narratives with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be written under intel/ paths when the agent is allowed to create files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
