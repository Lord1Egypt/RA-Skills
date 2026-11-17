## Description:

Granola archive: search, sync freshness, notes, transcripts, panels, SQL counts, and Graincrawl repo work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw](https://clawhub.ai/user/openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users with local Granola archives use this skill to search notes, transcripts, and panels, check archive freshness, refresh stale data when requested, and report exact date spans, source gaps, and availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local Granola notes and transcripts and sync from desktop-cache or private-api sources, which may expose sensitive meeting content.

Mitigation: Install only when comfortable with that local data access, use bounded reads, and report focused summaries such as date spans, titles, source gaps, and availability.

Risk: The install metadata uses a mutable external Go module version, so the installed graincrawl binary can change between installs.

Mitigation: Prefer a pinned, reviewed graincrawl version before deployment.

Risk: Encrypted-source debugging may require Keychain or secrets access.

Mitigation: Run explicit unlock and secrets checks only when intentionally requested, and avoid surprise Keychain prompts.

## Reference(s):

- [Graincrawl project homepage](https://github.com/openclaw/graincrawl)
- [ClawHub Graincrawl skill page](https://clawhub.ai/openclaw/skills/graincrawl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON command output summaries, exact date spans, note titles, source gaps, and transcript or panel availability.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
