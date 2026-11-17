## Description:

Audits one launch at one lifecycle read, selecting preflight readiness, launch-window execution, or post-lag outcome review without mixing those time horizons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, product, and launch teams use this skill to evaluate launch readiness, launch-window execution evidence, or post-launch outcomes before making follow-up decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch launch-related web evidence, so unsuitable or unexpected sources could affect the audit.

Mitigation: Review proposed WebFetch targets before use and rely on dated, profile-relevant evidence.

Risk: Audit conclusions could be mistaken for authorization to launch or mutate launch records.

Mitigation: Keep this skill to evidence review only; use separate approval and execution processes for launch actions or registry changes.

Risk: Persisted audit artifacts may capture sensitive launch evidence.

Mitigation: Allow persistence only after explicit permission and review the intended audit path and content before writing.

## Reference(s):

- [Standalone Auditor Runtime](artifact/references/auditor-runtime.md)
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/launch-readiness-auditor)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit report with structured status, verdict, score state, findings, Unknowns, and optional permissioned audit artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch dated launch evidence and may write a launch audit artifact only after explicit permission.]

## Skill Version(s):

19.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
