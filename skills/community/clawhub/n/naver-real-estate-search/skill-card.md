## Description:

Search, compare, and monitor Korean property listings from Naver Real Estate using natural-language queries, candidate-complex workflows, briefings, and watch alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twbeatles](https://clawhub.ai/user/twbeatles)

### License/Terms of Use:

MIT-0

## Use Case:

External users, real-estate researchers, and agent developers use this skill to turn Korean natural-language property questions into Naver Real Estate searches, candidate-complex lists, comparison briefings, JSON summaries, and local watch alerts.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: The skill queries Naver and may encounter rate limits or incomplete responses during broad searches.

Mitigation: Prefer direct complex URLs or IDs when available, narrow ambiguous requests to one to three candidate complexes, and avoid repeated broad scans.

Risk: Local candidate-cache and watch-rule JSON files can reveal property interests on shared machines.

Mitigation: Clear local cache and watch files after use on shared systems and avoid storing sensitive watch rules longer than needed.

Risk: Generated candidate seeds can misidentify similar apartment complexes or aliases.

Mitigation: Use preview modes first and manually verify complex ID, name, and address before applying generated seeds to operational files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twbeatles/skills/naver-real-estate-search)
- [README](README.md)
- [Design Notes](references/design.md)
- [Candidate Seed Builder](references/candidate-seed-builder.md)
- [Candidate Seeds](references/candidate-seeds.json)
- [Seoul Major Complex Seed Input](references/seoul-major-complexes.seed-input.json)
- [Generated Candidate Seeds](references/candidate-seeds.generated.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Korean text or JSON, with Markdown-friendly briefings and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local candidate-cache, candidate-seed, and watch-rule JSON files when apply or watch commands are used.]

## Skill Version(s):

2026.4.16 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
