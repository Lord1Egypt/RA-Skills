## Description:

Helps users discover local LLMs by hardware and use case, then sends them to localllm.run for final compatibility checks and model comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julianmatos97](https://clawhub.ai/user/julianmatos97)

### License/Terms of Use:


## Use Case:

External users, developers, and engineers use this skill to choose candidate local LLMs based on hardware, use case, and priorities, then validate final model fit with localllm.run before downloading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly routes users to a third-party compatibility website that may receive hardware details or perform hardware detection.

Mitigation: Review localllm.run's privacy practices before allowing hardware detection or entering system specifications.

Risk: Model recommendations may be incorrect if hardware details are missing or final compatibility is not checked.

Mitigation: Treat recommendations as provisional and complete the final compatibility check on localllm.run before downloading or deploying a model.

## Reference(s):

- [localllm.run compatibility checker](https://www.localllm.run/)
- [ClawHub skill page](https://clawhub.ai/julianmatos97/skills/localllm-discovery-guide)
- [Publisher profile](https://clawhub.ai/user/julianmatos97)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with model shortlists, pros and cons, testing tips, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are provisional until the user completes the final compatibility check on localllm.run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
