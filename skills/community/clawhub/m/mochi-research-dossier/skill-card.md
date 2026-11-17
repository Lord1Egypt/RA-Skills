## Description:

Connect research claims to supplied sources, verify quoted text, and flag unverified claims and duplicate URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Researchers and analysts use this skill to map claims to supplied sources, check whether quoted passages occur in provided text, and create a cited dossier with unverified claims and duplicate URLs flagged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports retain claim text, source URLs, and metadata locally.

Mitigation: Remove report exports and .mochilab/research-dossier/ when they are no longer needed.

Risk: A quote match confirms only that the text appears in supplied source material; it does not establish that a claim is true.

Mitigation: Review claims against their sources and keep uncertainty distinct from verified text matches.

Risk: Workspace path checks do not provide system-level isolation.

Mitigation: Keep the host sandbox enabled while processing selected research files.

## Reference(s):

- [Action contract](references/input.md)
- [Research Evidence Dossier on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-research-dossier)
- [MochiLab](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Markdown, JSON, HTML]

**Output Format:** [Markdown dossier with JSON and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source hashes, claim coverage, duplicate-source and distinct-domain counts; quote checks confirm text presence only.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
