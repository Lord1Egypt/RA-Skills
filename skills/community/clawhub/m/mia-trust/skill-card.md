## Description:

MIA-Trust is a Memory-Intelligent Assistant pipeline that gates user questions, reviews generated plans, and stores memory and trust experience for future agent runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sii-yucheng2002](https://clawhub.ai/user/sii-yucheng2002)

### License/Terms of Use:

ISC

## Use Case:

Developers and agent operators use this skill to run a question-safety gate, generate or review execution plans, and persist reusable memory, feedback, and trust-review experience for OpenClaw-style assistants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use can expose prompt and model text to shell command execution.

Mitigation: Run the skill only in an isolated, low-privilege environment and review shell-command construction before deployment.

Risk: The skill broadly persists user questions, plans, model outputs, feedback, and trust experience.

Mitigation: Do not process secrets or confidential prompts until persistent-memory behavior is reviewed and appropriate retention controls are in place.

Risk: The skill calls configurable local or HTTPS model endpoints for planning and trust review.

Mitigation: Use trusted local endpoints or allowlisted HTTPS endpoints and keep API credentials out of prompts and stored memories.

## Reference(s):

- [MIA-Trust pipeline guide](PIPELINE.md)
- [ClawHub skill page](https://clawhub.ai/sii-yucheng2002/skills/mia-trust)
- [Publisher profile](https://clawhub.ai/user/sii-yucheng2002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON and Markdown/text with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plan-review results, final plans, memory records, feedback records, and trust-audit summaries.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
