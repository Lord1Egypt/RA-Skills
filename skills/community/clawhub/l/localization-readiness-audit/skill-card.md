## Description: <br>
Use this skill when a product manager, engineering lead, or localization PM needs to audit a product surface for i18n / l10n readiness before engaging a translation vendor or committing to a new-locale launch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, engineering leads, localization PMs, globalization managers, and DevRel teams use this skill to collect launch context and produce a draft localization readiness audit before vendor engagement or new-locale launch commitments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary marks the release suspicious because a review helper may run nested Codex with full local access. <br>
Mitigation: Install only for intended ClawHub maintainer and Convex development workflows, review the skill before use, and avoid full local access unless it is required. <br>
Risk: Fallback review tools or broad credentials could expose private diffs or enable unintended publishing or moderation actions. <br>
Mitigation: Use scoped ClawHub and GitHub credentials, confirm publishing or moderation targets carefully, and avoid sending private diffs to fallback tools unless acceptable for the project. <br>
Risk: The audit is advisory and could be mistaken for a launch decision or legal compliance conclusion. <br>
Mitigation: Keep the DRAFT review label, require product, engineering, and globalization-lead review, and route market-specific legal and regulatory questions to counsel. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/archlab-space/localization-readiness-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown draft audit with intake summary, severity-rated findings, verdict, remediation plan, and per-locale checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit output is labeled DRAFT and requires product, engineering, globalization lead, and market-specific legal review where applicable.] <br>

## Skill Version(s): <br>
0.1.1 (source: server evidence and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
