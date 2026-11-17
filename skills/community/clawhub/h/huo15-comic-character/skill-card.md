## Description:

Generates three Seedream 4.0 character reference images from a script's characters field: a full-body pose, a half-body close-up, and a chibi-style portrait for each character.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative production teams use this skill to create consistent character reference cards from structured character descriptions before generating comic or storyboard scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Character descriptions and prompts are sent to Volcengine Ark using ARK_API_KEY.

Mitigation: Use only approved input data, keep ARK_API_KEY scoped and secret, and run the skill only in environments where this network transfer is acceptable.

Risk: Security evidence flags unsafe path handling and under-disclosed file and network behavior.

Mitigation: Review or patch path handling before using untrusted script.json files, constrain output directories, and limit network access in sensitive environments.

## Reference(s):

- [Volcengine Seedance documentation](https://www.volcengine.com/docs/82379/1520757)
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/97465)
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-comic-character)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated artifacts are PNG files and a JSON manifest.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ARK_API_KEY from the environment and writes character images plus manifest.json to the selected output directory.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
