## Description:

Nano Triple generates three parallel image options from one prompt using Nano Banana Pro so the user can choose a winner or request another set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvanhorn](https://clawhub.ai/user/mvanhorn)

### License/Terms of Use:

MIT

## Use Case:

External users and creative teams use this skill to compare three generated image candidates from the same prompt, then select one or refine the prompt for another three-option round.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command template can run unintended commands if untrusted prompt text is pasted into shell-interpolated command strings.

Mitigation: Pass prompts as literal arguments or through a parameter file, and quote or escape user text before command execution.

Risk: The workflow calls an external Gemini image API and writes three files per image request.

Mitigation: Require a configured GEMINI_API_KEY, disclose external API use, and review generated files before sharing or using them.

## Reference(s):

- [Nano Triple on ClawHub](https://clawhub.ai/mvanhorn/skills/nano-triple)
- [Google AI Studio](https://aistudio.google.com)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration, files]

**Output Format:** [Markdown guidance with bash command examples and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates three labeled image options per request and uses GEMINI_API_KEY from the environment or OpenClaw configuration.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
