## Description:

MiroFish runs 55 AI agents in simulated social-platform interactions to explore forecasts, simulations, and what-if scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iml1s](https://clawhub.ai/user/iml1s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to launch MiroFish simulations for trend forecasting and what-if analysis, then query generated reports or simulated agent perspectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable external code through the MiroFish npm package and uses a Docker-backed backend.

Mitigation: Use pinned or reviewed CLI and container versions, and install only from trusted package and image sources.

Risk: The skill requires an LLM_API_KEY and can interact with paid model services.

Mitigation: Configure the API key deliberately, use least-privilege credentials where possible, and avoid running the skill with sensitive files or production secrets.

Risk: Broad triggers and multi-agent simulations can create unexpected token spend.

Mitigation: Start with a small round count, monitor token usage and costs, and run simulations only for intentional forecasting tasks.

Risk: Starting the backend can pull and run Docker components on the local system.

Mitigation: Start the backend only for intentional simulations, review the runtime environment first, and stop the backend after use.

## Reference(s):

- [MiroFish Predict on ClawHub](https://clawhub.ai/iml1s/skills/mirofish-predict)
- [MiroFish project homepage](https://github.com/666ghj/MiroFish)
- [Publisher profile](https://clawhub.ai/user/iml1s)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and CLI-generated report references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Docker, the mirofish CLI, and an LLM_API_KEY; simulations can consume substantial LLM tokens.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
