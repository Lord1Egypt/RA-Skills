## Description:

LLM Wiki Karpathy helps agents inspect, repair, and grow a local Markdown wiki by ingesting raw material, maintaining source and derived pages, answering from the wiki, and running lint checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge-base maintainers use this skill to operate a local Markdown wiki: ingest raw notes and assets, answer from retrieved notes, file useful answers back, maintain page structure, and map missing concept/entity/synthesis pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented setup can execute an unpinned remote npm runtime with access to the selected vault.

Mitigation: Use a pinned, reviewed runtime version instead of @latest and avoid npx -y where confirmation is practical.

Risk: Write-capable wiki workflows can read and modify the selected vault.

Mitigation: Use a dedicated vault path and invoke write-capable tasks with the explicit $llm-wiki-karpathy prefix, clear scope limits, or dry-run wording.

Risk: Generated wiki pages may contain weak grounding, stale references, unsupported claims, or contradiction candidates.

Mitigation: Run kb_lint, read supporting notes before writing, keep source_refs aligned with real source notes, and rebuild indexes after changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/llm-wiki-karpathy)
- [Maintenance Playbook](references/maintenance-playbook.md)
- [Repository Layout](references/repo-layout.md)
- [Andrej Karpathy profile](https://x.com/karpathy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with structured wiki-page content, command snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses runtime-issued paths, IDs, hashes, and source references when writing or updating vault content.]

## Skill Version(s):

1.2.3 (source: server release, clawhub.json, CHANGELOG, RELEASE.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
