## Description:

AI pixel art sprite generation + processing pipeline for Godot games. Generate sprite sheets with Seedream, auto-process into Godot-ready assets (hframes, transparent PNG).

This skill is ready for commercial/non-commercial use.

## Publisher:

[muxueqingze](https://clawhub.ai/user/muxueqingze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game teams use this skill to generate pixel-art prompts, run local Python processing scripts, and turn AI-created sprite sheets into Godot-ready transparent PNG frames and sprite sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch generation can run arbitrary Python helper paths through configurable generator or processor arguments.

Mitigation: Run only reviewed helper scripts from trusted locations, and do not pass untrusted paths to --generator or --processor.

Risk: Unsafe configuration values can cause output writes outside the intended asset tree.

Mitigation: Use trusted JSON configs, review output_base, category, and asset name values before batch runs, and keep outputs in a disposable project directory.

Risk: The skill runs local Python scripts and depends on Pillow.

Mitigation: Install dependencies in a virtual environment with a pinned Pillow version before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muxueqingze/skills/pixel-asset-pipeline)
- [Sample batch configuration](references/sample_config.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced local scripts can produce PNG sprite sheets and individual transparent PNG frame files when run by the agent or user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
