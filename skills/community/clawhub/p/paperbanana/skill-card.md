## Description:

Generate publication-quality academic diagrams from paper methodology text

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwzhu-pku](https://clawhub.ai/user/dwzhu-pku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical authors use this skill to turn paper methodology text and figure captions into academic diagrams or pipeline figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports under-disclosed automatic network downloads and broad local imports.

Mitigation: Install only in a trusted project directory, review local imports before installation, and expect outbound network access including the PaperBananaBench dataset download.

Risk: The default workflow can make multiple parallel model-provider calls and may create cost or latency surprises.

Mitigation: Review model-provider costs before use and lower num-candidates or critic rounds when testing.

Risk: Untrusted or ambiguous input and output paths could cause unintended file reads or writes.

Mitigation: Use explicit input and output paths and avoid running the skill where untrusted files exist in the parent directory.

## Reference(s):

- [PaperBanana: Automating Academic Illustration for AI Scientists](https://arxiv.org/abs/2601.23265)
- [PaperBananaBench Dataset](https://huggingface.co/datasets/dwzhu/PaperBananaBench)
- [ClawHub Skill Page](https://clawhub.ai/dwzhu-pku/skills/paperbanana)
- [Publisher Profile](https://clawhub.ai/user/dwzhu-pku)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image files with absolute output paths printed as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate multiple candidate image files when num-candidates is greater than 1.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
