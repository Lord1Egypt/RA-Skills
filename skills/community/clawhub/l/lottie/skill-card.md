## Description:

Lottie and dotLottie adapter patterns for HyperFrames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-kay8](https://clawhub.ai/user/lucas-kay8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to embed lottie-web JSON and dotLottie animations in HyperFrames projects, register players for runtime seeking, and validate deterministic animation behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples load third-party player scripts and run package validation commands in a project environment.

Mitigation: Pin exact package versions, prefer local or locked dependencies, add integrity checks for CDN scripts where possible, and run npx validation commands in a normal least-privileged project environment.

Risk: Remote animation paths or late player registration can make HyperFrames validation or rendering nondeterministic.

Mitigation: Load animation assets from local project files, register players on window.__hfLottie before validation, and run HyperFrames lint and validation commands after edits.

Risk: Unsupported After Effects effects may not survive Lottie export.

Mitigation: Test each JSON or .lottie asset in a browser before using it in HyperFrames.

## Reference(s):

- [ClawHub Lottie skill page](https://clawhub.ai/lucas-kay8/skills/lottie)
- [lottie-web](https://github.com/airbnb/lottie-web)
- [lottie-web loadAnimation options](https://github.com/airbnb/lottie-web/wiki/loadAnimation-options)
- [dotLottie web player methods](https://developers.lottiefiles.com/docs/dotlottie-player/dotlottie-web/methods)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML, CSS, JavaScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes adapter patterns, runtime registration guidance, and validation commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
