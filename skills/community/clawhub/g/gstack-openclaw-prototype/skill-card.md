## Description:

Builds disposable prototypes that help developers quickly validate either interaction logic and state models or several substantially different UI directions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilmych](https://clawhub.ai/user/ilmych)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer design questions quickly before committing to production work. It routes requests toward either an interactive terminal prototype for logic and state-machine exploration or multiple UI variants for visual comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad requests such as "prototype this" or "mock up a UI" may invoke a throwaway-code workflow when the user expects production-quality implementation.

Mitigation: Confirm whether the desired output is a disposable prototype or production-ready code before applying the skill to ambiguous requests.

Risk: Prototype code may be mistaken for maintainable production code if it remains in the repository after validation.

Mitigation: Delete the prototype, fold the validated decision into real code, or clearly mark the artifact for cleanup after the design question is answered.

## Reference(s):

- [gstack Prototype on ClawHub](https://clawhub.ai/ilmych/skills/gstack-openclaw-prototype)
- [Publisher profile: ilmych](https://clawhub.ai/user/ilmych)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with code, commands, and concise implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prototype outputs are intended to be temporary and should be deleted, absorbed into production code, or clearly marked for cleanup after validation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
