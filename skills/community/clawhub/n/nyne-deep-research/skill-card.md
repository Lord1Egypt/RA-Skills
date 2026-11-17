## Description:

Research any person using the Nyne Deep Research API by submitting an email, phone, social URL, or name and receiving a comprehensive intelligence dossier with psychographic profile, social graph, career analysis, conversation starters, and approach strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfanous2](https://clawhub.ai/user/michaelfanous2)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to submit authorized person-research requests to the Nyne Deep Research API, poll for completion, and present the returned dossier sections clearly. It supports workflows that need contact enrichment, career context, social graph analysis, psychographic insights, conversation starters, and approach strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Person identifiers and returned dossiers can be used for covert profiling, harassment, discrimination, or sensitive decisions.

Mitigation: Use the skill only for legitimate, authorized research; avoid sensitive decisions and document the purpose, authorization basis, and allowed recipients before submitting identifiers.

Risk: Nyne API credentials may be exposed through shell history, logs, or diagnostic output.

Mitigation: Use temporary or scoped credentials where possible, store secrets outside version control, and avoid printing key or secret fragments.

Risk: Full dossier responses may contain sensitive personal data and can be retained in predictable files or sent to uncontrolled webhook destinations.

Mitigation: Write results only to controlled locations with limited access, delete temporary response files when no longer needed, and use callback URLs only when the destination is trusted and monitored.

## Reference(s):

- [Nyne API](https://api.nyne.ai)
- [Nyne Deep Research endpoint](https://api.nyne.ai/person/deep-research)
- [ClawHub skill page](https://clawhub.ai/michaelfanous2/skills/nyne-deep-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands, JSON examples, and structured dossier guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous API workflow with polling; outputs may include sensitive personal dossier data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
