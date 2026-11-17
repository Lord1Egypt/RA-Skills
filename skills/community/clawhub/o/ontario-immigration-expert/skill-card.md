## Description:

Ontario immigration policy assistant for OINP Ontario Workforce Priority and Sudbury RCIP/FCIP that checks official sources, surfaces policy updates, and computes itemized EOI scoring with eligibility gates for candidate profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forrest-tech](https://clawhub.ai/user/forrest-tech)

### License/Terms of Use:

MIT

## Use Case:

External users and advisors use this skill to assess Ontario immigration pathways, compute OINP EOI scoring from candidate JSON, and monitor official OINP and Sudbury RCIP/FCIP sources for policy changes. It is a reference aid and does not replace official immigration decisions or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Immigration scoring or policy guidance can be outdated or misleading if official pages changed, live fetches fail, or the skill overstates live policy coverage.

Mitigation: Treat output as a snapshot-based reference aid, independently verify current official OINP/RCIP/FCIP pages, and defer to official provincial decisions or qualified legal advice.

Risk: The daily policy monitor can create persistent background checks through cron.

Mitigation: Enable scheduled monitoring only after reviewing the exact schedule and command, confirming persistent checks are desired, and knowing how to disable or remove the cron entry.

Risk: Installing from a mutable default branch can change reviewed behavior after installation.

Mitigation: Prefer installing a pinned, reviewed release and re-check security evidence before upgrading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forrest-tech/skills/ontario-immigration-expert)
- [Ontario Workforce Priority Stream](https://www.ontario.ca/page/ontario-workforce-priority-stream)
- [2026 Ontario Immigrant Nominee Program updates](https://www.ontario.ca/page/2026-ontario-immigrant-nominee-program-updates)
- [O. Reg. 422/17](https://www.ontario.ca/laws/regulation/170422)
- [Sudbury RCIP/FCIP](https://investsudbury.ca/why-sudbury/newcomers/rcipfcip/)
- [Official source manifest](data/sources.json)
- [OINP Workforce Priority official snapshot](data/snapshots/oinp-workforce-priority-OFFICIAL.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with scoring tables, JSON-driven shell command examples, and plain-text monitor status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes candidate background JSON via stdin for local scoring; policy monitoring may create snapshot hashes when enabled.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
