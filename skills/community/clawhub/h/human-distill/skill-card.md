## Description:

Human Distill helps an agent turn public creator, KOL, expert, or founder material from web search, fetched pages, optional Douyin browser extraction, and optional local deep research into an evidence-graded persona dossier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to assemble public information about a person and a topic into a structured markdown profile with confirmed, inferred, and conflicting claims clearly labeled. It is aimed at repeatable creator research, knowledge management, and source-aware persona analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed-in browser reuse can expose personal account state or shared profile data during Douyin collection.

Mitigation: Use only your own or explicitly authorized Douyin account, prefer a dedicated browser profile, and confirm login state before collection.

Risk: Loosening browser network policy for collection can broaden navigation beyond the intended target domains.

Mitigation: Keep browser allowlists narrowly scoped to required Douyin domains and do not add arbitrary target domains.

Risk: Optional local-deep-research tooling is an additional local dependency that may be unpinned or unreviewed.

Mitigation: Pin or review the optional local-deep-research dependency before enabling deep mode.

Risk: Creator research may mix direct evidence with search snippets, captions, and inferred claims.

Mitigation: Preserve the skill's confirmed, inferred, and conflict labels in final markdown and review sensitive conclusions before reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spikesubingrui-design/skills/human-distill)
- [Publisher Profile](https://clawhub.ai/user/spikesubingrui-design)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Search Query Templates](artifact/references/search-queries.md)
- [Sample Persona Excerpt](artifact/examples/sample-persona-excerpt.md)
- [Launch Notes](artifact/docs/LAUNCH.md)
- [OpenClaw](https://openclaw.ai)
- [Cursor](https://cursor.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with evidence labels, source tables, transcript excerpts, and structured persona sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are typically written under memory/ and may include a people/[slug] knowledge entry when the host environment supports it.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
