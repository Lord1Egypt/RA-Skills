## Description:

Local Mail Digest turns email batches into local structured summaries with priorities, project grouping, todos, deadlines, and optional HTML, Markdown, or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aks-666888](https://clawhub.ai/user/aks-666888)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent hosts use this skill to summarize local email exports, direct IMAP pulls, or pasted email text into actionable priorities, todos, deadlines, and downstream automation data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM endpoints may receive email-derived content, which can conflict with the skill's local-only privacy posture if the endpoint is remote.

Mitigation: Use the default rules-based local processing path or only connect a trusted local LLM endpoint.

Risk: Optional webhook delivery may send subjects, senders, projects, deadlines, or todo summaries to external services.

Mitigation: Enable webhook delivery only for trusted destinations and review what summary content will be sent.

Risk: Direct IMAP and SMTP modes require app-specific mail credentials.

Mitigation: Use provider-issued app passwords, store them outside the skill, and prefer host connector JSON input when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aks-666888/skills/local-mail-digest)
- [Server-resolved source repository](https://github.com/aks-666888/local-mail-digest)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples; generated agent artifacts may be HTML, Markdown, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can emit structured JSON containing totals, priority counts, sender, subject, date, priority, project, todos, deadlines, summary, and body excerpts.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
