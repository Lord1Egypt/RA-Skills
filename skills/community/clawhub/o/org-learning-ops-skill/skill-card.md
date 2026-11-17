## Description:

Analyzes organization-wide multi-agent conversation history to produce daily learning briefs, skill radar summaries, and approval-ready Agent x Skill assignment recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangluckybao-lab](https://clawhub.ai/user/huangluckybao-lab)

### License/Terms of Use:


## Use Case:

Teams using multiple agents use this skill to turn visible agent conversation histories and installed-skill inventories into evidence-based organizational learning reports, external skill radar shortlists, and approval-ready assignment plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect organization-wide agent histories and configuration, which can expose raw prompts, tool outputs, secrets, personal data, or data outside the intended review scope.

Mitigation: Before use, restrict the permitted agents and date ranges, require approval for cross-agent access, redact secrets and personal data, and prevent raw prompts, tool outputs, or configuration values from appearing in reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangluckybao-lab/skills/org-learning-ops-skill)
- [README](artifact/README.md)
- [Daily brief example](artifact/examples/daily-brief-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown daily brief with coverage reports, skill radar entries, approval queues, and Agent x Skill assignment tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are evidence-gated and include risks, approval status, and rollback points where applicable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
