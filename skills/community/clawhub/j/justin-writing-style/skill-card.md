## Description:

Generates Chinese cold-narrative prose in the justin-writing-style pattern, using restrained language, concrete numbers, object details, unquoted dialogue, and anticlimactic endings while requiring fictionalized or anonymized subjects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and agents use this skill to draft Chinese personal essays and social narratives in a restrained, fact-forward style with self-checks for restraint, concreteness, rhythm, structure, and deadpan tone. It is intended for fictionalized or anonymized material, not identifiable real people, institutions, or events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may route general writing requests to this style generator.

Mitigation: Review and tune trigger phrases before deployment, especially in agents that frequently handle general writing requests.

Risk: A hidden memory note in the artifact could be imported as global memory by overly broad installers.

Mitigation: Install only the intended skill files and exclude hidden workspace memory notes from global memory import.

Risk: Generated narratives about identifiable real people, institutions, or events can create privacy or defamation risk.

Mitigation: Replace real names and identifiable details with fictional names before generation, and refuse requests where the user insists on identifiable real subjects.

Risk: The style fingerprint is based on a single source text and may overfit or underperform outside first-person viral essays.

Mitigation: Treat outputs for third-person, advertising, speech, or ordinary low-tension topics as lower confidence and validate them against the included evaluation prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qomob/skills/justin-writing-style)
- [Publisher profile](https://clawhub.ai/user/qomob)
- [README](README.md)
- [Honest Boundaries](honest-boundaries.md)
- [Style Reference](references/style.md)
- [Principles Reference](references/principles.md)
- [Runtime Reference](references/runtime.md)
- [Output Template](templates/output.md)
- [Evaluation README](evals/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text Chinese prose, with optional critique and revision guidance when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output omits prefaces and style explanations unless requested; real names and identifiable real-world entities must be replaced with fictional names or rejected when the user insists.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
