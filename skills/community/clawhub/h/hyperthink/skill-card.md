## Description:

Triple-perspective deep research engine triggered by /hyperthink that narrows scope with an interrogate flow, runs a fully automatic multi-stage pipeline, and produces a synthesized research report plus an executive brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inxan3](https://clawhub.ai/user/inxan3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced agent users use Hyperthink to run long-form deep research with Optimist, Analyst, and Critic perspectives after one scope-confirmation step. It is suited to broad strategy, product, technical, investment, or evaluation questions where a synthesized markdown report and executive brief are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pipeline runs unattended for many hours after the initial scope confirmation.

Mitigation: Use it only for topics where a single approval is acceptable, or add approval checkpoints before submitting later stages.

Risk: Prompts and generated content are sent to Anthropic during batch stages.

Mitigation: Use non-sensitive topics unless privacy controls and data-handling review are in place.

Risk: The skill writes persistent output and job state under /data/hyperthink and batch-jobs.

Mitigation: Restrict filesystem permissions, monitor stored outputs, and clean up artifacts that should not persist.

Risk: Optional webhook or Telegram notifications can send completion data to external destinations.

Mitigation: Enable notification environment variables only after explicit approval, and use least-privilege tokens or endpoints.

Risk: Supporting helper scripts must be implemented or generated before operation.

Mitigation: Review helper scripts before execution and pin dependencies such as python-docx where DOCX export is used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/inxan3/skills/hyperthink)
- [Publisher Profile](https://clawhub.ai/user/inxan3)
- [Batch Worker Implementation Spec](artifact/scripts/batch-worker-spec.md)
- [Markdown to DOCX Implementation Spec](artifact/scripts/md2docx-spec.md)
- [Analyst Persona](artifact/agents/analyst.md)
- [Critic Persona](artifact/agents/critic.md)
- [Optimist Persona](artifact/agents/optimist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown reports and briefs, JSON job and state files, shell commands, configuration guidance, and optional DOCX documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long-running multi-stage output; final brief can be exported to DOCX when python-docx is available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
