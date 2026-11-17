## Description:

Teaches AI agents how to learn better by enforcing deep correction, transfer learning, and proactive pattern recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fahrulalwan](https://clawhub.ai/user/fahrulalwan)

### License/Terms of Use:


## Use Case:

Developers and AI-agent operators use Metaskill to turn errors, complex-task preparation, and successful outcomes into reusable learning notes. It supports deeper correction, analogy checks against prior learnings, and lightweight evaluation of the learning process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions, error text, and excerpts of saved learning notes may be sent to configured LLM providers, including a fallback remote provider when the selected provider fails.

Mitigation: Review provider configuration before use, prefer a local provider such as Ollama for confidential work, and redact sensitive task or learning content before running LLM-backed commands.

Risk: Learning logs and evaluation reports are persistent workspace records that may retain sensitive operational details.

Mitigation: Periodically review, redact, or delete .learnings and memory report files according to the workspace data-retention policy.

Risk: The skill writes learning and evaluation files into the detected workspace or a fallback OpenClaw workspace path.

Mitigation: Confirm the workspace path before running scripts and inspect generated files before sharing or committing them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text and Markdown learning records, with YAML configuration and inline shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use configured LLM providers for extraction and transfer checks, or fall back to manual and heuristic modes when providers are unavailable.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
