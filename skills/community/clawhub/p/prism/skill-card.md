## Description:

PRISM is a multi-agent review protocol that uses independent specialist reviewers, prior-review memory, and evidence requirements to support architecture, security-sensitive, refactor, release, and long-lived engineering decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremyknows](https://clawhub.ai/user/jeremyknows)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use PRISM to run structured adversarial reviews for architecture decisions, security-sensitive changes, large refactors, open source releases, and decisions expected to last six months or more.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review history can contain sensitive or untrusted text that is reused in later reviewer prompts.

Mitigation: Protect analysis/prism/archive/ from untrusted edits, clean or disable the archive for sensitive work, and treat prior review text as context rather than authority.

Risk: The skill may run a local sub-agent completion script during review archival.

Mitigation: Verify ~/.openclaw/scripts/sub-agent-complete.sh before allowing the skill to execute it.

Risk: Review archives can grow and persist longer than intended because retention is not enforced by the skill.

Mitigation: Apply the documented archive retention policy manually until automated retention exists.

## Reference(s):

- [PRISM Evidence Rules](references/evidence-rules.md)
- [PRISM Orchestration Reference](references/orchestration.md)
- [PRISM Archive Retention Policy](references/archive-retention-policy.md)
- [Example PRISM v2 Review](references/example-review.md)
- [qmd search tool](https://github.com/tobilu/qmd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review synthesis with specialist findings, citations, verdicts, and actionable fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May archive review syntheses under analysis/prism/archive/<slug>/ and reuse protected prior review summaries as context.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
