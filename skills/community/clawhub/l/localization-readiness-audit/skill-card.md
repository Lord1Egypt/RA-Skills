## Description:

Audits a product surface for i18n and l10n readiness before vendor engagement or a new-locale launch, producing a draft findings report, launch verdict, and owner-tagged remediation plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, engineering leads, localization PMs, globalization managers, and DevRel teams use this skill to assess a single product surface before translation vendor engagement or new-locale launch planning. It guides structured intake and produces a draft localization-readiness audit across engineering, content, UI, process, and legal-review dimensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could treat the draft audit verdict as a final launch approval or legal compliance decision.

Mitigation: Keep product, engineering, globalization-lead, and licensed-counsel review in the release process before launch decisions.

Risk: Users may provide customer data, secrets, full unreleased strings, or other sensitive product information during intake.

Mitigation: Use non-sensitive evidence such as file paths, configuration keys, screenshots with sensitive text redacted, and architecture summaries.

Risk: Findings can be incomplete when the team supplies partial intake or unverified architecture details.

Mitigation: Confirm assumptions with named owners and validate high-impact findings against source files, pipeline settings, and runtime configuration before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/localization-readiness-audit)
- [Skill README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Draft Markdown audit with tables, checklists, severity-rated findings, verdict rationale, and remediation plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit guidance; does not modify code, commission translations, choose vendors, make launch decisions, or provide legal opinions.]

## Skill Version(s):

0.1.1 (source: server evidence release.version and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
