## Description:

Guides agents in using the Demucs CLI to separate vocals and instrument stems, batch process audio, choose output formats, and tune CPU/GPU performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinesemisaka](https://clawhub.ai/user/chinesemisaka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, audio engineers, and operators use this skill to turn audio separation requests into Demucs commands, including prerequisites, batch processing, output naming, format conversion, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Demucs through pip can introduce dependency supply-chain risk.

Mitigation: Use a pinned Demucs version in an isolated virtual environment or container before running generated commands.

Risk: Batch separation can consume significant CPU/GPU memory or process more local audio than intended.

Mitigation: Review generated batch commands, use explicit paths, and reduce segment size or batch size when memory is constrained.

Risk: Audio files may contain private or licensed content handled by local tools.

Mitigation: Keep processing local, verify input and output directories, and follow the user's content handling requirements before running commands.

## Reference(s):

- [Demucs GitHub repository](https://github.com/facebookresearch/demucs)
- [ClawHub skill page](https://clawhub.ai/chinesemisaka/skills/music-seperator-demucs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Demucs and FFmpeg prerequisites, local file path guidance, batch processing examples, output format options, and memory/performance tuning notes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
