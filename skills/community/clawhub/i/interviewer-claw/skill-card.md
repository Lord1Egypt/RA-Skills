## Description:

Conducts structured Socratic interviews to stress-test plans, designs, or ideas until ambiguities, decisions, risks, and open branches are captured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris-graffagnino](https://clawhub.ai/user/chris-graffagnino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, planners, and external users use this skill to pressure-test software or non-software plans through a phased interview, then synthesize decisions, open items, and risks. For software projects, it can produce spec-kit-compatible markdown artifacts after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask the agent to inspect plans, documents, or project artifacts as part of an extended interview.

Mitigation: Use it only with documents intended for review and avoid providing sensitive material that should not be analyzed in the session.

Risk: For software projects, the skill can prepare spec-kit files that may affect project direction if accepted without review.

Mitigation: Review generated artifacts and confirm proposed file writes before allowing the agent to create or update project files.

## Reference(s):

- [Questioning Techniques Reference](artifact/references/techniques.md)
- [Spec-Kit Output Reference](artifact/references/speckit.md)
- [GitHub Spec Kit](https://github.com/github/spec-kit)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown questions, structured summaries, and optional spec-kit artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks one question at a time and requires confirmation before writing generated spec-kit files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
