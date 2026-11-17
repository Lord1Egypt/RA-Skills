## Description:

Turns a keyword or reference image into an installable Codex v2 pet package with generated sprites, deterministic QA, and packaging support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a keyword, brand cue, or reference image into an installable Codex v2 pet package, including spritesheet assembly, validation, and packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local run artifacts and installs finished custom pets under the user's Codex pets directory.

Mitigation: Install and run it only when local pet asset creation is intended, and review the generated pet.json and spritesheet.webp before use.

Risk: Brand discovery can search the web using a supplied brand, company, product, or prospect name.

Mitigation: Provide non-confidential mascot cues instead of sensitive brand names when web discovery is not desired.

Risk: A reused pet id could overwrite or conflict with an existing custom pet package.

Mitigation: Use a unique pet id and check the target Codex pets directory before installation.

## Reference(s):

- [Codex V2 Pet Contract](references/codex-pet-contract.md)
- [V2 Animation Rows](references/animation-rows.md)
- [V2 Pet QA Rubric](references/qa-rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Codex pet artifacts such as pet.json and spritesheet.webp, plus QA images and JSON reports during generation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
