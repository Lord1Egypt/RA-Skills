## Description: <br>
Generate publication-quality academic diagrams, methodology figures, architecture illustrations, and statistical plots from text descriptions using the PaperBanana multi-agent AI pipeline, and evaluate diagram quality against reference images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GoatInAHat](https://clawhub.ai/user/GoatInAHat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and technical authors use this skill to turn methodology text, architecture descriptions, and CSV/JSON data into publication-ready diagrams, plots, and figure evaluations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts, captions, feedback, images, and CSV/JSON data may be sent to configured third-party AI providers. <br>
Mitigation: Avoid sensitive, confidential, unpublished, or proprietary inputs unless organizational policy permits that provider use; use limited API keys. <br>
Risk: The plotting workflow may run AI-generated Python plotting code without clear sandboxing. <br>
Mitigation: Run the skill in a constrained environment and review generated plots, code, and files before relying on them. <br>


## Reference(s): <br>
- [Provider Reference](references/providers.md) <br>
- [Skill homepage](https://github.com/GoatInAHat/openclaw-paperbanana) <br>
- [PaperBanana PyPI package](https://pypi.org/project/paperbanana/) <br>
- [PaperBanana project](https://github.com/llmsresearch/paperbanana) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Code, Shell commands, Configuration] <br>
**Output Format:** [PNG, JPEG, or WebP image files; Matplotlib-generated plots; text evaluation scores; and shell-command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Python 3.10 or later, and at least one configured provider API key.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
